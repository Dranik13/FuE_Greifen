#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "industrial_calibration::industrial_calibration_gui" for configuration ""
set_property(TARGET industrial_calibration::industrial_calibration_gui APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(industrial_calibration::industrial_calibration_gui PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libindustrial_calibration_gui.so"
  IMPORTED_SONAME_NOCONFIG "libindustrial_calibration_gui.so"
  )

list(APPEND _cmake_import_check_targets industrial_calibration::industrial_calibration_gui )
list(APPEND _cmake_import_check_files_for_industrial_calibration::industrial_calibration_gui "${_IMPORT_PREFIX}/lib/libindustrial_calibration_gui.so" )

# Import target "industrial_calibration::industrial_calibration_extrinsic_hand_eye_calibration_app" for configuration ""
set_property(TARGET industrial_calibration::industrial_calibration_extrinsic_hand_eye_calibration_app APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(industrial_calibration::industrial_calibration_extrinsic_hand_eye_calibration_app PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app"
  )

list(APPEND _cmake_import_check_targets industrial_calibration::industrial_calibration_extrinsic_hand_eye_calibration_app )
list(APPEND _cmake_import_check_files_for_industrial_calibration::industrial_calibration_extrinsic_hand_eye_calibration_app "${_IMPORT_PREFIX}/bin/industrial_calibration_extrinsic_hand_eye_calibration_app" )

# Import target "industrial_calibration::industrial_calibration_camera_intrinsic_calibration_app" for configuration ""
set_property(TARGET industrial_calibration::industrial_calibration_camera_intrinsic_calibration_app APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(industrial_calibration::industrial_calibration_camera_intrinsic_calibration_app PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app"
  )

list(APPEND _cmake_import_check_targets industrial_calibration::industrial_calibration_camera_intrinsic_calibration_app )
list(APPEND _cmake_import_check_files_for_industrial_calibration::industrial_calibration_camera_intrinsic_calibration_app "${_IMPORT_PREFIX}/bin/industrial_calibration_camera_intrinsic_calibration_app" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
