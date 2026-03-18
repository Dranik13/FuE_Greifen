#ifndef TRACKER_HPP
#define TRACKER_HPP

#include <opencv2/opencv.hpp>
#include <vector>
#include "Object3D.hpp"

/*
* Nearest-neighbor 3D tracker working directly with Object3D.
* Stores only tracking metadata (id, timestamps, missed frames).
* Positions and velocities are updated directly in Object3D references.
*/
class Tracker {
public:
    Tracker();

    // Update tracks with detections at given timestamp (seconds).
    // Fills in vy (y-direction velocity) and speed in each detection.
    // Objects only move along conveyor belt (y-direction).
    // Returns y-component of average velocity across all tracked objects.
    float update(std::vector<Object3D>& detections, double timestamp);

    // Set fallback velocity for prediction of temporarily invisible objects.
    void setPredictionVelocity(float vy_mm_s) { prediction_velocity_y_ = vy_mm_s; }

    // Current active tracks as object states (includes predicted invisible ones).
    std::vector<Object3D> getActiveObjects() const;
    
    // Get current averaged y-velocity
    float getAverageVelocity() const { return avg_velocity_y_; }

    // Parameters
    float max_match_distance_mm = 300.0f;
    float min_tracked_y_mm = -10000.0f;       // Objects removed when y falls below this (outside velocity region)
    float max_tracked_y_mm = 10000.0f;
    int max_missed_in_region = 3;           // Max missed frames while in velocity region before deletion
    float velocity_region_y_min = -350.0f;  // Trusted detection region boundaries
    float velocity_region_y_max = 170.0f;

private:
    struct Track {
        Object3D object;
        double last_ts;
        int missed;
        int age;
    };

    struct Candidate {
        Object3D object;
        double detected_ts;
    };

    std::vector<Track> tracks_;
    std::vector<Candidate> candidates_;
    int next_id_ = 1;
    float avg_velocity_y_ = 0.0f;  // Average y-velocity across all tracked objects
    float prediction_velocity_y_ = 0.0f;
};

#endif // TRACKER_HPP
