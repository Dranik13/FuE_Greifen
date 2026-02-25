#ifndef OBJECT3D_HPP
#define OBJECT3D_HPP

#include <string>

struct Object3D
{
    int id;
    std::string label;
    float x, y, z;
    float orientation;
    float width, length, height;
    // Velocity in y-direction (mm/s)
    float vy = 0.0f;
};

#endif // OBJECT3D_HPP
