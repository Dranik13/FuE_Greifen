# Default *-config.cmake file created by ros-industrial-cmake-boilerplate

set(industrial_calibration_examples_FOUND ON)
set(industrial_calibration_examples_LIBRARIES)

# Targets

# Dependencies
include(CMakeFindDependencyMacro)
find_dependency(industrial_calibration COMPONENTS analysis target_finders_opencv)

# Targets
include("${CMAKE_CURRENT_LIST_DIR}/examples-targets.cmake")
