# Install script for directory: /home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/tetripick/UR10_Pick_ws/ros2_ws/install/ros_industrial_cmake_boilerplate")
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

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/create_debian_changelog.py")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/clang_tidy_tools.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/cmake_tools.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/code_coverage.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/cpack_tools.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/cppcheck_tools.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/extract_package_metadata.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/iwyu_tools.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/ros_industrial_cmake_boilerplate/cmake/sanitizers.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/ros_industrial_cmake_boilerplate/ros_industrial_cmake_boilerplate-config.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ros_industrial_cmake_boilerplate" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/ros_industrial_cmake_boilerplate/ros_industrial_cmake_boilerplate-config-version.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/ros_industrial_cmake_boilerplate/share/ament_index/resource_index/packages/ros_industrial_cmake_boilerplate")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_industrial_cmake_boilerplate/hook" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/ros_industrial_cmake_boilerplate/share/ros_industrial_cmake_boilerplate/hook/ament_prefix_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_industrial_cmake_boilerplate/hook" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/ros_industrial_cmake_boilerplate/share/ros_industrial_cmake_boilerplate/hook/ros_package_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "ros_industrial_cmake_boilerplate" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ros_industrial_cmake_boilerplate/hook" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/ros_industrial_cmake_boilerplate/share/ros_industrial_cmake_boilerplate/hook/python_path.dsv")
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/tetripick/UR10_Pick_ws/ros2_ws/build/ros_industrial_cmake_boilerplate/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
