import time
import save_pos

def grip(rtde_r, rtde_c, gripper, speed = 0.1):
    actual_TCP = rtde_r.getActualTCPPose()
    gripper.close()
    
    actual_TCP[2] += 0.05  # Move up by 5 cm to ensure a secure grip
    if save_pos.is_save_position(actual_TCP[:3]):
        rtde_c.moveL(actual_TCP, 0.8, 0.5)
    else:
        print(f"[Grip Handler] Zielposition {actual_TCP[:3]} ist außerhalb des Arbeitsbereichs. Bewegung wird abgebrochen.")
    # time.sleep(1)
    # rtde_c.speedStop(0.1)