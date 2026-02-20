#include "camera_static.hpp"

/**
 * Main executable for Camera Reader 1 (conveyor belt camera)
 * Usage: ./camera_static
 */
int main() 
{
    std::cout << "Starting static camera reader \n";
    StaticCamera reader("config_cam_static.yml");

    if (!reader.isRunning()) {
        std::cerr << "Static camera reader failed to initialize.\n";
        return 1;
    }

    std::cout << "Static camera reader running. Press 'q' or ESC to exit.\n";
    reader.spin();

    std::cout << "Static camera reader stopped.\n";
    return 0;
}
