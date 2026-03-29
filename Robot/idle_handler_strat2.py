"""
Handles the IDLE state for the robot's state machine. This module provides the logic for moving the robot to its home position and waiting for the next task.
ANGEPASST: Gibt nun auch die Bauteilhöhe (obj_height / z-Koordinate) zurück.
"""

from re import sub

import save_pos
from pathlib import Path
import yaml
import camera_sub

id_counter = 1
pos_x = 0

def _load_start_conveyor_tcp_pos():
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    start_conveyor = data.get("Start_Conveyor", {})
    tcp_pos = start_conveyor.get("TCP Pos")
    if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
        raise ValueError("[idle_handler] Invalid or missing 'Start_Conveyor -> TCP Pos' values in pose.yaml")

    return [float(value) for value in tcp_pos]

START_CONVEYOR_TCP_POS = _load_start_conveyor_tcp_pos()


def wait_for_object_data(debug=False, gripper=None):
    sub = camera_sub.CameraSubscriber(address = 'tcp://localhost:5555', topic = "")
    if debug:
        print('[idle_handler] Waiting for messages on tcp://localhost:5555...')
    
    global id_counter
    counter = 0
    speed = []
    obj_label = "default"  # Initialisierung mit Fallback
    
    while True:
        objs = sub.receive_5555()
        if objs is None or len(objs) == 0:
            continue
            
        objs = objs[0] # Wir nehmen das erste erkannte Objekt
        
        # --- FARBE / LABEL HIER DIREKT AUSLESEN ---
        obj_label = objs.get('label', 'default')
        if not obj_label: # Falls der String leer ist
            obj_label = "default"
            
        object_speed = objs.get('vy', 0) / 1000.0 # mm/s -> m/s
        
        pos_x = objs['x']
        pos_y = objs['y']
        obj_height = objs['z']
        width = objs['width']
        
        if debug:
            print(f"[idle_handler] Tracking {obj_label} @ y={pos_y:.3f}, vy={object_speed:.3f}")

        # Geschwindigkeits-Glättung (deine Logik)
        if object_speed >= 0.05:
            if counter >= 7:
                speed.append(object_speed)
            if counter >= 12:
                object_speed = sum(speed) / len(speed)
                break # ERST HIER GEHEN WIR AUS DER SCHLEIFE
            counter += 1
            
    if debug:
        print(f"[idle_handler] FINAL: x: {pos_x}, y: {pos_y}, z: {obj_height}, vy: {object_speed}, label: {obj_label}")
        
    if gripper is not None:
        gripper.goTomm(int(width) + 30)
    
    id_counter += 1
    
    # Gib alle 5 Werte zurück
    return pos_x, pos_y, obj_height, object_speed, obj_label
    

def move_to_home(rtde_c, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    '''
    moves the robot to the predefined home position (Start Conveyor) to prepare for the next pick operation.
    '''
    if save_pos.is_save_position(START_CONVEYOR_TCP_POS[:3]):
        if debug:
            print(f"[idle_handler] Moving to Home position: {START_CONVEYOR_TCP_POS}")
        rtde_c.moveJ_IK(START_CONVEYOR_TCP_POS, robot_speed, robot_acceleration)
        if debug:
            print("[idle_handler] Reached Home position.")
    else:
        if debug:
            print(f"[idle_handler] target position {START_CONVEYOR_TCP_POS[:3]} is outside the workspace. Movement aborted.")


def idle(rtde_c, robot_speed=0.8, robot_acceleration=0.5, gripper=None, debug=False):
    '''
    The robot starts in the IDLE state, waiting for the next object to pick.
    Returns:
        A tuple containing the x and y position, the height (z), and the speed in the y-direction.
    '''
    global id_counter
    if id_counter == 1:
        if debug:
            print("[idle_handler] First ID, moving to Home position.")
        move_to_home(rtde_c, robot_speed=robot_speed, robot_acceleration=robot_acceleration, debug=debug)
        
    # Die Rückgabe von wait_for_object_data wird 1:1 durchgereicht
    return wait_for_object_data(debug=debug, gripper=gripper)