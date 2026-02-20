#include "camera_robot.hpp"

/**
 * Main executable for Camera Reader (robot camera)
 * Usage: ./camera_robot
 */
int main() 
{
    std::cout << "Starting CameraReader (Robot Camera)\n";
    RobotCamera reader("config_cam_robot.yml");

    if (!reader.isRunning()) {
        std::cerr << "CameraReader failed to initialize.\n";
        return 1;
    }

    std::cout << "CameraReader running. Press 'q' or ESC to exit.\n";
    reader.spin();

    std::cout << "CameraReader stopped.\n";
    return 0;
}
