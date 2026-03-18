#include "camera_robot.hpp"
#include <algorithm>
#include <string>
#include <vector>

RobotCamera::RobotCamera(const std::string& config_file)
    : BaseCameraReader(config_file)
{
    sub_socket_.set(zmq::sockopt::subscribe, "obj_list");
    sub_socket_.set(zmq::sockopt::rcvtimeo, 0);
    sub_socket_.connect("tcp://127.0.0.1:5555");
}

bool RobotCamera::receiveStaticObject()
{
    zmq::message_t topic_msg;
    zmq::message_t data_msg;

    auto topic_result = sub_socket_.recv(topic_msg, zmq::recv_flags::dontwait);
    if (!topic_result) {
        return false;
    }

    auto data_result = sub_socket_.recv(data_msg, zmq::recv_flags::none);
    if (!data_result) {
        return false;
    }

    Objects3D_msg list_msg;
    if (!list_msg.ParseFromArray(data_msg.data(), static_cast<int>(data_msg.size()))) {
        return false;
    }

    if (list_msg.objects_size() == 0) {
        return false;
    }

    const auto& obj = list_msg.objects(0);      // Aktuell immer das erste Objekt in der Liste nehmen -> Wir greifen Obj. mit kleinster ID
    current_obj.z = obj.z();
    current_obj.orientation = obj.orientation();
    current_obj.width = obj.width();
    current_obj.length = obj.length();
    current_obj.height = obj.height();
    return true;
}

void RobotCamera::processFrames() 
{
    try {
        receiveStaticObject();

        rs2::frameset frames = pipeline_.wait_for_frames(3000);
        rs2::align align_to_color(RS2_STREAM_COLOR);
        auto aligned_frames = align_to_color.process(frames);
        rs2::depth_frame depth = aligned_frames.get_depth_frame();
        rs2::video_frame color = aligned_frames.get_color_frame();

        if (!depth || !color) return;

        cv::Mat input_img(cv::Size(color.get_width(), color.get_height()), CV_8UC3,
                           (void*)color.get_data(), cv::Mat::AUTO_STEP);

        if (input_img.empty()) return;

        cv::Mat depth_mat(cv::Size(depth.get_width(), depth.get_height()), CV_16U,
                           (void*)depth.get_data(), cv::Mat::AUTO_STEP);

        if (depth_mat.empty()) return;
        cv::Mat depth_raw = depth_mat.clone();

        auto depth_intrinsics = depth.get_profile()
                       .as<rs2::video_stream_profile>()
                       .get_intrinsics();


        constexpr float kMmPerMeter = 1000.0f;
        cv::Mat depth_bin = cv::Mat::zeros(depth_mat.rows, depth_mat.cols, CV_8U);

        auto get_z_mm = [&](int x, int y, float& z_mm) -> bool {
            uint16_t raw_depth = depth_mat.at<uint16_t>(y, x);
            if (raw_depth == 0) return false;

            float depth_m = static_cast<float>(raw_depth) / kMmPerMeter;
            float pixel[2] = {static_cast<float>(x), static_cast<float>(y)};
            float point_3d[3];
            rs2_deproject_pixel_to_point(point_3d, &depth_intrinsics, pixel, depth_m);

            if (point_3d[2] <= 0.0f) return false;

            z_mm = point_3d[2] * kMmPerMeter;
            return true;
        };

        // Segmentation based on depth thresholding around predicted object z + offset
        for (int y = 0; y < depth_mat.rows; ++y) {
            for (int x = 0; x < depth_mat.cols; ++x) {
                float z_mm = 0.0f;
                if (get_z_mm(x, y, z_mm) == 0){
                    depth_bin.at<uint8_t>(y, x) = 255;
                } 
                else {
                    depth_bin.at<uint8_t>(y, x) = 0;
                }
            }
        }        

        // Morphology tuning against edge noise
        cv::Mat morph_kernel = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(15, 15));
        cv::morphologyEx(depth_bin, depth_bin, cv::MORPH_OPEN, morph_kernel, cv::Point(-1, -1), 1);

        // Calculate the center of the object (largest contour) in mm
        std::vector<std::vector<cv::Point>> contours;
        cv::findContours(depth_bin, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        cv::Mat object_mask = cv::Mat::zeros(depth_bin.size(), CV_8U);

        if (!contours.empty()) {
            // extract largest contour
            auto largest_it = std::max_element(
                contours.begin(), contours.end(),
                [](const std::vector<cv::Point>& a, const std::vector<cv::Point>& b) {
                    return cv::contourArea(a) < cv::contourArea(b);
                });

            cv::drawContours(object_mask,
                                std::vector<std::vector<cv::Point>>{*largest_it},
                                0,
                                cv::Scalar(255),
                                cv::FILLED);

            int max_y_px = -1;
            double sum_all_x_px = 0.0;
            int object_pixel_count = 0;

            for (int y = 0; y < object_mask.rows; ++y) {
                for (int x = 0; x < object_mask.cols; ++x) {
                    if (object_mask.at<uint8_t>(y, x) == 0) continue;
                    sum_all_x_px += static_cast<double>(x);
                    object_pixel_count++;
                    if (y > max_y_px) {
                        max_y_px = y;
                    }
                }
            }

            if (object_pixel_count > 0 && max_y_px >= 0) {
                int mean_x_px = static_cast<int>(std::lround(sum_all_x_px / object_pixel_count));

                mean_x_px = std::clamp(mean_x_px, 0, depth_raw.cols - 1);

                auto try_get_depth_m = [&](int px, int py, float& depth_m) -> bool {
                    constexpr int kSearchRadiusPx = 2;
                    for (int dy = -kSearchRadiusPx; dy <= kSearchRadiusPx; ++dy) {
                        for (int dx = -kSearchRadiusPx; dx <= kSearchRadiusPx; ++dx) {
                            int sx = std::clamp(px + dx, 0, depth_raw.cols - 1);
                            int sy = std::clamp(py + dy, 0, depth_raw.rows - 1);
                            uint16_t raw_depth = depth_raw.at<uint16_t>(sy, sx);
                            if (raw_depth == 0) continue;
                            depth_m = static_cast<float>(raw_depth) / kMmPerMeter;
                            return true;
                        }
                    }
                    return false;
                };

                float depth_m = 0.0f;
                if (try_get_depth_m(mean_x_px, max_y_px, depth_m)) {
                    // get distance Data of a point on conveyor infront of object, because the LiDAR can't detect the object
                    // as ist is too close to the camera
                    float pixel[2] = {static_cast<float>(mean_x_px), static_cast<float>(max_y_px+1)};
                    float point_3d[3];
                    rs2_deproject_pixel_to_point(point_3d, &depth_intrinsics, pixel, depth_m);

                    if (point_3d[2] > 0.0f) {
                        float obj_x_mm = point_3d[0] * kMmPerMeter;
                        float obj_y_mm = -1 * point_3d[1] * kMmPerMeter + current_obj.length / 2;       // Orientierung einberechnen später
                        float obj_z_mm = current_obj.z;

                        if (debug_) {
                            std::cout << "[robot_camera] Bottom edge: max_y_px=" << max_y_px
                                      << ", current_obj.length=" << current_obj.length
                                      << ", point_3d[1]=" << point_3d[1]
                                    //   << ", mean_x_px=" << mean_x_px
                                    //   << ", obj_x_mm=" << obj_x_mm
                                      << ", obj_y_mm=" << obj_y_mm << "\n";
                        }

                        // Send bottom-edge representative 3D point
                        sendCoordinates(obj_x_mm, obj_y_mm, obj_z_mm);
                    }
                }
            }
        }

        cv::imshow("Robot Camera - " + serial_, input_img);
        cv::imshow("depth mat" + serial_, object_mask);
    } catch (const rs2::error& e) {
        std::string message = e.what();
        if (message.find("Frame didn't arrive") != std::string::npos) {
            if (debug_) {
                std::cerr << "[robot_camera] Frame timeout, retrying...\n";
            }
            return;
        }
        std::cerr << "[robot_camera] RealSense error: " << message << "\n";
    } catch (const std::exception& e) {
        std::cerr << "[robot_camera] Exception: " << e.what() << "\n";
    }
}
