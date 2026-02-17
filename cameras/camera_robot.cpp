#include "camera_robot.hpp"

RobotCamera::RobotCamera(const std::string& config_file)
    : BaseCameraReader(config_file)
{
}

void RobotCamera::processFrames() 
{
    try {
        rs2::frameset frames = pipeline_.wait_for_frames(1000);
        rs2::align align_to_color(RS2_STREAM_COLOR);
        auto aligned_frames = align_to_color.process(frames);
        rs2::depth_frame depth = aligned_frames.get_depth_frame();
        rs2::video_frame color = aligned_frames.get_color_frame();

        if (!depth || !color) return;

        cv::Mat input_img(cv::Size(color.get_width(), color.get_height()), CV_8UC3,
                          (void*)color.get_data(), cv::Mat::AUTO_STEP);
        
        if (input_img.empty()) return;

        cv::imshow("Robot Camera - " + serial_, input_img);

        cv::Mat rgb_img = input_img.clone();
        cv::Mat depth_mat(cv::Size(depth.get_width(), depth.get_height()), CV_16U,
                          (void*)depth.get_data(), cv::Mat::AUTO_STEP);

        if (depth_mat.empty()) return;

        auto depth_intrinsics = depth.get_profile()
                                    .as<rs2::video_stream_profile>()
                                    .get_intrinsics();

        // Initialize reference point (once)
        if (!ref_pt_3d_.x)
        {
            float d_m = depth.get_distance(static_cast<int>(ref_pt_.x), static_cast<int>(ref_pt_.y));
            if (d_m > 0.0f) 
            {
                float pixel[2] = { static_cast<float>(ref_pt_.x),
                                    static_cast<float>(ref_pt_.y) };
                float pos[3];
                rs2_deproject_pixel_to_point(pos, &depth_intrinsics, pixel, d_m);
                ref_pt_3d_ = cv::Point3f(pos[0], pos[1], pos[2]);
                if (debug_) 
                {
                    std::cout << "[robot_camera] Reference point 3D (m): X=" << ref_pt_3d_.x 
                              << " Y=" << ref_pt_3d_.y << " Z=" << ref_pt_3d_.z << "\n";
                }
            } else {
                std::cerr << "Warning: Invalid depth at ref_pt\n";
            }
        }

        cv::Mat obj_mask = cv::Mat::zeros(depth_mat.rows, depth_mat.cols, CV_8U);

        for (int y = 0; y < depth_mat.rows; ++y) {
            for (int x = 0; x < depth_mat.cols; ++x) {
                float depth_value_mm = depth.get_distance(x, y) * 1000.0f;

                if (depth_value_mm == 0) continue;

                float pixel[2] = { static_cast<float>(x), static_cast<float>(y) };
                float point[3];
                rs2_deproject_pixel_to_point(point, &depth_intrinsics, pixel, depth_value_mm);

                float z_mm = point[2];

                if (z_mm < conveyor_z_dist_ - min_obj_height_) {
                    obj_mask.at<uint8_t>(y, x) = 255;
                }
            }
        }

        cv::GaussianBlur(obj_mask, obj_mask, cv::Size(5,5), 1.4);
        cv::Canny(obj_mask, obj_mask, canny_thresh_.at(0), canny_thresh_.at(1));

        std::vector<std::vector<cv::Point>> obj_contours;
        cv::findContours(obj_mask, obj_contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        // Process contours
        for (size_t ci = 0; ci < obj_contours.size(); ++ci) {
            const auto &cnt = obj_contours[ci];
            if (cv::contourArea(cnt) < 100.0) continue;  // Kleinere Mindestfläche

            cv::RotatedRect rrect = cv::minAreaRect(cnt);
            cv::Point2f box2f[4];
            rrect.points(box2f);

            std::vector<cv::Point3f> corners3d(4);
            for (int k = 0; k < 4; ++k) {
                int px = std::lround(box2f[k].x);
                int py = std::lround(box2f[k].y);
                
                if (px < 0 || py < 0 || px >= depth.get_width() || py >= depth.get_height()) {
                    corners3d[k] = cv::Point3f(NAN, NAN, NAN);
                    continue;
                }

                float d = depth.get_distance(px, py);
                if (d <= 0.0f) {
                    corners3d[k] = cv::Point3f(NAN, NAN, NAN);
                    continue;
                }

                float pixel[2] = { static_cast<float>(px), static_cast<float>(py) };
                float pos[3];
                rs2_deproject_pixel_to_point(pos, &depth_intrinsics, pixel, d);
                corners3d[k] = cv::Point3f(pos[0], pos[1], pos[2]);
            }

            // Calculate 2D center of contour
            cv::Moments m = cv::moments(cnt);
            float center_x_2d = (m.m10 / m.m00);
            float center_y_2d = (m.m01 / m.m00);

            // Collect valid depth values from all contour pixels
            float depth_sum = 0.0f;
            int valid_depth_count = 0;
            for (const auto& pt : cnt) {
                int px = pt.x;
                int py = pt.y;
                if (px >= 0 && py >= 0 && px < depth.get_width() && py < depth.get_height()) {
                    float d = depth.get_distance(px, py);
                    if (d > 0.0f) {
                        depth_sum += d;
                        valid_depth_count++;
                    }
                }
            }

            // Use average depth if available, otherwise try corner depths
            float center_depth = NAN;
            if (valid_depth_count > 0) {
                center_depth = depth_sum / valid_depth_count;
            } else {
                // Fallback: Find first valid depth from corners
                for (const auto& corner : corners3d) {
                    if (std::isfinite(corner.z)) {
                        center_depth = corner.z;
                        break;
                    }
                }
            }

            Object3D object;
            cv::Point3f obj_center;

            // If we have valid depth, deproject the 2D center to 3D
            if (std::isfinite(center_depth) && center_depth > 0.0f) {
                float pixel[2] = { center_x_2d, center_y_2d };
                float pos[3];
                rs2_deproject_pixel_to_point(pos, &depth_intrinsics, pixel, center_depth);
                obj_center = cv::Point3f(pos[0], pos[1], pos[2]);
            } else {
                // If no valid depth, use 2D center with NAN for 3D conversion
                // (This still allows us to get relative positions)
                obj_center = cv::Point3f(center_x_2d, center_y_2d, NAN);
            }

            object.x = (obj_center.x - ref_pt_3d_.x) * 1000;
            object.y = (obj_center.y - ref_pt_3d_.y) * 1000;
            object.z = (obj_center.z - ref_pt_3d_.z) * 1000;
            object.orientation = computeOrientation2D(corners3d);

            auto dist_mm = [](const cv::Point3f& A, const cv::Point3f& B)->float {
                if (!std::isfinite(A.x) || !std::isfinite(B.x)) return NAN;
                float dx = A.x - B.x, dy = A.y - B.y, dz = A.z - B.z;
                return std::sqrt(dx*dx + dy*dy + dz*dz) * 1000.0f;
            };

            float length_mm = dist_mm(corners3d[0], corners3d[1]);
            float width_mm = dist_mm(corners3d[1], corners3d[2]);
            if (length_mm < width_mm) std::swap(length_mm, width_mm);

            // Height calculation
            cv::Mat mask_roi = cv::Mat::zeros(obj_mask.size(), CV_8U);
            cv::drawContours(mask_roi, std::vector<std::vector<cv::Point>>{cnt}, -1, 255, cv::FILLED);
            
            float sum_z_mm = 0.0f;
            size_t count_z = 0;
            for (size_t y = 0; y < mask_roi.rows; ++y) {
                for (size_t x = 0; x < mask_roi.cols; ++x) {
                    if (mask_roi.at<uint8_t>(y, x) == 0) continue;

                    float d = depth.get_distance(x, y);

                    if (d <= 0.0f) continue;

                    float pixel[2] = { static_cast<float>(x), static_cast<float>(y) };
                    float pos[3];
                    rs2_deproject_pixel_to_point(pos, &depth_intrinsics, pixel, d);

                    float z_mm = pos[2] * 1000.0f;
                    sum_z_mm += z_mm;
                    count_z++;
                }
            }

            float height_mm = NAN;
            if (count_z > 0) {
                float z_mm = sum_z_mm / static_cast<float>(count_z);
                height_mm = conveyor_z_dist_ - z_mm + 20;
            }

            object.length = length_mm;
            object.width = width_mm;
            object.height = height_mm;

            // Filter: Skip objects with Height > 60 mm
            if (std::isfinite(object.height) && object.height > 60.0f) {
                continue;
            }

            // Validate object coordinates before adding to list
            if (!std::isfinite(object.x) || !std::isfinite(object.y) || !std::isfinite(object.z)) {
                if (debug_) {
                    std::cout << "[robot_camera] Skipping object with invalid coordinates: ("
                              << object.x << ", " << object.y << ", " << object.z << ")\n";
                }
                continue;
            }

            size_t id;
            if (checkIfObjIsInList(object, id)) {
                if (id < obj_list_.size()) {
                    obj_list_[id] = object;
                }
            } else {
                obj_list_.push_back(object);
            }

            sendObjList();

            if (debug_) {
                std::cout << "[robot_camera] Object " << ci << ": L=" << object.length << "mm W=" << object.width
                          << "mm    x:" << object.x << "mm y:" << object.y << "mm z:" << object.z << "mm \n";
                std::cout << "[robot_camera] listsize: " << obj_list_.size() << std::endl;

                std::vector<cv::Point> poly;
                for (int k = 0; k < 4; ++k) {
                    poly.emplace_back(std::lround(box2f[k].x), std::lround(box2f[k].y));
                }
                cv::polylines(input_img, std::vector<std::vector<cv::Point>>{poly}, true, cv::Scalar(0, 0, 255), 2);
                cv::putText(input_img, std::to_string(int(length_mm)) + "mm", poly[0],
                            cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(255, 0, 0), 2);
            }
        }

        if (debug_) {
            cv::imshow("Input RGB - " + serial_, rgb_img);
            // cv::imshow("Annotated ROI - " + serial_, input_img);
            cv::imshow("Depth Mat - " + serial_, depth_mat);
            
        }

    } catch (const rs2::error &e) {
        std::cerr << "[CameraReader2] RealSense error: " << e.what() << "\n";
    } catch (const std::exception &e) {
        std::cerr << "[CameraReader2] Exception: " << e.what() << "\n";
    }
}
