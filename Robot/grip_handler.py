import time

def grip(rtde_c, gripper, speed = 0.1):
    gripper.close()
    rtde_c.speedL([0,0,1,0,0,0], speed, 0.1)
    time.sleep(1)
    rtde_c.speedStop(0.1)