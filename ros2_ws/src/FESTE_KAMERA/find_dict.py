import cv2
import cv2.aruco as aruco

# 1. Pfad anpassen (JPG oder PNG?)
image_path = "/home/tetripick/UR10_Pick_ws/ros2_ws/src/FESTE_KAMERA/robot_cam_Color.png" 

img = cv2.imread(image_path)
if img is None:
    print("Fehler: Bild nicht gefunden. Pfad prüfen!")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Liste aller gängigen Dictionaries in ROS/OpenCV
ARUCO_DICTS = {
    "DICT_4X4_50": aruco.DICT_4X4_50,
    "DICT_4X4_250": aruco.DICT_4X4_250,
    "DICT_5X5_50": aruco.DICT_5X5_50,
    "DICT_5X5_250": aruco.DICT_5X5_250,
    "DICT_6X6_250": aruco.DICT_6X6_250,
    "DICT_7X7_1000": aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": aruco.DICT_APRILTAG_36h11 # Sehr oft in ROS genutzt!
}

print("Starte automatische Suche nach dem richtigen Dictionary...")
gefunden = False

for name, dict_id in ARUCO_DICTS.items():
    # OpenCV Versions-Kompatibilität abfangen
    try:
        aruco_dict = aruco.getPredefinedDictionary(dict_id)
    except AttributeError:
        aruco_dict = aruco.Dictionary_get(dict_id)
        
    try:
        parameters = aruco.DetectorParameters()
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, _ = detector.detectMarkers(gray)
    except AttributeError:
        parameters = aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Wenn er etwas findet...
    if ids is not None and len(ids) > 0:
        print("\n" + "="*50)
        print(f"!!! TREFFER !!!")
        print(f"Dein Board benutzt: {name}")
        print(f"Es wurden {len(ids)} Marker im Bild gefunden.")
        print(f"Verfügbare IDs auf dem Papier: {sorted(ids.flatten())}")
        print("="*50 + "\n")
        gefunden = True
        break

if not gefunden:
    print("Mist! Kein bekanntes Standard-Dictionary hat funktioniert.")