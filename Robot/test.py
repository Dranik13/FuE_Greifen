import time

import rtde_receive
import rtde_control
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.96.221")
# actual_q = rtde_r.getActualQ()
actual_TCP = rtde_r.getActualTCPPose()
# status = rtde_r.getRobotStatus()

# print("Joint Pos: ", actual_q)
print("TCP Pos: ", actual_TCP)
# binary_string = format(status, "04b")   # 4 Bits, mit führenden Nullen
# print(binary_string)
# rtde_c = rtde_control.RTDEControlInterface("192.168.96.221")
# rtde_c.moveL([0.46987006692897526, -0.6141117468652709, 0.29701407690139925, -2.2319500763632916, 2.2104305473135506, -0.0007869137174410558], 0.2, 0.1)
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
# print("TCP Pos: ", actual_TCP)