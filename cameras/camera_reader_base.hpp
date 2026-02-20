#ifndef BASE_CAMERA_READER_H
#define BASE_CAMERA_READER_H

#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <zmq.hpp>

#include "objects_3D.pb.h"
#include "tracker.hpp"
#include "Object3D.hpp"

struct Object3D;
/* (The actual struct is now in Object3D.hpp, included above)
 * Abstract base class for camera readers.
 * Handles RealSense device initialization, ZMQ communication, and frame capture.
 * Subclasses implement custom processFrames() logic.
 */
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
    cv::Point2i ref_pt_;
    cv::Point3f ref_pt_3d_;
    float pos_delta_;  
    float orientation_delta_;

    // RealSense
    rs2::pipeline pipeline_;
    std::string serial_;
    rs2::context ctx_;

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

#endif // BASE_CAMERA_READER_H
