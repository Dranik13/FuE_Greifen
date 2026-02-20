#include "tracker.hpp"
#include <cmath>

namespace {
float resolve_prediction_vy(const Object3D& state, float fallback_vy) {
    if (std::isfinite(state.vy) && std::abs(state.vy) > 1e-6f) {
        return state.vy;
    }
    return fallback_vy;
}
}

Tracker::Tracker() {}

float Tracker::update(std::vector<Object3D>& detections, double timestamp)
{
    int n = (int)detections.size();
    
    std::vector<int> matched_track_index(n, -1);
    const size_t original_track_count = tracks_.size();
    std::vector<bool> track_used(original_track_count, false);

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
        for (size_t j = 0; j < original_track_count; ++j) {
            if (track_used[j]) continue;
            const auto& track = tracks_[j];

            double dt = timestamp - track.last_ts;
            if (dt < 0.0) dt = 0.0;
            float pred_vy = resolve_prediction_vy(track.state, prediction_velocity_y_);

            float pred_x = track.state.x;
            float pred_y = track.state.y + pred_vy * static_cast<float>(dt);
            float pred_z = track.state.z;

            double dx = d.x - pred_x;
            double dy = d.y - pred_y;
            double dz = d.z - pred_z;
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
        if (tj != -1 && tj < (int)original_track_count) {
            Track& track = tracks_[tj];
            double dt = timestamp - track.last_ts;
            
            // Calculate y-velocity and store in Object3D
            if (dt > 1e-6 && dt < 10.0) {
                float vy = (detections[i].y - track.state.y) / (float)dt;
                
                if (vy >= 10){
                    detections[i].vy = vy;
                    sum_vy += vy;
                    vel_count++;
                }

            } else {
                detections[i].vy = resolve_prediction_vy(track.state, prediction_velocity_y_);
            }
            
            track.state = detections[i];
            track.last_ts = timestamp;
            track.missed = 0;
            track.age++;
        }
    }

    // Match detections also with candidates (to promote they to full tracks)
    std::vector<bool> candidate_matched(candidates_.size(), false);

    for (int i = 0; i < n; ++i) {
        if (matched_track_index[i] != -1) continue;  // Already matched with a track
        
        if (!std::isfinite(detections[i].x) || !std::isfinite(detections[i].y) || 
            !std::isfinite(detections[i].z)) {
            continue;
        }

        const cv::Point3f d(detections[i].x, detections[i].y, detections[i].z);
        float best_dist = max_match_distance_mm + 1.0f;
        int best_c = -1;

        for (size_t c = 0; c < candidates_.size(); ++c) {
            const auto& cand = candidates_[c];
            double dx = d.x - cand.state.x;
            double dy = d.y - cand.state.y;
            double dz = d.z - cand.state.z;
            float dist = std::sqrt(dx*dx + dy*dy + dz*dz);

            if (dist < best_dist) {
                best_dist = dist;
                best_c = (int)c;
            }
        }

        if (best_c != -1 && best_dist <= max_match_distance_mm) {
            // Candidate confirmed! Promote to full track
            const auto& cand = candidates_[best_c];
            Track newt;
            newt.id = next_id_++;
            newt.state = detections[i];
            newt.last_ts = timestamp;
            newt.missed = 0;
            newt.age = 1;
            tracks_.push_back(newt);
            
            candidate_matched[best_c] = true;
            detections[i].vy = 0.0f;  // New tracks have zero velocity initially
        }
    }

    // Remove matched candidates
    std::vector<Candidate> new_candidates;
    for (size_t c = 0; c < candidates_.size(); ++c) {
        if (!candidate_matched[c]) {
            new_candidates.push_back(candidates_[c]);
        }
    }
    candidates_ = new_candidates;

    // Create candidates for still-unmatched detections
    for (int i = 0; i < n; ++i) {
        if (matched_track_index[i] == -1 &&
            std::isfinite(detections[i].x) && std::isfinite(detections[i].y) && 
            std::isfinite(detections[i].z)) {

            Candidate cand;
            cand.state = detections[i];
            cand.detected_ts = timestamp;
            candidates_.push_back(cand);
            detections[i].vy = 0.0f;
        }
    }

    // Predict and mark unmatched existing tracks as missed
    for (size_t j = 0; j < original_track_count; ++j) {
        if (track_used[j]) continue;

        Track& track = tracks_[j];
        double dt = timestamp - track.last_ts;
        if (dt < 0.0) dt = 0.0;

        float pred_vy = resolve_prediction_vy(track.state, prediction_velocity_y_);
        track.state.y += pred_vy * static_cast<float>(dt);
        track.state.vy = pred_vy;
        track.last_ts = timestamp;
        track.missed++;
    }

    // Increase missed count for unused tracks
    // Only iterate through the original tracks (before pushback added new ones)

    // Remove tracks based on dual conditions:
    // 1. Inside velocity_region: delete if missed too many frames (false positives)
    // 2. Outside velocity_region: delete only if y < min_tracked_y_mm (allow longer prediction)
    std::vector<Track> new_tracks;
    for (size_t j = 0; j < tracks_.size(); ++j) {
        const Track& t = tracks_[j];
        bool in_region = (t.state.y >= velocity_region_y_min && t.state.y <= velocity_region_y_max);
        
        // bool keep = false;
        // if (in_region) {
        //     // Inside trusted region: strict - delete if too many misses
        //     keep = (t.missed <= max_missed_in_region);
        // } else {
        //     // Outside region: lenient - keep until y threshold
        //     keep = (t.state.y >= min_tracked_y_mm);
        // }

        bool keep = (t.state.y >= min_tracked_y_mm && t.state.y <= max_tracked_y_mm);
        
        if (keep) {
            new_tracks.push_back(t);
        }
    }
    tracks_ = new_tracks;  // Use assignment instead of swap

    // Compute average y-velocity across all tracked objects
    if (vel_count > 0) {
        avg_velocity_y_ = sum_vy / vel_count;
    }

    return avg_velocity_y_;
}

std::vector<Object3D> Tracker::getActiveObjects() const
{
    std::vector<Object3D> objects;
    objects.reserve(tracks_.size());
    for (const auto& track : tracks_) {
        objects.push_back(track.state);
    }
    return objects;
}
