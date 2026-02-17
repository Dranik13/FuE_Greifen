# import pyrealsense2 as rs
# import numpy as np

# # -----------------------------------------------------------
# # 1) HIER NUR DIE PIXELKOORDINATEN EINTRAGEN
# # -----------------------------------------------------------
# u = 572      # Beispiel: x-Pixel
# v = 272      # Beispiel: y-Pixel

# # -----------------------------------------------------------
# # 2) Eye-in-Hand Transformation (Kamera -> TCP)
# # -----------------------------------------------------------
# R_cam_tcp = np.array([
#     [-0.01408259,  0.86766931,  0.4969423 ],
#     [ 0.90467739,  0.22272849, -0.36325037],
#     [-0.42586441,  0.44445696, -0.7880974 ]
# ])

# t_cam_tcp = np.array([[-0.0796954],
#                       [-0.77019151],
#                       [ 0.28354273]])

# # -----------------------------------------------------------
# # Realsense Initialisieren
# # -----------------------------------------------------------
# pipeline = rs.pipeline()
# config = rs.config()
# config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

# profile = pipeline.start(config)

# # -----------------------------------------------------------
# # INTRINSICS AUTOMATISCH AUS DER KAMERA LADEN
# # -----------------------------------------------------------
# depth_stream = profile.get_stream(rs.stream.depth)           # Stream-Profil
# intr = depth_stream.as_video_stream_profile().get_intrinsics()

# fx = intr.fx
# fy = intr.fy
# cx = intr.ppx
# cy = intr.ppy

# print("Benutzte Kamera-Intrinsics:")
# print("fx:", fx)
# print("fy:", fy)
# print("cx:", cx)
# print("cy:", cy)

# # Frame holen
# frames = pipeline.wait_for_frames()
# depth_frame = frames.get_depth_frame()

# if not depth_frame:
#     raise RuntimeError("Kein Depth Frame erhalten")

# # Depth an Pixelkoordinate holen
# depth = depth_frame.get_distance(u, v)

# if depth == 0:
#     raise RuntimeError("Tiefe = 0 an diesem Pixel. Wähle einen anderen Punkt.")

# print("Gemessene Tiefe:", depth, "m")

# # -----------------------------------------------------------
# # 3D-Punkt in Kamera-Koordinaten rekonstruieren
# # -----------------------------------------------------------
# X_cam = (u - cx) * depth / fx
# Y_cam = (v - cy) * depth / fy
# Z_cam = depth

# P_cam = np.array([[X_cam], [Y_cam], [Z_cam]])

# print("3D-Punkt in Kamera-Koordinaten:")
# print(P_cam)

# # -----------------------------------------------------------
# # Kamera -> TCP Transformation anwenden
# # -----------------------------------------------------------
# P_tcp = R_cam_tcp @ P_cam + t_cam_tcp

# print("\n3D Punkt in TCP-Koordinaten:")
# print(P_tcp)

# # -----------------------------------------------------------
# # Pose zum manuellen Anfahren ausgeben
# # -----------------------------------------------------------
# print("\nRoboterpose manuell anfahren (X,Y,Z in Meter):")
# print("X:", float(P_tcp[0]))
# print("Y:", float(P_tcp[1]))
# print("Z:", float(P_tcp[2]))

# pipeline.stop()


import cv2
import numpy as np
import rtde_receive

# ================================
# UR Robot
# ================================
UR_IP = "192.168.96.221"
rtde_r = rtde_receive.RTDEReceiveInterface(UR_IP)

# ================================
# Kamera-Kalibrierung (DEINE WERTE!)
# ================================
K = np.array([
    [605.10428164,   0.0,         309.15481453],
    [0.0,           604.90180922, 248.99819762],
    [0.0,           0.0,           1.0]
])

dist = np.array([
    0.03518305,
    0.44417025,
   -0.00231133,
   -0.00157409,
   -1.82891902
])

# ================================
# Kamera → Tool (DEIN ERGEBNIS)
# ================================
T_cam2tool = np.array([
    [ 1.17607539e-01, -9.93029333e-01,  7.82373142e-03,  1.01747436e-01],
    [ 9.93059741e-01,  1.17596667e-01, -1.83704718e-03, -1.40417821e-02],
    [ 9.04196998e-04,  7.98548330e-03,  9.99967707e-01, -7.62957787e-02],
    [ 0.0,             0.0,             0.0,             1.0]
])

T_tool2cam = np.linalg.inv(T_cam2tool)

# ================================
# Klötzchen-Geometrie (Meter!)
# ================================
BLOCK_X = 0.05
BLOCK_Y = 0.05
BLOCK_Z = 0.0

# 4 Ecken der Oberseite im Block-KS
objp = np.array([
    [-BLOCK_X/2, -BLOCK_Y/2,  BLOCK_Z],
    [ BLOCK_X/2, -BLOCK_Y/2,  BLOCK_Z],
    [ BLOCK_X/2,  BLOCK_Y/2,  BLOCK_Z],
    [-BLOCK_X/2,  BLOCK_Y/2,  BLOCK_Z],
], dtype=np.float32)

# ================================
# Bild laden
# ================================
img = cv2.imread("/home/tetripick/UR10_Pick_ws/ros2_ws/src/images/image_021.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ================================
# 2D Punkte manuell anklicken
# ================================
img_points = []

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        img_points.append([x, y])
        cv2.circle(img, (x, y), 5, (0,255,0), -1)
        cv2.imshow("image", img)

cv2.imshow("image", img)
cv2.setMouseCallback("image", click)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_points = np.array(img_points, dtype=np.float32)

if len(img_points) != 4:
    raise RuntimeError("Es müssen genau 4 Punkte angeklickt werden")

# ================================
# solvePnP: Block → Kamera
# ================================
success, rvec, tvec = cv2.solvePnP(
    objp,
    img_points,
    K,
    dist
)

R_cam_block, _ = cv2.Rodrigues(rvec)

T_cam_block = np.eye(4)
T_cam_block[:3, :3] = R_cam_block
T_cam_block[:3, 3]  = tvec.reshape(3)

# ================================
# Base → Tool (live)
# ================================
pose = rtde_r.getActualTCPPose()

def ur_pose_to_T(p):
    Rm, _ = cv2.Rodrigues(np.array(p[3:]))
    T = np.eye(4)
    T[:3, :3] = Rm
    T[:3, 3]  = p[:3]
    return T

T_base_tool = ur_pose_to_T(pose)

# ================================
# Base → Block
# ================================
T_base_block = T_base_tool @ T_tool2cam @ T_cam_block

print("\n=== Klötzchen im Base-Frame ===")
print("Position [m]:", T_base_block[:3, 3])
print("Rotation:\n", T_base_block[:3, :3])
