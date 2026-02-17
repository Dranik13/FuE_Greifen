# Default *-config.cmake file created by ros-industrial-cmake-boilerplate

set(industrial_calibration_core_FOUND ON)
set(industrial_calibration_core_LIBRARIES)

# Targets
list(APPEND industrial_calibration_core_LIBRARIES industrial_calibration::industrial_calibration_core)

# Dependencies
include(CMakeFindDependencyMacro)
find_dependency(Eigen3)
find_dependency(yaml-cpp)

# Targets
include("${CMAKE_CURRENT_LIST_DIR}/core-targets.cmake")
