import time

def grip(rtde_c, gripper, speed = 0.1):
    while True:
        gripper.close()
        rtde_c.speedL([0,0,1,0,0,0], speed, 0.1)
        if stopping():
            break
    stop(rtde_c)


def stop(rtde_c):
    rtde_c.speedStop(0.1)

def stopping():
    time.sleep(1)
    return True