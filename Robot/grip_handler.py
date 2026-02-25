"""
grip_handler.py
----------------
Handles the GRIP state for the robot's state machine. This module provides the logic for gripping detected objects using the robot's gripper.

Example usage:
    from grip_handler import grip
    grip(rtde_r, rtde_c, gripper)
"""

import save_pos

def grip(rtde_r, rtde_c, gripper, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    '''
    Manages the GRIP state of the state machine. The robot grips the detected object using the provided gripper.
    Once the robot has successfully gripped the object, it transitions to the PLACE state to start placing the object.
    Parameters:
        rtde_r: RTDE receive interface for the robot.
        rtde_c: RTDE control interface for the robot.
        gripper: The gripper object used to control the robot's gripper.
        robot_speed: Speed at which the robot should move while gripping (in m/s).
        robot_acceleration: Acceleration at which the robot should move while gripping (in m/s^2).
        debug: If True, prints debug information.
    '''
    actual_TCP = rtde_r.getActualTCPPose()
    gripper.close()
    
    actual_TCP[2] += 0.1  # Move up by 10 cm to ensure a secure grip
    if save_pos.is_save_position(actual_TCP[:3]):
        rtde_c.moveL(actual_TCP, robot_speed, robot_acceleration)
        if debug:
            print(f"[grip_handler] moveL target={actual_TCP[:3]}, v={robot_speed}, a={robot_acceleration}")
    else:
        if debug:
            print(f"[grip_handler] target position {actual_TCP[:3]} is outside the workspace. Movement aborted.")
    if gripper.getPositionmm() < 10:  # Check if the gripper is fully closed (adjust threshold as needed)
        if debug:
            print("[grip_handler] Gripper is fully closed. Object may not be securely gripped.")
        return False  # Indicate that the grip was unsuccessful due to potential issues with the object or gripper
    else:
        return True  # Indicate that the grip was successful and the robot has moved (or attempted to move)