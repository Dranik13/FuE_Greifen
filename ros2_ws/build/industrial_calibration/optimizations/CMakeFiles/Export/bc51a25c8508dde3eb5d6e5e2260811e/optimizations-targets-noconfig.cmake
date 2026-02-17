#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "industrial_calibration::industrial_calibration_optimizations" for configuration ""
set_property(TARGET industrial_calibration::industrial_calibration_optimizations APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(industrial_calibration::industrial_calibration_optimizations PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libindustrial_calibration_optimizations.so"
  IMPORTED_SONAME_NOCONFIG "libindustrial_calibration_optimizations.so"
  )

list(APPEND _cmake_import_check_targets industrial_calibration::industrial_calibration_optimizations )
list(APPEND _cmake_import_check_files_for_industrial_calibration::industrial_calibration_optimizations "${_IMPORT_PREFIX}/lib/libindustrial_calibration_optimizations.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
