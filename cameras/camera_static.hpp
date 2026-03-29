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


float normalizeOrientationHalfTurn(float angle_rad)
{
    // Object orientation is 180-deg symmetric; keep angle in [0, pi).
    if (!std::isfinite(angle_rad)) return NAN;
    while (angle_rad >= static_cast<float>(CV_PI)) angle_rad -= static_cast<float>(CV_PI);
    while (angle_rad < 0.0f) angle_rad += static_cast<float>(CV_PI);
    return angle_rad;
}

bool isFiniteXY(const cv::Point3f& point)
{
    return std::isfinite(point.x) && std::isfinite(point.y);
}

bool computeMidpointXY(const cv::Point3f& a, const cv::Point3f& b, cv::Point2f& midpoint)
{
    if (!isFiniteXY(a) || !isFiniteXY(b)) return false;
    midpoint.x = 0.5f * (a.x + b.x);
    midpoint.y = 0.5f * (a.y + b.y);
    return true;
}

float edgeAngleXY(const cv::Point3f& a, const cv::Point3f& b)
{
    if (!isFiniteXY(a) || !isFiniteXY(b)) return NAN;

    const float dx = b.x - a.x;
    const float dy = b.y - a.y;
    if (dx * dx + dy * dy <= 1e-12f) return NAN;
    return std::atan2(dy, dx);
}

float computeRobustOrientation2D(const cv::Point2f box2f[4], const std::vector<cv::Point3f>& corners3d)
{
    if (corners3d.size() < 4) return NAN;

    const float edge01_len2_img =
        (box2f[1].x - box2f[0].x) * (box2f[1].x - box2f[0].x) +
        (box2f[1].y - box2f[0].y) * (box2f[1].y - box2f[0].y);
    const float edge12_len2_img =
        (box2f[2].x - box2f[1].x) * (box2f[2].x - box2f[1].x) +
        (box2f[2].y - box2f[1].y) * (box2f[2].y - box2f[1].y);

    int short_edge_a0 = 0;
    int short_edge_a1 = 1;
    int short_edge_b0 = 2;
    int short_edge_b1 = 3;
    int long_edge_0 = 1;
    int long_edge_1 = 2;

    if (edge01_len2_img >= edge12_len2_img) {
        // Long axis runs parallel to edges 0-1 and 2-3.
        short_edge_a0 = 1;
        short_edge_a1 = 2;
        short_edge_b0 = 3;
        short_edge_b1 = 0;
        long_edge_0 = 0;
        long_edge_1 = 1;
    }

    cv::Point2f mid_a;
    cv::Point2f mid_b;
    if (computeMidpointXY(corners3d[short_edge_a0], corners3d[short_edge_a1], mid_a) &&
        computeMidpointXY(corners3d[short_edge_b0], corners3d[short_edge_b1], mid_b)) {
        const float axis_dx = mid_b.x - mid_a.x;
        const float axis_dy = mid_b.y - mid_a.y;
        if (axis_dx * axis_dx + axis_dy * axis_dy > 1e-12f) {
            return normalizeOrientationHalfTurn(std::atan2(axis_dy, axis_dx));
        }
    }

    const float fallback_angle = edgeAngleXY(corners3d[long_edge_0], corners3d[long_edge_1]);
    return normalizeOrientationHalfTurn(fallback_angle);
}

float computeEdgeLengthMm(const cv::Point3f& a, const cv::Point3f& b)
{
    if (!std::isfinite(a.x) || !std::isfinite(a.y) || !std::isfinite(a.z) ||
        !std::isfinite(b.x) || !std::isfinite(b.y) || !std::isfinite(b.z)) {
        return NAN;
    }

    const float dx = a.x - b.x;
    const float dy = a.y - b.y;
    const float dz = a.z - b.z;
    return std::sqrt(dx * dx + dy * dy + dz * dz) * 1000.0f;
}

#endif // CAMERA_STATIC_HPP
