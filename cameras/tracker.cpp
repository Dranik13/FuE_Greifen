#include "tracker.hpp"
#include <cmath>

Tracker::Tracker() {}

float Tracker::update(std::vector<Object3D>& detections, double timestamp)
{
    int n = (int)detections.size();
    
    // Early return if no detections
    if (n == 0) return avg_velocity_y_;
    
    std::vector<int> matched_track_index(n, -1);
    std::vector<bool> track_used(tracks_.size(), false);
    // Greedy nearest-neighbor matching
    for (int i = 0; i < n; ++i) {
        // Skip detections with invalid coordinates
        if (!std::isfinite(detections[i].x) || !std::isfinite(detections[i].y) || 
            !std::isfinite(detections[i].z)) {
            continue;
        }
        
        const cv::Point3f d(detections[i].x, detections[i].y, detections[i].z);
        float best_dist = max_match_distance_mm + 1.0f;
        int best_j = -1;
        for (size_t j = 0; j < tracks_.size(); ++j) {
            if (track_used[j]) continue;
            const auto& t = tracks_[j];
            double dx = d.x - t.last_pos.x;
            double dy = d.y - t.last_pos.y;
            double dz = d.z - t.last_pos.z;
            float dist = std::sqrt(dx*dx + dy*dy + dz*dz);
            if (dist < best_dist) {
                best_dist = dist;
                best_j = (int)j;
            }
        }
        if (best_j != -1 && best_dist <= max_match_distance_mm) {
            matched_track_index[i] = best_j;
            track_used[best_j] = true;
        }
    }

    // Update matched tracks and collect y-velocities
    float sum_vy = 0.0f;
    int vel_count = 0;

    for (int i = 0; i < n; ++i) {
        int tj = matched_track_index[i];
        if (tj != -1 && tj < (int)tracks_.size()) {
            Track& t = tracks_[tj];
            double dt = timestamp - t.last_ts;
            
            // Calculate y-velocity and store in Object3D
            if (dt > 1e-6 && dt < 10.0) {
                float vy = (detections[i].y - t.last_pos.y) / (float)dt;
                
                detections[i].vy = vy;
                detections[i].speed = std::abs(vy);  // speed = |vy|
                
                sum_vy += vy;
                vel_count++;
            }
            
            t.last_pos = cv::Point3f(detections[i].x, detections[i].y, detections[i].z);
            t.last_ts = timestamp;
            t.missed = 0;
            t.age++;
        }
    }

    // Create tracks for unmatched detections
    for (int i = 0; i < n; ++i) {
        if (matched_track_index[i] == -1 && 
            std::isfinite(detections[i].x) && std::isfinite(detections[i].y) && 
            std::isfinite(detections[i].z)) {
            Track newt;
            newt.id = next_id_++;
            newt.last_pos = cv::Point3f(detections[i].x, detections[i].y, detections[i].z);
            newt.last_ts = timestamp;
            newt.missed = 0;
            newt.age = 1;
            tracks_.push_back(newt);
            
            // New detections have zero velocity
            detections[i].vy = 0.0f;
            detections[i].speed = 0.0f;
        }
    }
    // Increase missed count for unused tracks
    // Only iterate through the original tracks (before pushback added new ones)
    for (size_t j = 0; j < track_used.size(); ++j) {
        if (track_used[j]) continue;
        if (j < tracks_.size()) {
            tracks_[j].missed++;
        }
    }
    // Remove stale tracks
    std::vector<Track> new_tracks;
    for (size_t j = 0; j < tracks_.size(); ++j) {
        if (tracks_[j].missed <= max_missed_frames) {
            new_tracks.push_back(tracks_[j]);
        }
    }
    tracks_ = new_tracks;  // Use assignment instead of swap

    // Compute average y-velocity across all tracked objects
    if (vel_count > 0) {
        avg_velocity_y_ = sum_vy / vel_count;
    }

    return avg_velocity_y_;
}
