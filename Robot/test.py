import time

import rtde_receive
import rtde_control
rtde_r = rtde_receive.RTDEReceiveInterface("192.168.96.221")
actual_q = rtde_r.getActualQ()
actual_TCP = rtde_r.getActualTCPPose()
# status = rtde_r.getRobotStatus()

# print("Joint Pos: ", actual_q)
print("TCP Pos: ", actual_TCP)
# binary_string = format(status, "04b")   # 4 Bits, mit führenden Nullen
# print(binary_string)
# rtde_c = rtde_control.RTDEControlInterface("192.168.96.221")
# rtde_c.moveJ([2.468297004699707, -0.6077818435481568, 0.5860808531390589, -1.5494638488492747, -1.5705955664264124, -0.683514420186178], 0.2, 0.1)
# rtde_c.speedL([0,0.1,0,0,0,0], 0.1, 0.1)
# time.sleep(1)
# rtde_c.speedStop(0.1)
# actual_TCP = rtde_r.getActualTCPPose()
# print("TCP Pos: ", actual_TCP)