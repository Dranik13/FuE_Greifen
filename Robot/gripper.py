from pymodbus.client import ModbusSerialClient
from pyrobotiqgripper import RobotiqGripper
import time

gripper = RobotiqGripper()
gripper.activate()
gripper.calibrate(0,130)

gripper.open()
#time.sleep(2)
# gripper.close()

position_in_mm = gripper.getPositionmm()
print("Positionin mm: ", position_in_mm)
gripper.printInfo()
