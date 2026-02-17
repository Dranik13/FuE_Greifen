# Default *-config.cmake file created by ros-industrial-cmake-boilerplate

set(industrial_calibration_analysis_FOUND ON)
set(industrial_calibration_analysis_LIBRARIES)

# Targets
list(APPEND industrial_calibration_analysis_LIBRARIES industrial_calibration::industrial_calibration_analysis)

# Dependencies
include(CMakeFindDependencyMacro)
find_dependency(industrial_calibration COMPONENTS optimizations)

# Targets
include("${CMAKE_CURRENT_LIST_DIR}/analysis-targets.cmake")
