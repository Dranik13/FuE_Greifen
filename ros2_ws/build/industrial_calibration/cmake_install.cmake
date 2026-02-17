# Install script for directory: /home/tetripick/UR10_Pick_ws/ros2_ws/src/industrial_calibration

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/tetripick/UR10_Pick_ws/ros2_ws/install/industrial_calibration")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "industrial_calibration" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/industrial_calibration" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/industrial_calibration/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "industrial_calibration" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/industrial_calibration-config.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "industrial_calibration" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/industrial_calibration-config-version.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "industrial_calibration" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/share/ament_index/resource_index/packages/industrial_calibration")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "industrial_calibration" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/industrial_calibration/hook" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/share/industrial_calibration/hook/ament_prefix_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "industrial_calibration" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/industrial_calibration/hook" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/share/industrial_calibration/hook/ros_package_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "industrial_calibration" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/industrial_calibration/hook" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/share/industrial_calibration/hook/python_path.dsv")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/core/cmake_install.cmake")
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/optimizations/cmake_install.cmake")
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/analysis/cmake_install.cmake")
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/target_finders/cmake_install.cmake")
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/cmake_install.cmake")
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/examples/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
