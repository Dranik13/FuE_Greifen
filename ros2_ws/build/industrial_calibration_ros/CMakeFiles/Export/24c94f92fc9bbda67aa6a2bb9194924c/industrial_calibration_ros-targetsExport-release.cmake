#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "industrial_calibration_ros::industrial_calibration_ros_extrinsic_hand_eye_calibration_panel" for configuration "Release"
set_property(TARGET industrial_calibration_ros::industrial_calibration_ros_extrinsic_hand_eye_calibration_panel APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(industrial_calibration_ros::industrial_calibration_ros_extrinsic_hand_eye_calibration_panel PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libindustrial_calibration_ros_extrinsic_hand_eye_calibration_panel.so"
  IMPORTED_SONAME_RELEASE "libindustrial_calibration_ros_extrinsic_hand_eye_calibration_panel.so"
  )

list(APPEND _cmake_import_check_targets industrial_calibration_ros::industrial_calibration_ros_extrinsic_hand_eye_calibration_panel )
list(APPEND _cmake_import_check_files_for_industrial_calibration_ros::industrial_calibration_ros_extrinsic_hand_eye_calibration_panel "${_IMPORT_PREFIX}/lib/libindustrial_calibration_ros_extrinsic_hand_eye_calibration_panel.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
