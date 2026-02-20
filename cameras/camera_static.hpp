#ifndef CAMERA_READER_1_H
#define CAMERA_READER_1_H

#include "camera_reader_base.hpp"
#include <chrono>

/**
 * StaticCamera: Kamera am Förderband
 * - Erkennt Objekte auf Förderband
 * - Filtert nach Z > 60 mm
 * - Aktualisiert bestehende Objekte in Liste
 */
class StaticCamera : public BaseCameraReader {
public:
    explicit StaticCamera(const std::string& config_file = "config.yml");

private:
    void processFrames() override;
    
    // Frame skipping: process only every 3rd frame
    int frame_skip_counter_ = 0;
    static constexpr int FRAME_SKIP = 5;
    
    // Velocity filtering: exponential moving average (alpha = smoothing factor 0..1)
    float filtered_velocity_y_ = 0.0f;
    static constexpr float VEL_FILTER_ALPHA = 0.3f;  // 0.3 = 30% new, 70% old
    
    // FPS tracking
    int frame_count_ = 0;
    std::chrono::high_resolution_clock::time_point last_fps_time_;
};

#endif // CAMERA_READER_1_H
