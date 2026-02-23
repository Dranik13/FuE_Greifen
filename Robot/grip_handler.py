import save_pos

def grip(rtde_r, rtde_c, gripper, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    actual_TCP = rtde_r.getActualTCPPose()
    gripper.close()
    
    actual_TCP[2] += 0.05  # Move up by 5 cm to ensure a secure grip
    if save_pos.is_save_position(actual_TCP[:3]):
        rtde_c.moveL(actual_TCP, robot_speed, robot_acceleration)
        if debug:
            print(f"[grip_handler] moveL target={actual_TCP[:3]}, v={robot_speed}, a={robot_acceleration}")
    else:
        if debug:
            print(f"[grip_handler] target position {actual_TCP[:3]} is outside the workspace. Movement aborted.")