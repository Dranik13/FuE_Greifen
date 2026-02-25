#include "camera_robot.hpp"

/**
 * Main executable for robot camera (camera overlooking robot arm)
 * Usage: ./camera_robot
 */
int main() 
{
    std::cout << "Starting robot camera reader \n";
    RobotCamera reader("config_cam_robot.yml");

    if (!reader.isRunning()) {
        std::cerr << "Robot camera reader failed to initialize.\n";
        return 1;
    }

    reader.spin();

    std::cout << "Robot camera reader stopped.\n";
    return 0;
}
