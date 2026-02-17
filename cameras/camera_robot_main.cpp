#include "camera_robot.hpp"

/**
 * Main executable for Camera Reader 2 (fixed camera)
 * Usage: ./camera_robot
 */
int main() 
{
    std::cout << "Starting CameraReader2 (Fixed Camera)\n";
    RobotCamera reader("config2.yml");

    if (!reader.isRunning()) {
        std::cerr << "CameraReader2 failed to initialize.\n";
        return 1;
    }

    std::cout << "CameraReader2 running. Press 'q' or ESC to exit.\n";
    reader.spin();

    std::cout << "CameraReader2 stopped.\n";
    return 0;
}
