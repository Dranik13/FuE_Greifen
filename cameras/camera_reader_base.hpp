#ifndef BASE_CAMERA_READER_HPP
#define BASE_CAMERA_READER_HPP

#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <zmq.hpp>
#include <yaml-cpp/yaml.h>
#include <cmath>

#include "objects_3D.pb.h"
#include "tracker.hpp"
#include "Object3D.hpp"

struct ExtrinsicCalibration {
    double x;
    double y;
    double z;
    double roll_deg;
    double pitch_deg;
    double yaw_deg;
};

class BaseCameraReader {
public:
    BaseCameraReader(const std::string& config_file);
    virtual ~BaseCameraReader() = default;

    void spin() {
        while (true) {
            processFrames();
            int key = cv::waitKey(1);
            if (key == 'q' || key == 27) break;
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
        }
    }

    const std::vector<Object3D>& getObjects() const {
        return obj_list_;
    }

    bool isRunning() const {
        return running_;
    }

protected:
    // Subclasses override this for custom frame processing
    virtual void processFrames() = 0;

    // Helper methods accessible to subclasses
    cv::Point3f computeCenter(const std::vector<cv::Point3f>& corners);
    float computeOrientation2D(const std::vector<cv::Point3f>& corners);
    bool checkIfObjIsInList(const Object3D& new_obj, size_t& id);
    void sendObjList();
    void sendCoordinates(float &x, float &y, float &z);

    // Configuration and state
    bool running_ = false;
    bool debug_;
    int zmq_port_ = 5555;
    cv::Rect roi_;
    uint16_t conveyor_z_dist_;
    uint16_t min_obj_height_;
    uint16_t z_offset_;
    std::vector<double> canny_thresh_;
    std::string camera_serial_config_;
    std::string serial_number_ = "";
    float pos_delta_;  
    float orientation_delta_;
    // Max expected object height in mm (for filtering)
    float max_obj_height_mm_;
    // Minimum contour area to be considered an object (in pixels)
    int min_contour_area_;
    // Final affine calibration in robot frame (mm): out = scale * raw + offset
    float x_scale_ = 1.0f;
    float y_scale_ = 1.0f;
    float x_offset_mm_ = 0.0f;
    float y_offset_mm_ = 0.0f;

    // RealSense
    rs2::pipeline pipeline_;
    std::string serial_;
    rs2::context ctx_;
    rs2::pipeline_profile profile_;
    ExtrinsicCalibration extrinsic_calibration_; 
    cv::Matx44d transform_cam_to_robot_;

    // Object list and output
    std::vector<Object3D> obj_list_;
    zmq::context_t context_;
    zmq::socket_t socket_;
    // Lightweight tracker for detections -> velocities
    Tracker tracker_;

    // Config loading (can be overridden if needed)
    virtual void loadConfig(const std::string& config_file);

private:
    void initializeRealSense();
};

#endif // BASE_CAMERA_READER_HPP
