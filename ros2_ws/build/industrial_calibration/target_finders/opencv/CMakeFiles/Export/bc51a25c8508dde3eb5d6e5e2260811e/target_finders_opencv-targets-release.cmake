#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "industrial_calibration::industrial_calibration_target_finders_opencv" for configuration "Release"
set_property(TARGET industrial_calibration::industrial_calibration_target_finders_opencv APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(industrial_calibration::industrial_calibration_target_finders_opencv PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libindustrial_calibration_target_finders_opencv.so"
  IMPORTED_SONAME_RELEASE "libindustrial_calibration_target_finders_opencv.so"
  )

list(APPEND _cmake_import_check_targets industrial_calibration::industrial_calibration_target_finders_opencv )
list(APPEND _cmake_import_check_files_for_industrial_calibration::industrial_calibration_target_finders_opencv "${_IMPORT_PREFIX}/lib/libindustrial_calibration_target_finders_opencv.so" )

# Import target "industrial_calibration::industrial_calibration_plugins_opencv" for configuration "Release"
set_property(TARGET industrial_calibration::industrial_calibration_plugins_opencv APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(industrial_calibration::industrial_calibration_plugins_opencv PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libindustrial_calibration_plugins_opencv.so"
  IMPORTED_SONAME_RELEASE "libindustrial_calibration_plugins_opencv.so"
  )

list(APPEND _cmake_import_check_targets industrial_calibration::industrial_calibration_plugins_opencv )
list(APPEND _cmake_import_check_files_for_industrial_calibration::industrial_calibration_plugins_opencv "${_IMPORT_PREFIX}/lib/libindustrial_calibration_plugins_opencv.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
