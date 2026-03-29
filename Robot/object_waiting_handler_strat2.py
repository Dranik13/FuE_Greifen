# Greifstrategie 2: hinten am Fließband in geneigter Position warten

import time
import math
from camera_to_robot_transform import CameraToRobotTransformer
import camera_sub

# --- PHYSIKALISCHE KONSTANTEN ---
DISTANCE_TO_CAMERA = 0.1087  # Abstand Kamera-Gehäuse zu Greifer-Mitte (Y-Richtung)

def wait_for_object_data(transformer: CameraToRobotTransformer, sub: camera_sub.CameraSubscriber, debug=False, object_speed=0.1):
    """
    Wartet auf Objektdaten der Kamera, sammelt 5 Samples zur Glättung und merkt sich den Zeitstempel.
    """
    # --- RADIKALER PUFFER-FLUSH (Verhindert veraltete Daten) ---
    if debug:
        print("[object_waiting] Leere alten Daten-Puffer rigoros...")
    
    flushed_msgs = 0
    while True:
        junk = sub.receive_5556(1)
        if junk is None:
            break
        flushed_msgs += 1
        
    if debug:
        print(f"[object_waiting] Puffer geleert: {flushed_msgs} alte Frames verworfen.")
        
    safe_speed = object_speed if object_speed > 0.01 else 0.05
    timeout_sec = int(3.0 / safe_speed) 
    
    if debug:
        print(f"[object_waiting] Suche Bauteil (Timeout: {timeout_sec}s)...")
        
    start_time = time.time()
    
    samples_x = []
    latest_y = 0.0
    capture_time = 0.0
    
    # Sammle 5 Frames für einen stabilen Mittelwert (gegen Kamera-Zittern)
    while len(samples_x) < 5:
        objs = sub.receive_5556(100)
        
        if (time.time() - start_time) > timeout_sec:
            if debug:
                print("[object_waiting] FEHLER: Timeout!")
            return None, None, None
            
        if objs is None or len(objs) == 0:
            continue
            
        obj = objs[0] if isinstance(objs, list) else objs

        try:
            bx, by, bz = transformer.camera_point_to_base(obj['x'], obj['y'], obj['z'])
            samples_x.append(bx)
            latest_y = by
            capture_time = time.time() 
        except Exception as e:
            if debug:
                print(f"[object_waiting] Transformer-Fehler: {e}")
            continue

    avg_bx = sum(samples_x) / len(samples_x)
    return avg_bx, latest_y, capture_time


def object_waiting(rtde_c, rtde_r, object_speed=0.1, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    """
    Hauptfunktion: Berücksichtigt Linsen-Versatz (X), Neigungs-Versatz (Y) 
    und korrigiert perspektivische Fehler an den Rändern.
    """
    # --- HARDWARE-KONFIGURATION ---
    LINSEN_VERSATZ_X = 0.0     # Korrektur über MANUELLER_X_OFFSET
    BAUTEIL_HOEHE = 0.05       # 5 cm
    NEIGUNGS_WINKEL = 25.0     
    NEIGUNGS_RICHTUNG_Y = 1.0 

    X_MIN, X_MAX = -0.05, 1.05 
    TOLERANZ = 0.002           
    MANUELLER_X_OFFSET = -0.03  # Dein Grund-Offset für die Mitte
    
    # --- DYNAMISCHE RAND-KORREKTUR (FEINTUNING) ---
    BILD_MITTE_X = 0.839255        # <-- HIER DEINEN MITTIGEN bx_avg WERT EINTRAGEN
    Y_DRIFT_FAKTOR = 0.0      # Korrigiert Timing-Fehler links/rechts
    X_DRIFT_FAKTOR = 0.0      # Korrigiert Spur-Fehler (Backen-Schleifen) links/rechts
    # -----------------------------------------

    sub = camera_sub.CameraSubscriber(address='tcp://localhost:5556', topic="coordinates")
    transformer = CameraToRobotTransformer(rtde_receiver=rtde_r)
    
    # 1. Objektdaten empfangen
    bx, by, capture_time = wait_for_object_data(transformer, sub, debug=debug, object_speed=object_speed)
    if bx is None or by is None: return False

    # 2. Aktuelle Position des Roboters
    actual_TCP_pose = rtde_r.getActualTCPPose()
    current_x = actual_TCP_pose[0]

    # 3. Abweichung von der Mitte berechnen
    abweichung_x = bx - BILD_MITTE_X

    # --- BERECHNUNG DER KORREKTUREN ---
    winkel_rad = math.radians(NEIGUNGS_WINKEL)
    
    # Y-Korrektur (Basis + dynamischer Drift für Rand-Positionen)
    y_basis_korrektur = BAUTEIL_HOEHE * math.tan(winkel_rad) * NEIGUNGS_RICHTUNG_Y
    y_versatz_neigung = y_basis_korrektur + (abweichung_x * Y_DRIFT_FAKTOR)
    
    # X-Korrektur (Manuell + dynamischer Drift gegen Parallaxenfehler)
    dynamischer_x_offset = MANUELLER_X_OFFSET - (abweichung_x * X_DRIFT_FAKTOR)

    # --- ZIELKOORDINATEN BERECHNEN ---
    target_x = max(X_MIN, min(bx + dynamischer_x_offset, X_MAX))
    by_korrigiert = by - y_versatz_neigung

    if debug:
        print("-" * 50)
        print(f"!!! DEBUG: bx_avg={bx:.4f} | Abweichung={abweichung_x:.4f}")
        print(f"!!! TARGET: X={target_x:.4f} | Y_Corr={y_versatz_neigung:.4f}")

    # --- SPURKORREKTUR (X) ---
    if abs(target_x - current_x) > TOLERANZ:
        target_pose = list(actual_TCP_pose)
        target_pose[0] = target_x 
        # Synchron fahren (False), damit das Timing danach exakt berechnet werden kann
        rtde_c.moveL(target_pose, 0.2, 0.5, False) 

    # --- ABSOLUTES TIMING BERECHNEN (Y-ACHSE) ---
    tcp_y = actual_TCP_pose[1]
    distance_y = abs(tcp_y - by_korrigiert)
    safe_speed = object_speed if object_speed > 0.001 else 0.001
    
    # Reisezeit berechnen (Die + 1.0 ist dein Stellrad für früher/später greifen)
    total_travel_time = ((distance_y + DISTANCE_TO_CAMERA) / safe_speed) + 0.6
    
    # Abgelaufene Zeit seit dem Foto abziehen (inkl. Roboter-Bewegungszeit)
    elapsed_time = time.time() - capture_time
    stop_time = total_travel_time - elapsed_time

    if debug:
        print(f"[object_waiting] Countdown: {stop_time:.3f}s (Roboter-Fahrzeit war: {elapsed_time:.3f}s)")

    if stop_time > 0:
        time.sleep(stop_time)
    
    return True