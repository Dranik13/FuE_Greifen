
import save_pos
import time

def grip(rtde_r, rtde_c, gripper, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    '''
    Manages the GRIP state. 
    Lifts the object while keeping the rotation detected by the camera.
    '''
    # 1. AKTUELLE POSE HOLEN
    # Diese Pose enthält bereits die Drehung (RZ) aus dem object_waiting_handler!
    actual_TCP = rtde_r.getActualTCPPose()
    
    # 2. GREIFER SCHLIEẞEN
    if debug:
        print("[grip_handler] Schließe Greifer in Bauteil-Orientierung...")
    gripper.close()
    
    # Kurze Pause, damit die Backen sicher am Bauteil anliegen
    time.sleep(0.4)
    
    # 3. NACH OBEN ABHEBEN
    # Wir erhöhen nur die Z-Koordinate (Index 2). 
    # Die Winkel RX, RY und das gedrehte RZ bleiben unverändert in actual_TCP.
    actual_TCP[2] += 0.1  # 10 cm nach oben
    
    if save_pos.is_save_position(actual_TCP[:3]):
        if debug:
            print(f"[grip_handler] Hebe Bauteil an auf Z={actual_TCP[2]:.3f}m")
        # Bewegung ausführen (behält die Drehung bei)
        rtde_c.moveL(actual_TCP, robot_speed, robot_acceleration)
    else:
        if debug:
            print(f"[grip_handler] Fehler: Ziel-Position {actual_TCP[:3]} außerhalb des Workspace.")
        return False

    # 4. ERFOLGSKONTROLLE
    # Wenn der Greifer fast komplett zugefahren ist (< 15mm), hat er das Teil wohl verloren/verpasst
    gripper_pos = gripper.getPositionmm()
    if gripper_pos < 15:
        if debug:
            print(f"[grip_handler] Greifer zu weit geschlossen ({gripper_pos}mm). Griff fehlgeschlagen.")
        return False
    else:
        if debug:
            print(f"[grip_handler] Griff erfolgreich (Position: {gripper_pos}mm).")
        return True