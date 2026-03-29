"""
place_handler.py
----------------
Handles the PLACE state for the robot's state machine. This module provides the logic for moving the robot to its place position based on the object's color.
"""

import yaml
from pathlib import Path
import save_pos

def _load_all_place_positions():
    """
    Lädt die Ablagepositionen für die verschiedenen Farben aus der pose.yaml.
    Gibt ein Dictionary zurück, z.B. {'red': [x,y...], 'blue': [x,y...], 'default': [x,y...]}
    """
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    positions = {}
    
    # 1. Spezifische Farben aus der YAML laden (red, blue, white, black)
    for color in ['red', 'blue', 'white', 'black']:  
        yaml_key = f"Place_{color}"
        if yaml_key in data:
            tcp_pos = data[yaml_key].get("TCP Pos")
            if isinstance(tcp_pos, list) and len(tcp_pos) == 6:
                positions[color] = [float(value) for value in tcp_pos]

    # 2. Die Standard-Position als Fallback laden
    place_default = data.get("Move_to_Place", {})
    tcp_pos_default = place_default.get("TCP Pos")
    if isinstance(tcp_pos_default, list) and len(tcp_pos_default) == 6:
        positions["default"] = [float(value) for value in tcp_pos_default]
    else:
        raise ValueError("[place_handler] Missing or invalid fallback 'Move_to_Place -> TCP Pos' in pose.yaml")

    return positions

# Lade alle Positionen einmalig beim Programmstart in ein Dictionary
PLACE_POSITIONS = _load_all_place_positions()


def place(rtde_c, gripper, robot_speed=0.8, robot_acceleration=0.5, label="default", debug=False):
    '''
    Manages the PLACE state. The robot moves to the color-specific place position and releases the object.
    '''
    # 1. Farbe sicherstellen (alles klein geschrieben, Fallback falls leer)
    safe_label = str(label).lower() if label else "default"

    # 2. Zielposition aus dem Dictionary holen. Wenn Farbe nicht gefunden -> "default" nehmen
    target_pos = PLACE_POSITIONS.get(safe_label, PLACE_POSITIONS.get("default"))

    if debug:
        print(f"[place_handler] Erkanntes Label: '{safe_label}'. Fahre zur Position: {target_pos}")

    # 3. Sicherheitscheck und Bewegung
    if save_pos.is_save_position(target_pos[:3]):
        rtde_c.moveJ_IK(target_pos, robot_speed, robot_acceleration)
    else:
        print(f"[place_handler] Fehler: Ziel-Position {target_pos[:3]} für Farbe '{safe_label}' ist außerhalb des Workspace. Bewegung abgebrochen.")
        
    if debug:
        print(f"[place_handler] Reached PLACE position for {safe_label}.")


# """
# place_handler.py
# ----------------
# Handles the PLACE state for the robot's state machine. This module provides the logic for moving the robot to its place position and releasing the object.

# Example usage:
#     from place_handler import idle, move_to_home
#     place(rtde_c, gripper, robot_speed, robot_acceleration, debug)
# """

# import yaml
# from pathlib import Path
# import save_pos

# def _load_place_tcp_pos():
    
#     pose_file = Path(__file__).with_name("pose.yaml")
#     with pose_file.open("r", encoding="utf-8") as stream:
#         data = yaml.safe_load(stream)

#     place = data.get("Move_to_Place", {})

#     tcp_pos = place.get("TCP Pos")
#     if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
#         raise ValueError("[place_handler] Invalid or missing 'Move_to_Place -> TCP Pos' values in pose.yaml")

#     return [float(value) for value in tcp_pos]

# PLACE_TCP_POS = _load_place_tcp_pos()

# def place(rtde_c, gripper, robot_speed=0.8, robot_acceleration=0.5, debug=False):
#     '''
#     Manages the PLACE state of the state machine. The robot moves to the predefined place position and releases the object by opening the gripper.
#     Once the robot has successfully released the object, it transitions back to the IDLE state to wait for the next task.
#     Parameters:
#         rtde_c: RTDE control interface for the robot.
#         gripper: The gripper object used to control the robot's gripper.
#         robot_speed: Speed at which the robot should move while placing (in m/s).
#         robot_acceleration: Acceleration at which the robot should move while placing (in m/s^2).
#         debug: If True, prints debug information.
#     '''
#     if debug:
#         print(f"[place_handler] Moving to PLACE position: {PLACE_TCP_POS}")
#     if save_pos.is_save_position(PLACE_TCP_POS[:3]):
#         rtde_c.moveJ_IK(PLACE_TCP_POS, robot_speed, robot_acceleration)
#     else:
#         print(f"[place_handler] Target position {PLACE_TCP_POS[:3]} is outside the workspace. Movement aborted.")
#     if debug:
#         print("[place_handler] Reached PLACE position.")