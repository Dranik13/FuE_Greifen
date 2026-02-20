#include "camera_robot.hpp"
#include <algorithm>
#include <string>
#include <vector>

RobotCamera::RobotCamera(const std::string& config_file)
    : BaseCameraReader(config_file)
{
}

void RobotCamera::processFrames() 
{
    try {
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
        constexpr uint16_t kZThresholdMm = 200;
        constexpr float kMaskOffsetMm = 30.0f;
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

        // Tiefenwerte sammeln (downsampled für Speed)
        std::vector<float> object_depth_values;
        constexpr int kSampleStep = 4;  // Nur jeden 4. Pixel
        for (int y = 0; y < depth_mat.rows; y += kSampleStep) {
            for (int x = 0; x < depth_mat.cols; x += kSampleStep) {
                float z_mm = 0.0f;
                if (get_z_mm(x, y, z_mm)) {
                    object_depth_values.push_back(z_mm);
                }
            }
        }

        // Median berechnen
        if (!object_depth_values.empty()) {
            std::nth_element(object_depth_values.begin(),
                             object_depth_values.begin() + (object_depth_values.size() - 1) / 2,
                             object_depth_values.end());
            size_t mid = (object_depth_values.size() - 1) / 2;
            float median_z = object_depth_values[mid];
        
            if (debug_) {
                // std::cout << "[robot_camera] Median Z-Koordinate: " << median_z << "mm\n";
            }
        
            // Segmentierung basierend auf Z-Koordinate
            for (int y = 0; y < depth_mat.rows; ++y) {
                for (int x = 0; x < depth_mat.cols; ++x) {
                    float z_mm = 0.0f;
                    if (!get_z_mm(x, y, z_mm)) continue;

                    // Wenn Z-Koordinate signifikant kleiner ist → Objekt
                    if ((median_z - z_mm) > kZThresholdMm) {
                        depth_mat.at<uint16_t>(y, x) = static_cast<uint16_t>(median_z);
                    }
                }
            }
            // Mittelwert berechnen + binäre Maske in einem Durchlauf
            double sum_z = 0.0;
            int valid_pixels = 0;
        
            for (int y = 0; y < depth_mat.rows; ++y) {
                for (int x = 0; x < depth_mat.cols; ++x) {
                    float z_mm = 0.0f;
                    if (!get_z_mm(x, y, z_mm)) continue;
                    sum_z += z_mm;
                    valid_pixels++;
                }
            }
            if (valid_pixels == 0) {
                cv::imshow("Robot Camera - " + serial_, input_img);
                return;
            }

            float mean_z = static_cast<float>(sum_z / valid_pixels);
            std::cout << "Mean z-coordinate: " << mean_z << "mm\n";

            // Erzeuge binäre Maske: Pixel signifikant vor dem Mittelwert -> 255
            for (int y = 0; y < depth_mat.rows; ++y) {
                for (int x = 0; x < depth_mat.cols; ++x) {
                    float z_mm = 0.0f;
                    if (!get_z_mm(x, y, z_mm)) continue;

                    if (z_mm < mean_z - kMaskOffsetMm) {
                        depth_bin.at<uint8_t>(y, x) = 255;
                    }
                }
            }
            

            // Mittelpunkt des Objekts (größte Kontur) in mm berechnen
            std::vector<std::vector<cv::Point>> contours;
            cv::findContours(depth_bin, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

            if (!contours.empty()) {
                auto largest_it = std::max_element(
                    contours.begin(), contours.end(),
                    [](const std::vector<cv::Point>& a, const std::vector<cv::Point>& b) {
                        return cv::contourArea(a) < cv::contourArea(b);
                    });

                cv::Mat object_mask = cv::Mat::zeros(depth_bin.size(), CV_8U);
                cv::drawContours(object_mask,
                                 std::vector<std::vector<cv::Point>>{*largest_it},
                                 0,
                                 cv::Scalar(255),
                                 cv::FILLED);

                double sum_x_mm = 0.0;
                double sum_y_mm = 0.0;
                double sum_z_mm = 0.0;
                int object_valid_pixels = 0;

                for (int y = 0; y < object_mask.rows; ++y) {
                    for (int x = 0; x < object_mask.cols; ++x) {
                        if (object_mask.at<uint8_t>(y, x) == 0) continue;

                        uint16_t raw_depth = depth_raw.at<uint16_t>(y, x);
                        if (raw_depth == 0) continue;

                        float depth_m = static_cast<float>(raw_depth) / kMmPerMeter;
                        float pixel[2] = {static_cast<float>(x), static_cast<float>(y)};
                        float point_3d[3];
                        rs2_deproject_pixel_to_point(point_3d, &depth_intrinsics, pixel, depth_m);

                        if (point_3d[2] <= 0.0f) continue;

                        sum_x_mm += static_cast<double>(point_3d[0] * kMmPerMeter);
                        sum_y_mm += static_cast<double>(point_3d[1] * kMmPerMeter);
                        sum_z_mm += static_cast<double>(point_3d[2] * kMmPerMeter);
                        object_valid_pixels++;
                    }
                }

                if (object_valid_pixels > 0) {
                    float center_x_mm = static_cast<float>(sum_x_mm / object_valid_pixels);
                    float center_y_mm = static_cast<float>(sum_y_mm / object_valid_pixels);
                    float center_z_mm = static_cast<float>(sum_z_mm / object_valid_pixels);

                    std::cout << "Objektmittelpunkt [mm] (X, Y, Z): "
                              << center_x_mm << ", "
                              << center_y_mm << ", "
                              << center_z_mm << "\n";
                
                    // Send coordinates via ZMQ
                    sendCoordinates(center_x_mm, center_y_mm, center_z_mm);
                }
            }
        }

        cv::imshow("Robot Camera - " + serial_, input_img);
        cv::imshow("depth mat" + serial_, depth_bin);
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
