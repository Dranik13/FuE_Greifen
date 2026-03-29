# schräg liegende Bauteile (45 Grad) greifen

import time
from turtle import width
import yaml
import math
from pathlib import Path
from camera_to_robot_transform import CameraToRobotTransformer
import camera_sub
import save_pos

def _load_camera_mount_to_camera_distance():
    """Lädt den physikalischen Versatz zwischen Kamera und Greifer aus der Kalibrierung."""
    pose_file = Path(__file__).with_name("Calibration_results_final.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    camera_mount_to_camera = data.get("camera_mount_to_camera", {})
    camera_to_mount_distance = camera_mount_to_camera.get("x")
    
    if isinstance(camera_to_mount_distance, list):
        return float(camera_to_mount_distance[0])
    try:
        return float(camera_to_mount_distance)
    except (TypeError, ValueError):
        raise ValueError("[follow_handler] Ungültiger Wert in Calibration_results_final.yaml")

# Physischer Versatz der Kamera am Greifer (Y-Richtung auf dem Band)
distance_to_camera = _load_camera_mount_to_camera_distance()

def wait_for_object_data(transformer: CameraToRobotTransformer, sub: camera_sub.CameraSubscriber, debug=False, object_speed=0.1):
    """
    Wartet auf die präzisen X/Y-Koordinaten von Kamera 2 (Port 5556).
    """
    timeout = int(1 / object_speed) if object_speed > 0 else 10
    start_time = time.time()
    
    while True:
        obj = sub.receive_5556(100)
        if (time.time() - start_time) > timeout:
            if debug: print("[follow_handler] Timeout: Kein Objekt auf Port 5556.")
            return None, None, None
            
        if obj is None:
            continue
        
        # Umrechnung Pixel/mm zu Meter
        pos_x = obj['x'] / 1000.0
        pos_y = obj['y'] / 1000.0
        
        # Winkel (Wird hier ignoriert, da wir 'orientation' vom idle_handler nutzen)
        pos_theta = obj.get('orientation', 0.0) 

        # --- NEU: Breite und Länge auslesen ---
        #width = obj.get('width', 1.0)
        #length = obj.get('length', 1.0)

        return pos_x, pos_y, pos_theta

def object_waiting(rtde_c, rtde_r, object_speed=0.1, robot_speed=0.8, robot_acceleration=0.5, orientation=0.0, width=1.0, length=1.0, debug=False):
    """
    Richtet den Greifer schräg zum Bauteil aus und wartet auf den Griff-Zeitpunkt.
    """
    sub = camera_sub.CameraSubscriber(address='tcp://localhost:5556', topic="coordinates")
    transformer = CameraToRobotTransformer(rtde_receiver=rtde_r)

    # 1. Aktuelle X/Y Feindaten holen
    pos_x, pos_y, _ = wait_for_object_data(transformer, sub, debug=debug, object_speed=object_speed)
    
    if pos_y is None:
        return False

    # Timing berechnen
    stop_time = (distance_to_camera + abs(pos_y)) / object_speed - 0.5
    start_time = time.time()

    # --- KORREKTUR FÜR DIE TOOL-ROTATION (WICHTIG!) ---
    
    # 2. Aktuelle Pose des Roboters holen
    actual_pose = rtde_r.getActualTCPPose()
    
    # 3. Basis-Ziel vorbereiten (nur X-Verschiebung korrigieren)
    base_target = list(actual_pose)
    base_target[0] -= (pos_x - 0.03) # Seitlicher Versatz zum Bauteil
    
    # 4. Tool-Rotation definieren
    max_side = max(width, length)
    min_side = min(width, length)
    aspect_ratio = (max_side / min_side) if min_side > 0 else 1.0
    
    if aspect_ratio < 1.25:
        # ES IST EIN QUADRAT (oder rund)
        # Ein Quadrat kann man an zwei verschiedenen Kanten greifen. 
        # Wir berechnen beide Wege:
        rot1 = -(orientation - math.radians(90))
        rot2 = -orientation
        
        # Wir zwingen den Roboter, den Winkel zu nehmen, der am nächsten an 0 ist.
        # Das verhindert den riesigen 90°-Ausraster!
        if abs(rot1) < abs(rot2):
            rad_theta = rot1
        else:
            rad_theta = rot2
            
        # Wenn das Quadrat nur minimal schief liegt (< 5 Grad Kamera-Zittern),
        # setzen wir die Drehung knallhart auf 0.
        if abs(rad_theta) < math.radians(5):
            rad_theta = 0.0
            
    else:
        # ES IST EIN LÄNGLICHES BAUTEIL (Quader)
        # Hier muss er bei quer liegenden Teilen zwingend 90° drehen.
        rad_theta = -(orientation - math.radians(90))
    
    tool_rotation = [0, 0, 0, 0, 0, rad_theta]

    # 5. Transformation berechnen (Pose Trans)
    # Kombiniert die Ziel-Pose im Raum mit der lokalen Drehung des Greifers.
    final_target = rtde_c.poseTrans(base_target, tool_rotation)

    if debug:
        grad_theta = math.degrees(orientation)
        print("-" * 50)
        print(f"[DEBUG ROTATION STRAT 2]")
        print(f" -> Winkel vom Idle: {grad_theta:.2f}°")
        print(f" -> Pose-Verschiebung X: {-(pos_x-0.03):.4f}m")
        print(f" -> Aktuelle Pose (Base): {actual_pose}")
        print(f" -> Finale Zielpose (Tool): {final_target}")
        print("-" * 50)

    # 6. Kombinierte Bewegung (Seitlich rücken + Drehen)
    if save_pos.is_save_position(final_target[:3]):
        rtde_c.moveL(final_target, robot_speed, robot_acceleration)
    else:
        if debug: print("[follow_handler] FEHLER: Zielpose außerhalb des Arbeitsraums!")

    # 7. Warten, bis Bauteil den Greifer erreicht
    while (time.time() - start_time) < stop_time:
        time.sleep(0.02)
        
    return True