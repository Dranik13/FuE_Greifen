import cv2
import cv2.aruco as aruco
import numpy as np
from scipy.spatial.transform import Rotation as R

# ==========================================
# 1. HARDCODED KALIBRIERUNGSDATEN (Greifer-Kamera)
# ==========================================
t_cam_mount = np.array([0.1087, -0.03436, -0.05987])
q_cam_mount = [0.0003631, 0.01987, 0.716, 0.6978]

T_flange_camG = np.eye(4)
T_flange_camG[:3, :3] = R.from_quat(q_cam_mount).as_matrix()
T_flange_camG[:3, 3] = t_cam_mount

# ==========================================
# 2. ### DEINE WERTE HIER EINTRAGEN ###
# ==========================================

# A. Deine 4 Bild-Paare
bild_paare = [
    (
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/robot_cam_Color.png", 
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/Pic_static_cam_Color.png" 
    ),
    (
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/robot_cam1_Color.png", 
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/Pic_static_cam_1_Color.png"
    ),
    (
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/robot_cam2_Color.png", 
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/Pic_static_cam_2_Color.png"
    ),
    (
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/robot_cam3_Color.png", 
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/Pic_static_cam_3_Color.png"
    ),
    (
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/robot_cam4_Color.png", 
        "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/Pic_static_cam_4_Color.png"
    )
]

# B. Roboterpose beim Auslösen
robot_x = 0.84111  
robot_y = -0.65372  
robot_z = 0.4725
robot_rx = 0.038  
robot_ry = -3.151  
robot_rz = 0.003  

# ==============================================================================
# 3. GETRENNTE KAMERA-MATRIZEN (Mittelpunkt bei 360 korrigiert!)
# ==============================================================================
# Matrix für die GREIFER-Kamera (D435i)
camera_matrix_G = np.array([
    [920.0, 0, 640.0],  
    [0, 920.0, 360.0],
    [0, 0, 1]
], dtype=float)

# Matrix für die STATISCHE Kamera (L515)
camera_matrix_S = np.array([
    [914.0, 0, 640.0],  
    [0, 914.0, 360.0],
    [0, 0, 1]
], dtype=float)

dist_coeffs = np.zeros((4,1))
marker_length = 0.027  
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# ==========================================
# 4. HILFSFUNKTIONEN
# ==========================================
def get_transform_from_image(image_path, cam_matrix, marker_id_to_find=0):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Bild {image_path} nicht gefunden!")
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv_version = cv2.__version__
    
    v_major = int(cv_version.split('.')[0])
    v_minor = int(cv_version.split('.')[1])
    
    if v_major >= 4 and v_minor >= 7:
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    else:
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    if ids is not None and marker_id_to_find in ids:
        idx = np.where(ids == marker_id_to_find)[0][0]
        
        half_l = marker_length / 2.0
        obj_points = np.array([
            [-half_l,  half_l, 0],
            [ half_l,  half_l, 0],
            [ half_l, -half_l, 0],
            [-half_l, -half_l, 0]
        ], dtype=np.float32)
        
        img_points = corners[idx][0]
        cam_mat_f32 = np.array(cam_matrix, dtype=np.float32)
        dist_f32 = np.array(dist_coeffs, dtype=np.float32)
        
        success, rvec, tvec = cv2.solvePnP(obj_points, img_points, cam_mat_f32, dist_f32)
        
        if not success:
            raise ValueError("Pose konnte nicht berechnet werden.")
            
        T_cam_board = np.eye(4)
        T_cam_board[:3, :3], _ = cv2.Rodrigues(rvec)
        T_cam_board[:3, 3] = tvec.flatten()
        return T_cam_board
    else:
        raise ValueError(f"Marker {marker_id_to_find} im Bild {image_path} nicht gefunden!")

# ==========================================
# 5. DIE MATHEMATIK & SCHLEIFE
# ==========================================
print("Starte Multi-Kalibrierung mit getrennten Kamera-Profilen...")

alle_translations = []
alle_quaternions = []

T_base_flange = np.eye(4)
T_base_flange[:3, :3] = R.from_rotvec([robot_rx, robot_ry, robot_rz]).as_matrix()
T_base_flange[:3, 3] = [robot_x, robot_y, robot_z]

for i, (pfad_greifer, pfad_statisch) in enumerate(bild_paare):
    print(f"\n--- BILD-PAAR {i+1} ---")
    try:
        T_camG_board = get_transform_from_image(pfad_greifer, camera_matrix_G)
        T_base_board = T_base_flange @ T_flange_camG @ T_camG_board
        
        T_camS_board = get_transform_from_image(pfad_statisch, camera_matrix_S)
        T_base_camS = T_base_board @ np.linalg.inv(T_camS_board)
        
        rotations_euler = R.from_matrix(T_base_camS[:3, :3]).as_euler('xyz', degrees=True)
        
        print(f"X: {T_base_camS[0,3]:.4f} m | Y: {T_base_camS[1,3]:.4f} m | Z: {T_base_camS[2,3]:.4f} m")
        print(f"Roll: {rotations_euler[0]:.2f}° | Pitch: {rotations_euler[1]:.2f}° | Yaw: {rotations_euler[2]:.2f}°")
        
        alle_translations.append(T_base_camS[:3, 3])
        alle_quaternions.append(R.from_matrix(T_base_camS[:3, :3]).as_quat())
        
    except Exception as e:
        print(f"FEHLER bei Paar {i+1} (wird übersprungen): {e}")

# ==========================================
# 6. DER FINALE DURCHSCHNITT
# ==========================================
print("\n" + "="*50)
print("      FINALE KALIBRIERUNGS-WERTE (DURCHSCHNITT)")
print("="*50)

if len(alle_translations) > 0:
    avg_translation = np.mean(alle_translations, axis=0)
    avg_rotation = R.from_quat(alle_quaternions).mean()
    avg_euler = avg_rotation.as_euler('xyz', degrees=True)
    
    print(f"X-Position: {avg_translation[0]:.4f} m")
    print(f"Y-Position: {avg_translation[1]:.4f} m")
    print(f"Z-Position: {avg_translation[2]:.4f} m")
    print("-" * 50)
    print(f"Verdrehung um X (Roll):  {avg_euler[0]:.2f} Grad")
    print(f"Verdrehung um Y (Pitch): {avg_euler[1]:.2f} Grad")
    print(f"Verdrehung um Z (Yaw):   {avg_euler[2]:.2f} Grad   <--- Dein X/Y-Greifwinkel")
    print("="*50 + "\n")
else:
    print("Es konnten keine Bilder erfolgreich ausgewertet werden. Überprüfe die Pfade!")