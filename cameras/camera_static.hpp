#ifndef CAMERA_STATIC_HPP
#define CAMERA_STATIC_HPP

#include "camera_reader_base.hpp"


/**
 * StaticCamera: Camera reader for fixed camera overlooking conveyor belt
 * - Detects objects on the conveyor belt
 * - Estimates object velocities 
 * - Updates existing objects in the list
 */
class StaticCamera : public BaseCameraReader {
public:
    explicit StaticCamera(const std::string& config_file = "config_cam_static.yml");

private:
    void processFrames() override;
    cv::Point3f transformCamToRobot(const cv::Point3f& cam_point_m) const;

    // Frame skipping: process only every 3rd frame
    int frame_skip_counter_ = 0;
    static constexpr int FRAME_SKIP = 3;

    // Velocity filtering: exponential moving average (alpha = smoothing factor 0..1)
    float filtered_velocity_y_ = 0.0f;
    static constexpr float VEL_FILTER_ALPHA = 0.3f;  // 0.3 = 30% new, 70% old -> low-pass filter
    
    // FPS tracking
    int frame_count_ = 0;
    std::chrono::high_resolution_clock::time_point last_fps_time_;
};

#endif // CAMERA_STATIC_HPP
