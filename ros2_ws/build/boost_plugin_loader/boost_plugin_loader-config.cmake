# Default *-config.cmake file created by ros-industrial-cmake-boilerplate


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was boost_plugin_loader-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

####################################################################################

set(boost_plugin_loader_FOUND ON)

# These variables are needed so catkin packages can be located. 
if (EXISTS "/home/tetripick/UR10_Pick_ws/ros2_ws/install/ros_industrial_cmake_boilerplate/include")
  set(boost_plugin_loader_INCLUDE_DIRS "/home/tetripick/UR10_Pick_ws/ros2_ws/install/ros_industrial_cmake_boilerplate/include")
else()
  set(boost_plugin_loader_INCLUDE_DIRS)
endif()
set(boost_plugin_loader_LIBRARIES)

# Targets
list(APPEND boost_plugin_loader_LIBRARIES boost_plugin_loader::boost_plugin_loader)

# Dependencies
include(CMakeFindDependencyMacro)
find_dependency(Boost REQUIRED COMPONENTS filesystem)

# Targets
include("${CMAKE_CURRENT_LIST_DIR}/boost_plugin_loader-targets.cmake")
