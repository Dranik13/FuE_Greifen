"""
idle_handler.py
----------------
Handles the IDLE state for the robot's state machine. This module provides the logic for moving the robot to its home position and waiting for the next task.

Example usage:
    from idle_handler import idle, move_to_home
    idle(rtde_c, robot_speed, robot_acceleration, gripper, debug)
    move_to_home(rtde_c, robot_speed, robot_acceleration, debug)
"""


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
    orientations = []  # NEU: Liste zum Sammeln der Winkel
    
    while True:
        objs = sub.receive_5555()
        if objs is None:
            continue
        if debug:
            print(f'[idle_handler] Received objects: {objs}')
            
        if len(objs) > 0:
            objs = objs[0] # Nimm einfach das erste erkannte Objekt in der Liste
        else:
            continue
            
        if debug:
            print(f"[idle_handler]  {objs['label']} @ ({objs['x']:.3f}, {objs['y']:.3f}, {objs['z']:.3f}), vy={objs.get('vy', 0):.3f}")
            
        object_speed = objs.get('vy', 0)  # speed in y-direction
        object_speed = object_speed / 1000    # conversion from mm/s to m/s
        pos_x = objs['x']
        pos_y = objs['y']

        # Farbe
        label = objs['label']
        
        # Aktuellen Winkel für diesen Frame holen
        current_orientation = objs['orientation']

        width = objs['width'] 
        length = objs['length']
        
        if object_speed >= 0.05:    # wait for multiple measurements with speed to reduce noise
            if counter >= 7:
                speed.append(object_speed)
                orientations.append(current_orientation)  # NEU: Winkel speichern
                
            if counter >= 12:  
                object_speed = sum(speed) / len(speed)  # mean speed
                
                # NEU: Ausreißer beim Winkel entfernen und mitteln
                if len(orientations) > 2:
                    orientations.sort() # Sortiert von klein nach groß
                    filtered_orientations = orientations[1:-1] # Schneidet das erste (Minimum) und letzte (Maximum) ab
                    orientation = sum(filtered_orientations) / len(filtered_orientations)
                    if debug:
                        print(f"[idle_handler] Winkel-Rohdaten: {orientations}")
                        print(f"[idle_handler] Gefilterte Winkel: {filtered_orientations} -> Mittelwert: {orientation}")
                else:
                    orientation = sum(orientations) / len(orientations)
                    
                break
            counter += 1
            
    if debug:
        print(f"[idle_handler] x, y, speed and orientation from Camera: x: {pos_x}, y: {pos_y}, vy: {object_speed}, orient: {orientation}")
        
    # if gripper is not None:
    #     gripper.goTomm(int(width) + 20) 
    #     if debug:
    #         print(f"[idle_handler] Gripper closed with width: {width + 20}")
    
    id_counter += 1
    return pos_x, pos_y, object_speed, orientation, label, width, length
    

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
    '''
    global id_counter
    if id_counter == 1:
        if debug:
            print("[idle_handler] First ID, moving to Home position.")
        move_to_home(rtde_c, robot_speed=robot_speed, robot_acceleration=robot_acceleration, debug=debug)
    return wait_for_object_data(debug=debug, gripper=gripper)