#Wir machen 2 in 1 im get_pose.py, das hier muss nicht mehr verwendet werden


import pyrealsense2 as rs
import cv2
import time

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

time.sleep(1)

frames = pipeline.wait_for_frames()
color_frame = frames.get_color_frame()

color_image = np.asanyarray(color_frame.get_data())

timestamp = int(time.time())
filename = f"/home/tetripick/UR10_Pick_ws/ros2_ws/src/images/image_{timestamp}.png"

cv2.imwrite(filename, color_image)
print("Gespeichert:", filename)

pipeline.stop()
