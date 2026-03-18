"""
move_handler.py
----------------
Handles the MOVE state for the robot's state machine. This module provides the logic for moving the robot to a target position based on camera input and object speed.

Example usage:
    from move_handler import idle, move_to_home
    move(pos_x, pos_y, rtde_r, rtde_c, object_speed, robot_speed, robot_acceleration, debug)
"""

from pathlib import Path
import yaml
import save_pos


def _load_kamera_2_kalib_tcp_pos():
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    start_conveyor = data.get("Kamera_2_Kalib", {})
    tcp_pos = start_conveyor.get("TCP Pos")
    if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
        raise ValueError("[move_handler] Invalid or missing 'Kamera_2_Kalib -> TCP Pos' values in pose.yaml")

    return [float(value) for value in tcp_pos]


KAMERA_2_KALIB_TCP_POS = _load_kamera_2_kalib_tcp_pos()

def _load_camera_mount_to_camera_distance():
    pose_file = Path(__file__).with_name("Calibration_results_final.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    camera_mount_to_camera = data.get("camera_mount_to_camera", {})
    camera_to_mount_distance = camera_mount_to_camera.get("y")
    # print(f"[follow_handler] Loaded camera_to_mount_distance from YAML: {camera_to_mount_distance}")
    if isinstance(camera_to_mount_distance, list):
        if len(camera_to_mount_distance) != 1:
            raise ValueError("[follow_handler] Invalid values for 'camera_mount_to_camera -> y' in Calibration_results_final.yaml (expected: 1 value)")
        return float(camera_to_mount_distance[0])

    try:
        return float(camera_to_mount_distance)
    except (TypeError, ValueError):
        raise ValueError("[follow_handler] Invalid or missing value for 'camera_mount_to_camera -> y' in Calibration_results_final.yaml")


DISTANCE_TO_CAMERA = _load_camera_mount_to_camera_distance()


def move(pos_x, pos_y, rtde_r, rtde_c, object_speed, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    
    new_x = pos_x / 1000                           # compensate for the distance between the camera and the robot's TCP, and add a safety margin
    dif_x = new_x / 0.6
    new_y = pos_y / 1000 + (object_speed*(2+(2*dif_x)))  # compensate for the movement of the object during the robot's movement
    target_tcp = KAMERA_2_KALIB_TCP_POS.copy()
    target_tcp[0] = new_x
    target_tcp[1] = new_y
    target_tcp[2] = 0.10
    if save_pos.is_save_position(target_tcp[:3]):
        rtde_c.moveL(target_tcp, robot_speed, robot_acceleration)
        if debug:
            print(f"[move_handler] moveL target={target_tcp[:3]}, v={robot_speed}, a={robot_acceleration}")
    else:
        print(f"[move_handler] Target position {target_tcp[:3]} is outside the workspace. Movement aborted.")