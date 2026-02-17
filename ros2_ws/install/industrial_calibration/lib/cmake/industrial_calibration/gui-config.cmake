# Default *-config.cmake file created by ros-industrial-cmake-boilerplate

set(industrial_calibration_gui_FOUND ON)
set(industrial_calibration_gui_LIBRARIES)

# Targets
list(APPEND industrial_calibration_gui_LIBRARIES industrial_calibration::industrial_calibration_gui)

# Dependencies
include(CMakeFindDependencyMacro)
find_dependency(industrial_calibration COMPONENTS analysis target_finders_opencv)
find_dependency(Qt5 REQUIRED COMPONENTS Widgets)
find_dependency(boost_plugin_loader)

# Targets
include("${CMAKE_CURRENT_LIST_DIR}/gui-targets.cmake")
