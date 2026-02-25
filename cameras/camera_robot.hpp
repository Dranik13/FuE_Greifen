#ifndef CAMERA_ROBOT_HPP
#define CAMERA_ROBOT_HPP

#include "camera_reader_base.hpp"

/**
 * RobotCamera: Camera attached to endeffector
 * - Detects objects right in front of TCP to estimate grasping moment
 */
class RobotCamera : public BaseCameraReader {
public:
    explicit RobotCamera(const std::string& config_file = "config_cam_robot.yml");

private:
    void processFrames() override;
    bool receiveStaticObject(Object3D& out_obj);

    zmq::context_t sub_context_{1};
    zmq::socket_t sub_socket_{sub_context_, zmq::socket_type::sub};
};

#endif // CAMERA_ROBOT_HPP
