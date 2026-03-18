# Greifstrategie 2: hinten am Fließband in geneigter Position warten

"""
Handles the GRIP state for the robot's state machine. 
(Strategie 1: Schräg greifen, senkrecht nach oben abheben und in der Luft wieder senkrecht ausrichten).
"""

import save_pos
import time

def grip(rtde_r, rtde_c, gripper, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    '''
    Manages the GRIP state of the state machine. The robot grips the detected object 
    using the provided gripper in an angled position, lifts it up, and rotates it to a vertical position.
    
    Parameters:
        rtde_r: RTDE receive interface for the robot.
        rtde_c: RTDE control interface for the robot.
        gripper: The gripper object used to control the robot's gripper.
        robot_speed: Speed at which the robot should move while gripping (in m/s).
        robot_acceleration: Acceleration at which the robot should move while gripping (in m/s^2).
        debug: If True, prints debug information.
    '''
    
    # 1. SCHRÄG GREIFEN
    # Der Roboter steht bereits im richtigen Winkel und auf der richtigen Höhe.
    if debug:
        print("[grip_handler] Schließe Greifer in schräger Position...")
    gripper.close()
    
    # Eine winzige Pause, um sicherzugehen, dass die Finger komplett geschlossen sind, 
    # bevor der Roboter ruckartig nach oben zieht.
    time.sleep(0.5)     # evt. anpassen!
    
    # 2. NACH OBEN ABHEBEN (Sicherheitsabstand zum Band)
    actual_TCP = rtde_r.getActualTCPPose()
    actual_TCP[2] += 0.1  # 10 cm nach oben im Basis-Koordinatensystem
    
    if save_pos.is_save_position(actual_TCP[:3]):
        if debug:
            print(f"[grip_handler] Hebe Bauteil an auf Z={actual_TCP[2]:.3f}...")
        rtde_c.moveL(actual_TCP, robot_speed, robot_acceleration)
    else:
        if debug:
            print(f"[grip_handler] target position {actual_TCP[:3]} is outside the workspace. Movement aborted.")
        return False # Wenn er nicht abheben kann, abbrechen!
        
    # 3. IN DER LUFT SENKRECHT AUFRICHTEN
    # Wir nehmen die aktuelle Position in der Luft und überschreiben NUR die Rotation.
    # Das sind exakt deine Werte aus der "Kamera_2_Kalib" für den senkrechten Greifer:
    vertical_TCP = actual_TCP.copy()
    vertical_TCP[3] = -2.232760029556063
    vertical_TCP[4] = 2.2031143315023454
    vertical_TCP[5] = 0.02547098480488615
    
    if debug:
        print("[grip_handler] Richte Handgelenk senkrecht aus...")
    rtde_c.moveL(vertical_TCP, robot_speed, robot_acceleration)
    
    # 4. ERFOLGSKONTROLLE
    # Check if the gripper is fully closed (adjust threshold as needed)
    if gripper.getPositionmm() < 10:  
        if debug:
            print("[grip_handler] Gripper is fully closed (< 10mm). Object may not be securely gripped.")
        return False  
    else:
        if debug:
            print("[grip_handler] Bauteil erfolgreich gegriffen und für den Transport aufgerichtet!")
        return True