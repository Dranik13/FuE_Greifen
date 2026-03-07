/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 1. Objekte werden von Stationärer Kamera erkannt und in eine Liste gepackt. Jedes Objekt hat: Größe, Pose, Geschw. und Klasse
// 2. Position der Objekte wird dauerhaft auf Basis der Geschw. in der Liste aktualisiert. -> Geschwindigkeit als globaler Eintrag?? 
// 3. Regler sucht sich ein Objekt raus und positioniert sich einem Versatz in y-Richtung über dem Objekt 
// 4. Roboterkamera lokalisiert Objekt und Distanz zum Objekt -> Wenn keine Distanzdaten da sind orientiert man sich an der Größe des Loches -> Abgleich mit gespeicherten Größendaten??
// 5. Roboter richtet sich den Kameradaten nach aus, sodass Objekt zentral liegt
// 6. Roboter bleibt stehen und der Griffzeitpunkt wird anhand der Objektgeschwindigkeit ermittelt
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "camera_static.hpp"
#include "apriltag/apriltag.h"
#include "apriltag/apriltag_pose.h"
#include "apriltag/tag36h11.h"


StaticCamera::StaticCamera(const std::string& config_file)
    : BaseCameraReader(config_file)
{
}

void calibration() 
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

        // cv::imshow("Static Camera - " + serial_, input_img);

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
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    // ================= USER PARAMS =================
    double TAG_SIZE = 0.027;   // Meter

    rs2::video_stream_profile color_profile = profile_.get_stream(RS2_STREAM_COLOR).as<rs2::video_stream_profile>();

    rs2_intrinsics intr = color_profile.get_intrinsics();

    double fx = intr.fx;
    double fy = intr.fy;
    double cx = intr.ppx;
    double cy = intr.ppy;
    // Intrinsics von RealSense (bereits ausgelesen)
    cv::Mat cameraMatrix = (cv::Mat_<double>(3,3) <<
        fx, 0, cx,
        0, fy, cy,
        0, 0, 1);

    cv::Mat distCoeffs = cv::Mat::zeros(4,1,CV_64F);

    // ================= APRILTAG SETUP =================
    apriltag_family_t* tf = tag25h9_create();
    apriltag_detector_t* td = apriltag_detector_create();
    apriltag_detector_add_family(td, tf);

    td->quad_decimate = 1.0;
    td->quad_sigma = 0.0;
    td->nthreads = 4;

    // ================= IMAGE PROCESSING =================
    // color_frame -> cv::Mat frame (BGR)
    cv::Mat gray;
    cv::cvtColor(input_img, gray, cv::COLOR_BGR2GRAY);

    // In AprilTag Image konvertieren
    image_u8_t img_header{gray.cols, gray.rows, gray.cols, gray.data};
    zarray_t* detections = apriltag_detector_detect(td, &img_header);

    cv::Vec3d rvec_final, tvec_final;
    bool pose_valid = false;
    std::cout << "zarray_size(detections) = " << zarray_size(detections) << "\n";
    
    for (int i = 0; i < zarray_size(detections); i++)
    {
        std::cout << "AprilTag detected: ID=" << i << "\n";
        apriltag_detection_t* det;
        zarray_get(detections, i, &det);

        apriltag_detection_info_t info;
        info.det = det;
        info.tagsize = TAG_SIZE;
        info.fx = fx;
        info.fy = fy;
        info.cx = cx;
        info.cy = cy;

        apriltag_pose_t pose;
        double err = estimate_tag_pose(&info, &pose);

        if (err >= 0)
        {
            cv::Mat R(3,3,CV_64F);
            cv::Mat t(3,1,CV_64F);

            for(int r=0;r<3;r++)
                for(int c=0;c<3;c++)
                    R.at<double>(r,c) = MATD_EL(pose.R, r, c);

            for(int r=0;r<3;r++)
                t.at<double>(r) = pose.t->data[r];

            cv::Rodrigues(R, rvec_final);
            tvec_final = t;

            cv::drawFrameAxes(input_img, cameraMatrix, distCoeffs,
                            rvec_final, tvec_final, 0.05);

            pose_valid = true;
        }
    }
    cv::imshow("AprilTag Calibration", input_img);

    // ================= TRANSFORMATION =================
    if (pose_valid)
    {
        std::cout << "Pose valid" << std::endl;
        cv::Mat R;
        cv::Rodrigues(rvec_final, R);

        cv::Mat T = cv::Mat::eye(4,4,CV_64F);
        R.copyTo(T(cv::Rect(0,0,3,3)));
        T.at<double>(0,3) = tvec_final[0];
        T.at<double>(1,3) = tvec_final[1];
        T.at<double>(2,3) = tvec_final[2];

        cv::Matx44d T_matx;
        for (int r = 0; r < 4; ++r) {
            for (int c = 0; c < 4; ++c) {
                T_matx(r, c) = T.at<double>(r, c);
            }
        }

        T_cam_to_belt_ = T_matx;
        extrinsics_loaded_ = true;

        if (debug_) {
            std::cout << "T_cam_to_board:\n" << T << std::endl;
        }
    }

        if (extrinsics_loaded_) {
            std::cout << "Extrinsics loaded, processing depth data...\n";
            int px = std::clamp(ref_pt_.x, 0, depth.get_width() - 1);
            int py = std::clamp(ref_pt_.y, 0, depth.get_height() - 1);
            float d_m = depth.get_distance(px, py);

            if (d_m > 0.0f) {
                float pixel[2] = { static_cast<float>(px), static_cast<float>(py) };
                float cam_point[3] = {0.f, 0.f, 0.f};
                rs2_deproject_pixel_to_point(cam_point, &depth_intrinsics, pixel, d_m);

                cv::Point3f belt_point_m = transformCamToBelt(
                    cv::Point3f(cam_point[0], cam_point[1], cam_point[2]));

                float x_mm = belt_point_m.x * 1000.0f;
                float y_mm = belt_point_m.y * 1000.0f;
                float z_mm = belt_point_m.z * 1000.0f;

                sendCoordinates(x_mm, y_mm, z_mm);

                if (debug_) {
                    std::cout << "[static_camera] ref_pt belt [mm]: x=" << x_mm
                              << " y=" << y_mm
                              << " z=" << z_mm << "\n";
                }
            }
        }
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



        if (debug_) {
            cv::imshow("Input - " + serial_, input_img);
            // cv::imshow("Mask - " + serial_, mask_roi);
            cv::imshow("Annotated ROI - " + serial_, rgb_img);
        }

    } catch (const rs2::error &e) {
        std::cerr << "[static_camera] RealSense error: " << e.what() << "\n";
    } catch (const std::exception &e) {
        std::cerr << "[static_camera] Exception: " << e.what() << "\n";
    }
}
