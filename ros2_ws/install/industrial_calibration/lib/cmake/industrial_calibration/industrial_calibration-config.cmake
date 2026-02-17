# Default *-config.cmake file created by ros-industrial-cmake-boilerplate


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was industrial_calibration-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

####################################################################################

set(industrial_calibration_FOUND ON)

# These variables are needed so catkin packages can be located. 
if (EXISTS "/home/tetripick/UR10_Pick_ws/ros2_ws/install/ros_industrial_cmake_boilerplate/include")
  set(industrial_calibration_INCLUDE_DIRS "/home/tetripick/UR10_Pick_ws/ros2_ws/install/ros_industrial_cmake_boilerplate/include")
else()
  set(industrial_calibration_INCLUDE_DIRS)
endif()
set(industrial_calibration_LIBRARIES)

# Components
set(industrial_calibration_SUPPORTED_COMPONENTS core optimizations analysis target_finders_opencv gui examples)
if (NOT industrial_calibration_FIND_COMPONENTS)
  foreach(component ${industrial_calibration_SUPPORTED_COMPONENTS})
    include(${CMAKE_CURRENT_LIST_DIR}/${component}-config.cmake)
  endforeach()

  set(industrial_calibration_LIBRARIES)
  foreach(component ${industrial_calibration_SUPPORTED_COMPONENTS})
    list(APPEND industrial_calibration_LIBRARIES ${industrial_calibration_${component}_LIBRARIES})
  endforeach()
else()
  foreach(component ${industrial_calibration_FIND_COMPONENTS})
    if(NOT component IN_LIST industrial_calibration_SUPPORTED_COMPONENTS)
      set(industrial_calibration_${component}_FOUND OFF)
      set(industrial_calibration_${component}_NOT_FOUND_MESSAGE "Unsupported component")
      if (industrial_calibration_FIND_REQUIRED_${component})
        message(FATAL_ERROR "Project ${PROJECT_NAME}, failed to find required component ${component} for package industrial_calibration. Supported components are: ${industrial_calibration_SUPPORTED_COMPONENTS}")
      endif()
    else()
      include(${CMAKE_CURRENT_LIST_DIR}/${component}-config.cmake)
    endif()
  endforeach()

  set(industrial_calibration_LIBRARIES)
  foreach(component ${industrial_calibration_FIND_COMPONENTS})
    if(component IN_LIST industrial_calibration_SUPPORTED_COMPONENTS)
      list(APPEND industrial_calibration_LIBRARIES ${industrial_calibration_${component}_LIBRARIES})
    endif()
  endforeach()
endif()

