import cv2
import cv2.aruco as aruco
import numpy as np
from scipy.spatial.transform import Rotation as R

# ==========================================
# 1. HARDCODED KALIBRIERUNGSDATEN (Greifer-Kamera)
# ==========================================
# Werte aus deiner Datei: camera_mount_to_camera
t_cam_mount = np.array([0.1087, -0.03436, -0.05987])
# Scipy erwartet Quaternions im Format [x, y, z, w]! (In deiner Datei ist w zuerst)
q_cam_mount = [0.0003631, 0.01987, 0.716, 0.6978]

# Transformationsmatrix: Flansch -> Greifer-Kamera
T_flange_camG = np.eye(4)
T_flange_camG[:3, :3] = R.from_quat(q_cam_mount).as_matrix()
T_flange_camG[:3, 3] = t_cam_mount

# ==========================================
# 2. ### DEINE WERTE HIER EINTRAGEN ###
# ==========================================

# A. Roboterpose beim Auslösen von 'bild_greifer.png' (in Metern und Bogenmaß/Radiant!)
# Wenn dein Roboter Grad anzeigt, musst du es in Radiant umrechnen (Grad * pi / 180)
robot_x = 0.8098  # Beispielwert
robot_y = -0.57945  # Beispielwert
robot_z = -0.14937  # Beispielwert
robot_rx = 2.195  # Beispielwert (Roll)
robot_ry = -2.224  # Beispielwert (Pitch)
robot_rz = 0.003  # Beispielwert (Yaw)

# B. Kamera Intrinsics (Brennweite und Bildmitte aus deiner Realsense)
# Format: [[fx, 0, cx], [0, fy, cy], [0, 0, 1]]
camera_matrix = np.array([
    [324.703, 0, 598.554],  # ERSETZEN!
    [0, 241.537, 598.359],  # ERSETZEN!
    [0, 0, 1]
], dtype=float)
dist_coeffs = np.zeros((4,1)) # Wir gehen von rektifizierten/verzerrungsfreien Bildern aus

# C. Größe eines einzelnen ArUco-Markers in Metern (z.B. 3cm = 0.03)
marker_length = 0.027  # ERSETZEN!

# D. Welches ArUco Dictionary hast du gedruckt? (Oft DICT_4X4_50 oder DICT_5X5_250)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# ==========================================
# 3. HILFSFUNKTIONEN (Segfault-sicher)
# ==========================================
def get_transform_from_image(image_path, marker_id_to_find=0):
    print(f"\n--> [DEBUG] Lade Bild: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Bild {image_path} nicht gefunden!")
        
    print("--> [DEBUG] Bild geladen. Konvertiere zu Graustufen...")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv_version = cv2.__version__
    print(f"--> [DEBUG] OpenCV Version erkannt: {cv_version}")
    print("--> [DEBUG] Suche nach Markern...")
    
    # Versionsabhängiger, sicherer Aufruf
    v_major = int(cv_version.split('.')[0])
    v_minor = int(cv_version.split('.')[1])
    
    if v_major >= 4 and v_minor >= 7:
        # Für neuere OpenCV Versionen (ab 4.7)
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    else:
        # Für ältere OpenCV Versionen (ROS Foxy/Humble Standard)
        parameters = aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    print(f"--> [DEBUG] Erkannte Marker-IDs: {ids}")
    
    if ids is not None and marker_id_to_find in ids:
        idx = np.where(ids == marker_id_to_find)[0][0]
        print(f"--> [DEBUG] Marker {marker_id_to_find} gefunden. Berechne 3D-Pose...")
        
        half_l = marker_length / 2.0
        obj_points = np.array([
            [-half_l,  half_l, 0],
            [ half_l,  half_l, 0],
            [ half_l, -half_l, 0],
            [-half_l, -half_l, 0]
        ], dtype=np.float32)
        
        img_points = corners[idx][0]
        cam_mat_f32 = np.array(camera_matrix, dtype=np.float32)
        dist_f32 = np.array(dist_coeffs, dtype=np.float32)
        
        success, rvec, tvec = cv2.solvePnP(obj_points, img_points, cam_mat_f32, dist_f32)
        
        if not success:
            raise ValueError("Pose konnte nicht berechnet werden.")
            
        print("--> [DEBUG] Pose erfolgreich berechnet!")
        T_cam_board = np.eye(4)
        T_cam_board[:3, :3], _ = cv2.Rodrigues(rvec)
        T_cam_board[:3, 3] = tvec.flatten()
        return T_cam_board
    else:
        raise ValueError(f"Marker {marker_id_to_find} im Bild {image_path} nicht gefunden!")
    

# ==========================================
# 4. DIE MATHEMATIK (DIE "BRÜCKE")
# ==========================================
try:
    print("Analysiere Bilder...")
    
    # 1. T_CamG_Board (Wo ist das Board im Bild der Greiferkamera?)
    T_camG_board = get_transform_from_image("/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/robot_cam_Color.png")
    
    # 2. T_Base_Flange (Roboterpose als Matrix)
    T_base_flange = np.eye(4)
    T_base_flange[:3, :3] = R.from_rotvec([robot_rx, robot_ry, robot_rz]).as_matrix()
    T_base_flange[:3, 3] = [robot_x, robot_y, robot_z]
    
    # 3. Absolute Position des Boards in der Welt (Roboterbasis) berechnen
    # T_Base_Board = T_Base_Flange * T_Flange_CamG * T_CamG_Board
    T_base_board = T_base_flange @ T_flange_camG @ T_camG_board
    
    # 4. T_CamS_Board (Wo ist das Board im Bild der statischen Kamera?)
    T_camS_board = get_transform_from_image("/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/Pic_static_cam_Color.png")
    
    # 5. Position der statischen Kamera berechnen
    # Wir stellen um: T_Base_Board = T_Base_CamS * T_CamS_Board  ==>  T_Base_CamS = T_Base_Board * Inverse(T_CamS_Board)
    T_base_camS = T_base_board @ np.linalg.inv(T_camS_board)
    
    # 6. Rotationswinkel (Yaw) extrahieren
    rotations_euler = R.from_matrix(T_base_camS[:3, :3]).as_euler('xyz', degrees=True)
    
    print("\n--- ERGEBNIS ---")
    print(f"X-Position: {T_base_camS[0,3]:.4f} m")
    print(f"Y-Position: {T_base_camS[1,3]:.4f} m")
    print(f"Z-Position: {T_base_camS[2,3]:.4f} m")
    print(f"Verdrehung um X (Roll):  {rotations_euler[0]:.2f} Grad")
    print(f"Verdrehung um Y (Pitch): {rotations_euler[1]:.2f} Grad")
    print(f"Verdrehung um Z (Yaw):   {rotations_euler[2]:.2f} Grad   <--- DAS IST DEIN GESUCHTER WERT!")

except Exception as e:
    print(f"\nFEHLER: {e}")