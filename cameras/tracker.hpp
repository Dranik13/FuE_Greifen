#ifndef TRACKER_HPP
#define TRACKER_HPP

#include <opencv2/opencv.hpp>
#include <vector>
#include "Object3D.hpp"

// Simple nearest-neighbor 3D tracker working directly with Object3D.
// Stores only tracking metadata (id, timestamps, missed frames).
// Positions and velocities are updated directly in Object3D references.
class Tracker {
public:
    Tracker();

    // Update tracks with detections at given timestamp (seconds).
    // Fills in vy (y-direction velocity) and speed in each detection.
    // Objects only move along conveyor belt (y-direction).
    // Returns y-component of average velocity across all tracked objects.
    float update(std::vector<Object3D>& detections, double timestamp);
    
    // Get current averaged y-velocity
    float getAverageVelocity() const { return avg_velocity_y_; }

    // Parameters
    float max_match_distance_mm = 100.0f;
    int max_missed_frames = 5;

private:
    struct Track {
        int id;
        cv::Point3f last_pos;  // For velocity calculation
        double last_ts;
        int missed;
        int age;
    };

    std::vector<Track> tracks_;
    int next_id_ = 1;
    float avg_velocity_y_ = 0.0f;  // Average y-velocity across all tracked objects
};

#endif // TRACKER_HPP
