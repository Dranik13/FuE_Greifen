#ifndef CAMERA_READER_2_H
#define CAMERA_READER_2_H

#include "camera_reader_base.hpp"

/**
 * RobotCamera: Camara attached to endeffector
 * - Implementiere hier eigene Logik für die zweite Kamera
 * - Z.B. andere Objekterkennung, andere Filter, andere Ausgabe
 */
class RobotCamera : public BaseCameraReader {
public:
    explicit RobotCamera(const std::string& config_file = "config2.yml");

private:
    void processFrames() override;
    bool receiveStaticObject(Object3D& out_obj);

    zmq::context_t sub_context_{1};
    zmq::socket_t sub_socket_{sub_context_, zmq::socket_type::sub};
};

#endif // CAMERA_READER_2_H
