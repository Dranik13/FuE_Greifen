import time

import rtde_receive
import rtde_control
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.96.221")
# actual_q = rtde_r.getActualQ()
actual_TCP = rtde_r.getActualTCPPose()
# status = rtde_r.getRobotStatus()

# print("Joint Pos: ", actual_q)
# print("TCP Pos: ", actual_TCP)
rtde_c = rtde_control.RTDEControlInterface("192.168.96.221")
new_x = 0.4299188979059998 + 0.03436 + 0.10 - 0.005
new_y = -0.6104172709301667 - 0.05
rtde_c.moveL([new_x, new_y, 0.10, -2.232739631053332, 2.203136075703988, 0.025498422826788783], 0.2, 0.1)
# start = time.time()
# rtde_c.speedL([0,-1,0,0,0,0], 0.1, 0.1)
# time.sleep(1)
# start_2 = time.time()
# rtde_c.speedL([0,-1,1,0,0,0], 0.1, 0.1)

# time.sleep(0.6)
# stop_2 = time.time()
# rtde_c.speedStop(0.1)
# print(f"Time with speedL([0,-1,0,0,0,0]): {start_2 - start:.3f}s")
# print(f"Time with speedL([0,-1,1,0,0,0]): {stop_2 - start_2:.3f}s")
# actual_TCP = rtde_r.getActualTCPPose()
print("TCP Pos: ", actual_TCP)