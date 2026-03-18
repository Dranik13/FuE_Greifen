# Greifstrategie 2: hinten am Fließband in geneigter Position warten

"""
Handles the OBJECT_WAITING state for the robot's state machine. 
Der Roboter steht regungslos in seiner schrägen Lauerposition. Die eigene Kamera (Port 5556)
erkennt das Bauteil, entzerrt die schrägen Bilddaten in absolute Fließbandkoordinaten und 
berechnet exakt die Millisekunde, in der das Bauteil unter dem Greifer ankommt.
"""

import time
from camera_to_robot_transform import CameraToRobotTransformer
import camera_sub

def wait_for_object_data(transformer: CameraToRobotTransformer, sub: camera_sub.CameraSubscriber, debug=False, object_speed=0.1):
    """
    Wartet auf das Bauteil, entzerrt das schräge Kamerabild und gibt die absolute 
    Position des Bauteils im Roboter-Koordinatensystem zurück.
    """
    # 1. NOTBREMSE: Verhindert Absturz durch Null-Division, falls das Band stoppt
    safe_speed = object_speed if object_speed > 0.01 else 0.05
    
    # 2. Timeout in Sekunden berechnen (z.B. 1 / 0.1 m/s = 10 Sekunden)
    timeout_sec = int(1.5 / safe_speed) 
    
    if debug:
        print(f"[object_waiting] Warte auf Bauteil mit Timeout von {timeout_sec} Sekunden...")
        
    start_time = time.time()
    
    while True:
        objs = sub.receive_5556(100)  # Warte 100 ms auf neue Daten
        
        if (time.time() - start_time) > timeout_sec:
            if debug:
                print(f"[object_waiting] Timeout ({timeout_sec} s). Kein Bauteil gesehen.")
            return None, None
            
        # 3. LISTEN-FIX: Prüfen, ob wir Daten haben und sie entpacken
        if objs is None or len(objs) == 0:
            continue
            
        obj = objs[0] # <-- GANZ WICHTIG: Das erste erkannte Bauteil aus der Liste holen!

        # --- NEUE LOGIK: BILD ENTZERREN ---
        # Wandelt die x/y/z Daten der schrägen Kamera in echte Basis-Koordinaten um!
        bx, by, bz = transformer.camera_point_to_base(obj['x'], obj['y'], obj['z'])
        
        if debug:
            print(f"[object_waiting] Bauteil erkannt! Absolut [Base, m]: X={bx:.4f}, Y={by:.4f}, Z={bz:.4f}")
            
        return bx, by


def object_waiting(rtde_c, rtde_r, object_speed=0.1, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    '''
    Übernimmt das Warten und Timing. Der Roboter bewegt sich hier NICHT, 
    sondern berechnet nur den Countdown bis zum Greifen.
    '''
    # Kamera abonnieren und Transformer initialisieren
    sub = camera_sub.CameraSubscriber(address='tcp://localhost:5556', topic="coordinates")
    transformer = CameraToRobotTransformer(rtde_receiver=rtde_r)
    
    if debug:
        print("[object_waiting] Lauerstellung aktiv. Kamera 5556 sucht Bauteil...")
        
    # 1. Warten, bis das Bauteil ins Bild fährt
    bx, by = wait_for_object_data(transformer, sub, debug=debug, object_speed=object_speed)
    
    if by is None:
        if debug:
            print("[object_waiting] Bauteil verloren. Bleibe im WAITING state oder breche ab.")
        return False  

    # 2. DAS TIMING BERECHNEN
    # Wo befindet sich unser Greifer (TCP) exakt in diesem Moment auf der Y-Achse?
    actual_TCP_pose = rtde_r.getActualTCPPose()
    tcp_y = actual_TCP_pose[1]

    # Wie weit muss das Bauteil auf dem Fließband noch fahren, bis es exakt unter dem Greifer ist?
    # (Abstand zwischen Greifer-Y und Bauteil-Y)
    distance_y = abs(tcp_y - by)

    # Wir verhindern, dass durch 0 geteilt wird:
    safe_speed = object_speed if object_speed > 0.001 else 0.001

    # Zeit = Strecke / Geschwindigkeit
    # (Wir ziehen einen winzigen Puffer von z.B. 0.05s ab, da das Schließen der Finger auch minimal Zeit kostet)
    stop_time = (distance_y / safe_speed) - 0.05 

    if debug:
        print(f"[object_waiting] Distanz zum Greifer: {distance_y:.3f}m")
        print(f"[object_waiting] Berechneter Countdown: {stop_time:.3f}s")

    # 3. COUNTDOWN STARTEN
    if stop_time > 0:
        time.sleep(stop_time)
    else:
        if debug:
            print("[object_waiting] WARNUNG: Bauteil ist bereits am Greifer vorbei!")
        # Wenn ihr wollt, könnt ihr hier False zurückgeben, um einen Fehl-Griff zu verhindern

    # Zeit ist abgelaufen, das Bauteil liegt jetzt perfekt unterm Greifer!
    # Wir wechseln in den GRIP State.
    return True