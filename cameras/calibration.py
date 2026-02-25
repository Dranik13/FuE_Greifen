import pyrealsense2 as rs
import numpy as np
import cv2
from pupil_apriltags import Detector

# =============================
# USER PARAMETERS
# =============================

TAG_SIZE = 0.027        # Meter
TAGS_X = 5
TAGS_Y = 7
TAG_SPACING = 0.003     # Meter Abstand zwischen Tags

# =============================
# RealSense Setup
# =============================

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
profile = pipeline.start(config)

color_stream = profile.get_stream(rs.stream.color).as_video_stream_profile()
intr = color_stream.get_intrinsics()

camera_matrix = np.array([
    [intr.fx, 0, intr.ppx],
    [0, intr.fy, intr.ppy],
    [0, 0, 1]
])

dist_coeffs = np.zeros((4,1))  # L515 ist praktisch verzerrungsfrei

# =============================
# AprilTag Detector
# =============================

at_detector = Detector(
    families='tag36h11',
    nthreads=4,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1
)

print("Board flach auf das Laufband legen.")
print("Drücke 'c' zum Berechnen.")

rvec_final = None
tvec_final = None

while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    image = np.asanyarray(color_frame.get_data())
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    results = at_detector.detect(
        gray,
        estimate_tag_pose=True,
        camera_params=[intr.fx, intr.fy, intr.ppx, intr.ppy],
        tag_size=TAG_SIZE
    )

    for r in results:
        # Achsen zeichnen
        R = r.pose_R
        t = r.pose_t

        rvec, _ = cv2.Rodrigues(R)
        cv2.drawFrameAxes(image, camera_matrix, dist_coeffs, rvec, t, 0.05)

        rvec_final = rvec
        tvec_final = t

    cv2.imshow("AprilTag Calibration", image)
    key = cv2.waitKey(1)

    if key == ord('c') and rvec_final is not None:
        break

pipeline.stop()
cv2.destroyAllWindows()

# =============================
# Transformation berechnen
# =============================

R, _ = cv2.Rodrigues(rvec_final)

T_cam_to_board = np.eye(4)
T_cam_to_board[0:3, 0:3] = R
T_cam_to_board[0:3, 3] = tvec_final.flatten()

print("\n===== Transformation Kamera → Laufband =====")
print(T_cam_to_board)

np.save("T_cam_to_treadmill.npy", T_cam_to_board)
print("Matrix gespeichert.")