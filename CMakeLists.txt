cmake_minimum_required(VERSION 3.16)

project(UR10_Pick LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Find dependencies
find_package(OpenCV REQUIRED)
find_package(PkgConfig REQUIRED)
find_package(Protobuf REQUIRED)

pkg_check_modules(REALSR realsense2 QUIET)
pkg_check_modules(ZMQ REQUIRED libzmq)

# Copy config files
configure_file(${CMAKE_SOURCE_DIR}/cameras/config_cam_static.yml ${CMAKE_BINARY_DIR}/config_cam_static.yml COPYONLY)
if(EXISTS ${CMAKE_SOURCE_DIR}/cameras/config_cam_robot.yml)
  configure_file(${CMAKE_SOURCE_DIR}/cameras/config_cam_robot.yml ${CMAKE_BINARY_DIR}/config_cam_robot.yml COPYONLY)
endif()

if (REALSR_FOUND)
  message(STATUS "Found librealsense2 via pkg-config")
  include_directories(${REALSR_INCLUDE_DIRS})
  link_directories(${REALSR_LIBRARY_DIRS})
  set(REALSR_LIBS ${REALSR_LIBRARIES})
else()
  message(WARNING "librealsense2 not found via pkg-config; try installing librealsense2-dev or provide a CMake config")
  set(REALSR_LIBS "")
endif()

# ============ Shared Camera Library ============
add_library(camera_base SHARED
  cameras/camera_reader_base.cpp
  cameras/camera_static.cpp
  cameras/camera_robot.cpp
  cameras/tracker.cpp
  zeroMQ/objects_3D.pb.cc
)

target_include_directories(camera_base PUBLIC
  ${OpenCV_INCLUDE_DIRS}
  ${CMAKE_CURRENT_SOURCE_DIR}
  ${ZMQ_INCLUDE_DIRS}
  ${CMAKE_CURRENT_SOURCE_DIR}/zeroMQ)

target_link_libraries(camera_base PUBLIC
  ${OpenCV_LIBS}
  ${REALSR_LIBS}
  protobuf::libprotobuf
  ${ZMQ_LIBRARIES})

# ============ CameraReader Executables ============
# Static Camera Reader
add_executable(camera_static
  cameras/camera_static_main.cpp
)
target_link_libraries(camera_static PRIVATE camera_base)

# Camera Reader 2 (fixed camera)
add_executable(camera_robot
  cameras/camera_robot_main.cpp
)
target_link_libraries(camera_robot PRIVATE camera_base)

# # Backward compatibility: camera_reader alias
# add_executable(camera_reader
#   cameras/camera_reader_main.cpp
# )
# target_link_libraries(camera_reader PRIVATE camera_base)

# ============ ZeroMQ Message Receiver ============
# add_executable(msg_receiver 
#   zeroMQ/msg_receiver.cpp
#   zeroMQ/objects_3D.pb.cc)

# target_include_directories(msg_receiver PRIVATE 
#                           ${OpenCV_INCLUDE_DIRS} 
#                           ${CMAKE_CURRENT_SOURCE_DIR}
#                           ${ZMQ_INCLUDE_DIRS}
#                           ${CMAKE_CURRENT_SOURCE_DIR}/zeroMQ)
# target_link_libraries(msg_receiver PRIVATE 
#                       ${OpenCV_LIBS} 
#                       ${REALSR_LIBS}
#                       protobuf::libprotobuf
#                       ${ZMQ_LIBRARIES})

# # ============ Install Targets ============
# install(TARGETS camera_static camera_robot msg_receiver DESTINATION bin)