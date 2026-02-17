# Install script for directory: /home/tetripick/UR10_Pick_ws/ros2_ws/src/industrial_calibration/gui

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

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/src/industrial_calibration/gui/include/")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "gui" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libindustrial_calibration_gui.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libindustrial_calibration_gui.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libindustrial_calibration_gui.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/libindustrial_calibration_gui.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libindustrial_calibration_gui.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libindustrial_calibration_gui.so")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libindustrial_calibration_gui.so"
         OLD_RPATH "/home/tetripick/UR10_Pick_ws/ros2_ws/install/boost_plugin_loader/lib:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/analysis:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/target_finders/opencv:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/optimizations:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/core:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libindustrial_calibration_gui.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "gui" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "gui" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/industrial_calibration_extrinsic_hand_eye_calibration_app")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app"
         OLD_RPATH "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui:/home/tetripick/UR10_Pick_ws/ros2_ws/install/boost_plugin_loader/lib:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/analysis:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/optimizations:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/target_finders/opencv:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/core:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "gui" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/industrial_calibration_camera_intrinsic_calibration_app")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app"
         OLD_RPATH "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui:/home/tetripick/UR10_Pick_ws/ros2_ws/install/boost_plugin_loader/lib:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/analysis:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/optimizations:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/target_finders/opencv:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/core:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "gui" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration/gui-targets.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration/gui-targets.cmake"
         "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/CMakeFiles/Export/bc51a25c8508dde3eb5d6e5e2260811e/gui-targets.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration/gui-targets-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration/gui-targets.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/CMakeFiles/Export/bc51a25c8508dde3eb5d6e5e2260811e/gui-targets.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/CMakeFiles/Export/bc51a25c8508dde3eb5d6e5e2260811e/gui-targets-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "gui" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/industrial_calibration" TYPE FILE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui-config.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_extrinsic_hand_eye_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_extrinsic_hand_eye_calibration_app")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_extrinsic_hand_eye_calibration_app"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration" TYPE EXECUTABLE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/industrial_calibration_extrinsic_hand_eye_calibration_app")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_extrinsic_hand_eye_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_extrinsic_hand_eye_calibration_app")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_extrinsic_hand_eye_calibration_app"
         OLD_RPATH "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui:/home/tetripick/UR10_Pick_ws/ros2_ws/install/boost_plugin_loader/lib:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/analysis:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/optimizations:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/target_finders/opencv:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/core:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_extrinsic_hand_eye_calibration_app")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/CMakeFiles/industrial_calibration_extrinsic_hand_eye_calibration_app.dir/install-cxx-module-bmi-Release.cmake" OPTIONAL)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_camera_intrinsic_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_camera_intrinsic_calibration_app")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_camera_intrinsic_calibration_app"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration" TYPE EXECUTABLE FILES "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/industrial_calibration_camera_intrinsic_calibration_app")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_camera_intrinsic_calibration_app" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_camera_intrinsic_calibration_app")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_camera_intrinsic_calibration_app"
         OLD_RPATH "/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui:/home/tetripick/UR10_Pick_ws/ros2_ws/install/boost_plugin_loader/lib:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/analysis:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/optimizations:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/target_finders/opencv:/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/core:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/industrial_calibration/industrial_calibration_camera_intrinsic_calibration_app")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/tetripick/UR10_Pick_ws/ros2_ws/build/industrial_calibration/gui/CMakeFiles/industrial_calibration_camera_intrinsic_calibration_app.dir/install-cxx-module-bmi-Release.cmake" OPTIONAL)
endif()

