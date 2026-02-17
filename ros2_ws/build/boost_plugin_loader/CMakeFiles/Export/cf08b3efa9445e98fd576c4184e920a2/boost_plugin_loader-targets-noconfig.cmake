#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "boost_plugin_loader::boost_plugin_loader" for configuration ""
set_property(TARGET boost_plugin_loader::boost_plugin_loader APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(boost_plugin_loader::boost_plugin_loader PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libboost_plugin_loader.so"
  IMPORTED_SONAME_NOCONFIG "libboost_plugin_loader.so"
  )

list(APPEND _cmake_import_check_targets boost_plugin_loader::boost_plugin_loader )
list(APPEND _cmake_import_check_files_for_boost_plugin_loader::boost_plugin_loader "${_IMPORT_PREFIX}/lib/libboost_plugin_loader.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
