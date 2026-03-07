from pymodbus.client import ModbusSerialClient
from pyrobotiqgripper import RobotiqGripper
import time

gripper = RobotiqGripper()
gripper.activate()
gripper.calibrate(0,130)

gripper.open()
#gripper.close()
#time.sleep(2)
gripper.goTomm(50)

# position_in_mm = gripper.getPositionmm()
# print("Positionin mm: ", position_in_mm)
# gripper.printInfo()
# print(dir(gripper))