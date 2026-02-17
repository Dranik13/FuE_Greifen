# #!/usr/bin/env python3
# import cv2
# import numpy as np
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import Image
# from cv_bridge import CvBridge

# class HandEyeCalib(Node):

#     def __init__(self):
#         super().__init__('hand_eye_calibration')
#         self.bridge = CvBridge()

#         self.subscription = self.create_subscription(
#             Image,
#             '/camera/color/image_raw',
#             self.image_callback,
#             10)

#         self.obj_points = []
#         self.img_points = []

#         self.pattern_size = (7, 5)  # Anzahl innerer Ecken (Beispiel)
#         self.square_size = 0.025    # 25 mm

#         # 3D-Koordinaten des Checkerboards vorbereiten
#         objp = np.zeros((np.prod(self.pattern_size), 3), np.float32)
#         objp[:, :2] = np.indices(self.pattern_size).T.reshape(-1, 2)
#         objp *= self.square_size
#         self.objp_template = objp

#     def image_callback(self, msg):
#         frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         found, corners = cv2.findChessboardCorners(gray, self.pattern_size)

#         if found:
#             self.img_points.append(corners)
#             self.obj_points.append(self.objp_template)
#             cv2.drawChessboardCorners(frame, self.pattern_size, corners, found)

#         cv2.imshow("image", frame)
#         cv2.waitKey(1)


# def main(args=None):
#     rclpy.init(args=args)
#     node = HandEyeCalib()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()


#!/usr/bin/env python3
import cv2
import numpy as np
import glob
import os
from pathlib import Path

# ==================================================
# Pfade
# ==================================================
BASE_PATH = "/home/tetripick/UR10_Pick_ws/ros2_ws/src"
IMAGE_DIR = os.path.join(BASE_PATH, "images")
POSE_DIR  = os.path.join(BASE_PATH, "poses")

# ==================================================
# Checkerboard-Parameter
# ==================================================
PATTERN_SIZE = (7, 5)     # innere Ecken
SQUARE_SIZE  = 0.03      # Meter

# ==================================================
# Objektpunkte (Checkerboard im Board-KS)
# ==================================================
objp = np.zeros((PATTERN_SIZE[0] * PATTERN_SIZE[1], 3), np.float32)
objp[:, :2] = np.indices(PATTERN_SIZE).T.reshape(-1, 2)
objp *= SQUARE_SIZE

# ==================================================
# Hilfsfunktion: UR Pose laden (Axis-Angle!)
# ==================================================
def load_ur_pose_txt(path):
    data = np.loadtxt(path)

    t = data[0:3]           # x, y, z
    rvec = data[3:6]        # rx, ry, rz (Axis-Angle)

    Rm, _ = cv2.Rodrigues(rvec)
    return Rm, t

# ==================================================
# Bilder einlesen + Checkerboard erkennen
# ==================================================
objpoints = []
imgpoints = []
valid_indices = []

images = sorted(glob.glob(os.path.join(IMAGE_DIR, "image_*.png")))

for img_path in images:
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    found, corners = cv2.findChessboardCorners(
        gray,
        PATTERN_SIZE,
        cv2.CALIB_CB_ADAPTIVE_THRESH +
        cv2.CALIB_CB_NORMALIZE_IMAGE
    )

    if not found:
        print(f"[WARN] Checkerboard nicht gefunden: {img_path}")
        continue

    corners_refined = cv2.cornerSubPix(
        gray,
        corners,
        (11, 11),
        (-1, -1),
        (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)
    )

    objpoints.append(objp)
    imgpoints.append(corners_refined)

    idx = Path(img_path).stem.split("_")[1]
    valid_indices.append(idx)

print(f"[INFO] Verwendete Bild-Pose-Paare: {len(objpoints)}")

# ==================================================
# 1) Kamerakalibrierung
# ==================================================
ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    None,
    None
)

print("\n=== Kameramatrix K ===")
print(K)
print("\n=== Distortion ===")
print(dist.ravel())

# ==================================================
# 2) Checkerboard → Kamera (solvePnP)
# ==================================================
R_target2cam = []
t_target2cam = []

for i in range(len(objpoints)):
    success, rvec, tvec = cv2.solvePnP(
        objpoints[i],
        imgpoints[i],
        K,
        dist
    )

    Rm, _ = cv2.Rodrigues(rvec)
    R_target2cam.append(Rm)
    t_target2cam.append(tvec.reshape(3))

# ==================================================
# 3) Tool → Base (UR Posen)
# ==================================================
R_gripper2base = []
t_gripper2base = []

for idx in valid_indices:
    pose_path = os.path.join(POSE_DIR, f"pose_{idx}.txt")

    Rm, t = load_ur_pose_txt(pose_path)

    R_gripper2base.append(Rm)
    t_gripper2base.append(t)

# ==================================================
# 4) Hand-Auge-Kalibrierung (UR → Kamera)
# ==================================================
R_cam2gripper, t_cam2gripper = cv2.calibrateHandEye(
    R_gripper2base,
    t_gripper2base,
    R_target2cam,
    t_target2cam,
    method=cv2.CALIB_HAND_EYE_TSAI
)

# ==================================================
# Ergebnis als homogene Matrix
# ==================================================
T_cam2tool = np.eye(4)
T_cam2tool[:3, :3] = R_cam2gripper
T_cam2tool[:3, 3] = t_cam2gripper.reshape(3)


print("\n=== Ergebnis: Kamera → Tool (TCP) ===")
print(T_cam2tool)
