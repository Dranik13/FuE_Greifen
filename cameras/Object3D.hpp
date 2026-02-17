#ifndef OBJECT3D_HPP
#define OBJECT3D_HPP

#include <string>

struct Object3D
{
    float x, y, z;
    float orientation;
    float width, length, height;
    std::string label;
    // Velocity in y-direction (mm/s) - only this matters for conveyor belt
    float vy = 0.0f;
    float speed = 0.0f;  // |vy| for convenience
};

#endif // OBJECT3D_HPP
