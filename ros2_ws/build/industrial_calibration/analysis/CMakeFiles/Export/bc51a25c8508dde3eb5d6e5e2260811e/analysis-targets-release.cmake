#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "industrial_calibration::industrial_calibration_analysis" for configuration "Release"
set_property(TARGET industrial_calibration::industrial_calibration_analysis APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(industrial_calibration::industrial_calibration_analysis PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libindustrial_calibration_analysis.so"
  IMPORTED_SONAME_RELEASE "libindustrial_calibration_analysis.so"
  )

list(APPEND _cmake_import_check_targets industrial_calibration::industrial_calibration_analysis )
list(APPEND _cmake_import_check_files_for_industrial_calibration::industrial_calibration_analysis "${_IMPORT_PREFIX}/lib/libindustrial_calibration_analysis.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
