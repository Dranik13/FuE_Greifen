/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 1. Objekte werden von Stationärer Kamera erkannt und in eine Liste gepackt. Jedes Objekt hat: Größe, Pose, Geschw. und Klasse
// 2. Position der Objekte wird dauerhaft auf Basis der Geschw. in der Liste aktualisiert. -> Geschwindigkeit als globaler Eintrag?? 
// 3. Regler sucht sich ein Objekt raus und positioniert sich einem Versatz in y-Richtung über dem Objekt 
// 4. Roboterkamera lokalisiert Objekt und Distanz zum Objekt -> Wenn keine Distanzdaten da sind orientiert man sich an der Größe des Loches -> Abgleich mit gespeicherten Größendaten??
// 5. Roboter richtet sich den Kameradaten nach aus, sodass Objekt zentral liegt
// 6. Roboter bleibt stehen und der Griffzeitpunkt wird anhand der Objektgeschwindigkeit ermittelt
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "camera_static.hpp"

StaticCamera::StaticCamera(const std::string& config_file)
    : BaseCameraReader(config_file)
{
}

void StaticCamera::processFrames() 
{
    try {
        rs2::frameset frames = pipeline_.wait_for_frames(1000);
        rs2::align align_to_color(RS2_STREAM_COLOR);
        auto aligned_frames = align_to_color.process(frames);
        rs2::depth_frame depth = aligned_frames.get_depth_frame();
        rs2::video_frame color = aligned_frames.get_color_frame();

        if (!depth || !color) return;

        // Frame skipping: only process every FRAME_SKIP-th frame
        frame_skip_counter_++;
        if (frame_skip_counter_ < FRAME_SKIP) {
            return;
        }
        frame_skip_counter_ = 0;

        cv::Mat input_img(cv::Size(color.get_width(), color.get_height()), CV_8UC3,
                          (void*)color.get_data(), cv::Mat::AUTO_STEP);
        
        if (input_img.empty()) return;

        cv::imshow("Static Camera - " + serial_, input_img);

        // Handle ROI: if roi is empty (0,0,0,0), use full frame as effective_roi
        cv::Rect effective_roi = (roi_.area() > 0) ? roi_ : cv::Rect(0, 0, input_img.cols, input_img.rows);
        
        cv::Mat rgb_img = input_img(effective_roi).clone();
        cv::Mat depth_mat(cv::Size(depth.get_width(), depth.get_height()), CV_16U,
                          (void*)depth.get_data(), cv::Mat::AUTO_STEP);

        if (depth_mat.empty()) return;

        cv::Mat depth_roi = depth_mat(effective_roi).clone();

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
                    std::cout << "[static_camera] Reference point 3D (m): X=" << ref_pt_3d_.x 
                              << " Y=" << ref_pt_3d_.y << " Z=" << ref_pt_3d_.z << "\n";
                }
            } else {
                std::cerr << "Warning: Invalid depth at ref_pt\n";
            }
        }

        // Create mask
        cv::Mat obj_mask = cv::Mat::zeros(depth_roi.rows, depth_roi.cols, CV_8U);

        for (int y = 0; y < depth_roi.rows; ++y) {
            for (int x = 0; x < depth_roi.cols; ++x) {
                int total_x = effective_roi.x + x;
                int total_y = effective_roi.y + y;
                float depth_value_mm = depth.get_distance(total_x, total_y) * 1000.0f;

                if (depth_value_mm == 0) continue;

                float pixel[2] = { static_cast<float>(total_x), static_cast<float>(total_y) };
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

        // Process contours -> collect detections directly as Object3D
        std::vector<Object3D> detected_objects;

        for (size_t ci = 0; ci < obj_contours.size(); ++ci) {
            const auto &cnt = obj_contours[ci];
            if (cv::contourArea(cnt) < 200.0) continue;

            cv::RotatedRect rrect = cv::minAreaRect(cnt);
            cv::Point2f box2f[4];
            rrect.points(box2f);

            std::vector<cv::Point3f> corners3d(4);
            for (int k = 0; k < 4; ++k) {
                int px_roi = std::lround(box2f[k].x);
                int py_roi = std::lround(box2f[k].y);
                int px = effective_roi.x + px_roi;
                int py = effective_roi.y + py_roi;
                
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

            Object3D object;
            cv::Point3f obj_center = computeCenter(corners3d);
            object.x = (obj_center.x - ref_pt_3d_.x) * 1000;
            object.y = (obj_center.y - ref_pt_3d_.y) * 1000;
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

                    int px = effective_roi.x + x;
                    int py = effective_roi.y + y;
                    float d = depth.get_distance(px, py);

                    if (d <= 0.0f) continue;

                    float pixel[2] = { static_cast<float>(px), static_cast<float>(py) };
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

            object.z = (obj_center.z - ref_pt_3d_.z) * 1000 + (height_mm/2);
            object.length = length_mm;
            object.width = width_mm;
            object.height = height_mm;

            // Filter: Skip objects with Heigth > 60 mm
            if (std::isfinite(object.height) && object.height > 60.0f) {
                // if (debug_) {
                //     std::cout << "[static_camera] Skipping object with heigth=" << object.heigth << " mm (> 60 mm)" << std::endl;
                // }
                continue;
            }

            // Validate object coordinates before adding to list
            if (!std::isfinite(object.x) || !std::isfinite(object.y) || !std::isfinite(object.z)) {
                if (debug_) {
                    std::cout << "[static_camera] Skipping object with invalid coordinates: ("
                              << object.x << ", " << object.y << ", " << object.z << ")\n";
                }
                continue;
            }

            detected_objects.push_back(object);
        }
        // Frame timestamp (seconds)
        double frame_ts = color.get_timestamp() / 1000.0;

        // Only update tracker if we have valid detections
        if (detected_objects.empty()) {
            // if (debug_) {
            //     std::cout << "[static_camera] No valid detections in this frame\n";
            // }
            sendObjList();
            return;
        }
        // Update tracker: fills in vy (y-direction velocity) and speed in each detection
        float global_velocity_y = tracker_.update(detected_objects, frame_ts);
        
        // Apply low-pass filter to velocity (exponential moving average)
        filtered_velocity_y_ = VEL_FILTER_ALPHA * global_velocity_y + (1.0f - VEL_FILTER_ALPHA) * filtered_velocity_y_;
        
        // Strategy: Pick a random object from detections and use its y-velocity
        // if its position is within the velocity reference region
        float reference_velocity_y = filtered_velocity_y_;  // Use filtered velocity as fallback
        bool found_reference = false;

        if (!detected_objects.empty()) {
            // Pick random object
            int ref_idx = rand() % detected_objects.size();
            const auto& ref_obj = detected_objects[ref_idx];
            
            // Check if position is within region
            if (ref_obj.x >= velocity_region_x_min_ && ref_obj.x <= velocity_region_x_max_ &&
                ref_obj.y >= velocity_region_y_min_ && ref_obj.y <= velocity_region_y_max_) {
                
                reference_velocity_y = ref_obj.vy;
                found_reference = true;
                
                if (debug_) {
                    std::cout << "[static_camera] Reference object at (" << ref_obj.x << ", " 
                              << ref_obj.y << ") with vy=" << reference_velocity_y << " mm/s\n";
                }
            }
        }

        // Apply reference y-velocity to all detected objects
        for (auto& obj : detected_objects) {
            obj.vy = reference_velocity_y;
            obj.speed = std::abs(reference_velocity_y);

            size_t id;
            if (checkIfObjIsInList(obj, id)) {
                // Update existing object at index id
                if (id < obj_list_.size()) {
                    obj_list_[id] = obj;
                }
            } else {
                // Add new object
                obj_list_.push_back(obj);
            }
        }

        sendObjList();

        if (debug_) {
            cv::imshow("Mask - " + serial_, obj_mask);
            cv::imshow("Annotated ROI - " + serial_, rgb_img);
        }

    } catch (const rs2::error &e) {
        std::cerr << "[static_camera] RealSense error: " << e.what() << "\n";
    } catch (const std::exception &e) {
        std::cerr << "[static_camera] Exception: " << e.what() << "\n";
    }
}
