import os
import time
import rtde_receive
import pyrealsense2 as rs
import numpy as np
import cv2

# --------------------
# EINSTELLUNGEN
# --------------------
UR_IP = "192.168.96.221"

BASE_PATH = "/home/tetripick/UR10_Pick_ws/ros2_ws/src"
POSE_DIR = os.path.join(BASE_PATH, "poses")
IMAGE_DIR = os.path.join(BASE_PATH, "images")

os.makedirs(POSE_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# --------------------
# UR ROBOT VERBINDUNG
# --------------------
rtde_r = rtde_receive.RTDEReceiveInterface(UR_IP)

# --------------------
# REALSENSE PIPELINE
# --------------------
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)
time.sleep(1)   # kurze Zeit für Auto-Exposure

# --------------------
# DATEINAMEN ERMITTELN
# --------------------
def get_next_index():
    poses = [f for f in os.listdir(POSE_DIR) if f.startswith("pose_")]
    if not poses:
        return 1
    nums = [int(p.split("_")[1].split(".")[0]) for p in poses]
    return max(nums) + 1

idx = get_next_index()

pose_file = os.path.join(POSE_DIR, f"pose_{idx:03d}.txt")
image_file = os.path.join(IMAGE_DIR, f"image_{idx:03d}.png")

# --------------------
# POSE VOM ROBOTER HOLEN
# --------------------
#pose = rtde_r.getActualTCPPose()
pose = rtde_r.getActualToolFlangePose()

# speichern
with open(pose_file, "w") as f:
    f.write(" ".join(map(str, pose)))

print("Gespeicherte Pose:", pose)
print("→", pose_file)

# --------------------
# BILD AUFNEHMEN
# --------------------
frames = pipeline.wait_for_frames()
color_frame = frames.get_color_frame()
color_image = np.asanyarray(color_frame.get_data())

# speichern
cv2.imwrite(image_file, color_image)
print("Gespeichertes Bild:", image_file)

# --------------------
# CLEANUP
# --------------------
pipeline.stop()
print("\nFertig: Pose + Bild wurden synchron aufgenommen.\n")

