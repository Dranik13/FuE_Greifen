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
    while True:
        objs = sub.receive_5555()
        if objs is None:
            continue
        if debug:
            print(f'[idle_handler] Received objects: {objs}')
        objs = next((o for o in objs if o.get("id") == id_counter), None)
        if objs is None:
            continue
        if debug:
            print(f"[idle_handler]  {objs['label']} @ ({objs['x']:.3f}, {objs['y']:.3f}, {objs['z']:.3f}), vy={objs.get('vy', 0):.3f}")
        object_speed = objs.get('vy', 0)  # speed in y-direction
        object_speed = object_speed / 1000    # conversion from mm/s to m/s
        pos_x = objs['x']
        pos_y = objs['y']
        orientation = objs['orientation']
        width = objs['width']
        if object_speed >= 0.05:    # wait for multiple measurements with speed to reduce noise
            if counter >= 7:
                speed.append(object_speed)
            if counter >= 12:  # wait for multiple measurements with speed to reduce noise
                object_speed = sum(speed) / (len(speed))  # mean speed
                break
            counter += 1
    if debug:
        print(f"[idle_handler] x, y and speed from Camera: x: {pos_x}, y: {pos_y}, vy: {object_speed}")
        
    if gripper is not None:
        gripper.goTomm(int(width) + 20) # Close the gripper based on the measured width + some tolerance
        if debug:
            print(f"[idle_handler] Gripper closed with width: {width + 20}")
    
    id_counter += 1
    return pos_x, pos_y, object_speed
    

def move_to_home(rtde_c, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    '''
    moves the robot to the predefined home position (Start Conveyor) to prepare for the next pick operation.
    Parameters:
        rtde_c: RTDE control interface for the robot.
        robot_speed: Speed at which the robot should move while transitioning from IDLE to MOVE (in m/s).
        robot_acceleration: Acceleration at which the robot should move while transitioning from IDLE to MOVE (in m/s^2).
        debug: If True, prints debug information about the robot's actions and the target position.
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
    The robot starts in the IDLE state, waiting for the next object to pick. It listens for object data from the camera and processes it to determine the position and speed of the object. 
    Once the object data is received and processed, the robot moves to the home position to prepare for the next pick operation.
    After moving to the home position, it transitions to the MOVE state to start the picking process.
    Parameters:
        rtde_c: RTDE control interface for the robot.
        robot_speed: Speed at which the robot should move while transitioning from IDLE to MOVE (in m/s).
        robot_acceleration: Acceleration at which the robot should move while transitioning from IDLE to MOVE (in m/s^2).
        gripper: Optional gripper object used to control the robot's gripper. If provided, it will be used to close the gripper based on the measured width of the object.
        debug: If True, prints debug information about the received object data and the robot's actions.
    Returns:
        A tuple containing the x and y position of the detected object (in mm) and its speed in the y-direction (in m/s). 
        This information is used to transition to the MOVE state and start the picking process.
        If there is an issue during handling, it may return None to indicate that the state should remain in IDLE until the issue is resolved. 
    '''
    global id_counter
    if id_counter == 1:
        if debug:
            print("[idle_handler] First ID, moving to Home position.")
        move_to_home(rtde_c, robot_speed=robot_speed, robot_acceleration=robot_acceleration, debug=debug)
    return wait_for_object_data(debug=debug, gripper=gripper)