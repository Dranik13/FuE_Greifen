# Default *-config.cmake file created by ros-industrial-cmake-boilerplate

set(industrial_calibration_optimizations_FOUND ON)
set(industrial_calibration_optimizations_LIBRARIES)

# Targets
list(APPEND industrial_calibration_optimizations_LIBRARIES industrial_calibration::industrial_calibration_optimizations)

# Dependencies
include(CMakeFindDependencyMacro)
find_dependency(Ceres)
find_dependency(industrial_calibration COMPONENTS core)

# Targets
include("${CMAKE_CURRENT_LIST_DIR}/optimizations-targets.cmake")
