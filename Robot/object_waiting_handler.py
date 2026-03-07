"""
object_waiting_handler.py
----------------
Handles the FOLLOW state for the robot's state machine. This module provides the logic for waiting to detect the object using the robot's camera
and calculate the needed wait time before gripping the object.

Example usage:
    from follow_handler import follow
    follow(rtde_c, rtde_r, object_speed, robot_speed, robot_acceleration, debug)
"""

import time
import yaml
from pathlib import Path
from camera_to_robot_transform import CameraToRobotTransformer
import camera_sub
import save_pos


def _load_camera_mount_to_camera_distance():
    pose_file = Path(__file__).with_name("Calibration_results_final.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    camera_mount_to_camera = data.get("camera_mount_to_camera", {})
    camera_to_mount_distance = camera_mount_to_camera.get("x")
    # Uncomment for debugging:
    # print(f"[follow_handler] Loaded camera_to_mount_distance from YAML: {camera_to_mount_distance}")
    if isinstance(camera_to_mount_distance, list):
        if len(camera_to_mount_distance) != 1:
            raise ValueError("[follow_handler] Invalid values for 'camera_mount_to_camera -> x' in Calibration_results_final.yaml (expected: 1 value)")
        return float(camera_to_mount_distance[0])

    try:
        return float(camera_to_mount_distance)
    except (TypeError, ValueError):
        raise ValueError("[follow_handler] Invalid or missing value for 'camera_mount_to_camera -> x' in Calibration_results_final.yaml")


distance_to_camera = _load_camera_mount_to_camera_distance()


def wait_for_object_data(transformer: CameraToRobotTransformer, sub: camera_sub.CameraSubscriber, debug=False, object_speed=0.1):
    """
    Receives object position from the camera subscriber and returns the y-position in meters.
    Optionally prints debug information.
    """
    timeout = int(1 / object_speed)  # in ms, scaled with object speed (e.g. 1m at 0.1m/s)
    print(f"[follow_handler] Waiting for object data with timeout of {timeout} ms...")
    start_time = time.time()
    while True:
        obj = sub.receive_5556(100)  # Wait for 100 ms for new data
        if (time.time() - start_time) > timeout:
            if debug:
                print(f"[follow_handler] Timeout reached ({timeout} ms) while waiting for object data. No valid data received.")
            return None  # Timeout reached without receiving valid data
        if obj is None:
            continue

        if debug:
            print(f"[follow_handler] Object center [mm]: X={obj['x']:.3f}, Y={obj['y']:.3f}, Z={obj['z']:.3f}")
        pos_y = obj['y'] / 1000.0  # Convert mm to meter
        pos_x = obj['x'] / 1000.0  # Convert mm to meter
        # To transform to robot coordinates, uncomment below:
        # bx, by, bz = transformer.camera_point_to_base(obj['x'], obj['y'], obj['z'])
        # print(f"[follow_handler] Object center [base,m]: X={bx:.4f}, Y={by:.4f}, Z={bz:.4f}")
        return pos_x, pos_y


def object_waiting(rtde_c, rtde_r, object_speed=0.1, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    '''
    Manages the FOLLOW state of the state machine. The robot waits for the object to be detected.
    Once detected, it calculates the required wait time before closing the gripper, then transitions to the GRIP state.

    Parameters:
        rtde_c: RTDE control interface for the robot.
        rtde_r: RTDE receive interface for the robot.
        object_speed: Speed of the object to follow (in m/s).
        robot_speed: Speed of the robot (in m/s).
        robot_acceleration: Acceleration of the robot (in m/s^2).
        debug: If True, prints debug information.
    '''
    sub = camera_sub.CameraSubscriber(address='tcp://localhost:5556', topic="coordinates")
    transformer = CameraToRobotTransformer(rtde_receiver=rtde_r)
    if debug:
        print("[follow_handler] Waiting for 'coordinates' messages on tcp://localhost:5556...")
    pos_x, pos_y = wait_for_object_data(transformer, sub, debug=debug, object_speed=object_speed)
    if pos_y is None:
        if debug:
            print("[follow_handler] No valid object position received within timeout. Remaining in FOLLOW state.")
        return False  # Indicate failure to receive data
    stop_time = (distance_to_camera + abs(pos_y)) / object_speed - 0.3  # Subtract a small buffer time to ensure we grip slightly before the object reaches the camera
    start_time = time.time()
    if debug:
        print(f"[follow_handler] Calculated stop time: {stop_time:.3f}s based on pos_y={pos_y:.3f}m and object_speed={object_speed:.3f}m/s")
    actual_TCP_pose = rtde_r.getActualTCPPose()
    actual_TCP_pose[0] -= (pos_x - 0.03)  # Move in x-direction to align with the object
    print(f"[follow_handler] Adjusted TCP pose for following: {(pos_x - 0.03):.3f}m in x-direction, with {pos_x} + 0.03)m total adjustment")
    if save_pos.is_save_position(actual_TCP_pose[:3]):
        if debug:
            print(f"[follow_handler] Moving to position: {actual_TCP_pose} with speed: {robot_speed} m/s and acceleration: {robot_acceleration} m/s^2")
        rtde_c.moveL(actual_TCP_pose, robot_speed, robot_acceleration)
    else:
        if debug:
            print(f"[follow_handler] Current position {actual_TCP_pose[:3]} is not a valid save position. Skipping move command.")
    while (time.time() - start_time) < stop_time:
        # if debug:
        #     elapsed = time.time() - start_time
        #     remaining = stop_time - elapsed
        #     print(f"[follow_handler] Waiting... Elapsed: {elapsed:.3f}s, Remaining: {remaining:.3f}s")
        time.sleep(0.05)  # Sleep briefly to avoid busy-waiting
    return True  # Indicate that we are ready to transition to the GRIP state after following the object