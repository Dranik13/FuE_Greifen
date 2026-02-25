"""
base.py
----------------
Handles the base functionality for the robot's state machine. This module provides the logic for initializing the robot, gripper, and state machine.
It defines the state machine and its handlers for each state, as well as a safe shutdown procedure.
"""

from __future__ import annotations
from platform import machine
from enum import Enum, auto
from typing import Callable, Dict, Optional
import rtde_receive
import rtde_control
from pyrobotiqgripper import RobotiqGripper

from runtime_config import load_runtime_config

# Import handler-modules
import idle_handler
import move_handler
import place_handler
import object_waiting_handler
import grip_handler


RUNTIME_CONFIG = load_runtime_config()
DEBUG = RUNTIME_CONFIG.debug

# initialization of Gripper
GRIPPER = RobotiqGripper()
GRIPPER.activate()
GRIPPER.calibrate(0, 130)
GRIPPER.open()

pos_x = 0
pos_y = 0
object_speed = 0
ROBOT_SPEED = RUNTIME_CONFIG.robot_speed
ROBOT_ACC = RUNTIME_CONFIG.robot_acceleration
ROBOT_IP = RUNTIME_CONFIG.robot_ip

RTDE_C = rtde_control.RTDEControlInterface(ROBOT_IP)
RTDE_R = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

class MachineState(Enum):
	IDLE = auto()
	MOVE = auto()
	OBJECT_WAITING = auto()
	GRIP = auto()
	PLACE = auto()


StateHandler = Callable[["RandomStateMachine"], Optional[MachineState]]


class RandomStateMachine:
	'''
	A state machine that manages the different states of the robot's operation, including IDLE, MOVE, FOLLOW, GRIP, and PLACE.
	The state machine transitions between states based on the handlers defined for each state, which contain the logic for performing the necessary actions in each state 
	and determining the next state to transition to.
	'''
	def __init__(self, handlers: Dict[MachineState, StateHandler], start_state: Optional[MachineState] = MachineState.IDLE) -> None:
		missing = [state for state in MachineState if state not in handlers]
		if missing:
			missing_names = ", ".join(state.name for state in missing)
			raise ValueError(f"[Base] Missing handlers for states: {missing_names}")

		self._handlers = handlers
		self.state = start_state if start_state is not None else MachineState.IDLE

	def set_state(self, new_state: MachineState) -> None:
		self.state = new_state


def idle_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	'''
	Handles the IDLE state of the state machine. In this state, the robot waits for an object to be detected and retrieves its position and speed.
	Once the necessary information is obtained, it transitions to the MOVE state.
	Parameters:
		machine: The instance of the RandomStateMachine that is currently in the IDLE state.
	Returns:
		The next state to transition to, which is typically MachineState.MOVE after successfully handling the IDLE state.
		If there is an issue during handling, it may return None to indicate that the state should remain in IDLE until the issue is resolved.
	'''
	
	if DEBUG:
		print("[Base] Handling IDLE state...")
	global pos_x, pos_y, object_speed
	pos_x, pos_y, object_speed = idle_handler.idle(
		rtde_c=RTDE_C,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
		gripper=GRIPPER,
	)
	return MachineState.MOVE


def move_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	'''
	Handles the MOVE state of the state machine. In this state, the robot moves to the position of the detected object using the provided coordinates and speed.
	Once the robot has moved to the target position, it transitions to the OBJECT_WAITING state to start waiting for the object.
	Parameters:
		machine: The instance of the RandomStateMachine that is currently in the MOVE state.
	Returns:
		The next state to transition to, which is typically MachineState.OBJECT_WAITING after successfully handling the MOVE state.
		If there is an issue during handling, it may return None to indicate that the state should remain in MOVE until the issue is resolved.
	'''
	if DEBUG:
		print("[Base] Handling MOVE state...")
	move_handler.move(
		pos_x = pos_x,
		pos_y = pos_y,
		rtde_r=RTDE_R,
		rtde_c=RTDE_C,
		object_speed=object_speed,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
	)
	return MachineState.OBJECT_WAITING


def object_waiting_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	'''
	Handles the OBJECT_WAITING state for the robot's state machine. This module provides the logic for waiting to detect the object using the robot's camera
	and calculate the needed wait time before gripping the object.
	Parameters:
		machine: The instance of the RandomStateMachine that is currently in the OBJECT_WAITING state.
	Returns:
		The next state to transition to, which is typically MachineState.GRIP after successfully handling the OBJECT_WAITING state.
		If there is an issue during handling, it may indicate failure, open the gripper, move to home position, and switch back to IDLE to reset the process.
	'''

	if DEBUG:
		print("[Base] Handling OBJECT_WAITING state...")
	if object_waiting_handler.object_waiting(
		rtde_c=RTDE_C,
		rtde_r=RTDE_R,
		object_speed=object_speed,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
	):
		return MachineState.GRIP
	else:
		if DEBUG:
			print("[Base] Object waiting handler indicated failure. Move to start and change to IDLE State.")
		GRIPPER.open()  # Ensure the gripper is open before moving back to start
		idle_handler.move_to_home(rtde_c=RTDE_C, debug=DEBUG)
		return MachineState.IDLE


def grip_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	'''
	Handles the GRIP state of the state machine. In this state, the robot grips the detected object using the provided gripper.
	Once the robot has successfully gripped the object, it transitions to the PLACE state to start placing the object.
	Parameters:
		machine: The instance of the RandomStateMachine that is currently in the GRIP state.
	Returns:
		The next state to transition to, which is typically MachineState.PLACE after successfully handling the GRIP state.
		If there is an issue during handling, it may indicate failure, open the gripper, move to home position, and switch back to IDLE to reset the process.
	'''

	if DEBUG:
		print("[Base] Handling GRIP state...")
	if grip_handler.grip(
		rtde_r=RTDE_R,
		rtde_c=RTDE_C,
		gripper=GRIPPER,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
	):
		return MachineState.PLACE
	else:
		if DEBUG:
			print("[Base] Grip handler indicated failure. Move to start and change to IDLE State.")
		GRIPPER.open()  # Ensure the gripper is open before moving back to start
		idle_handler.move_to_home(rtde_c=RTDE_C, debug=DEBUG)
		return MachineState.IDLE


def place_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	'''
	Handles the PLACE state of the state machine. In this state, the robot moves to the target position and places the gripped object using the provided gripper.
	Once the robot has successfully placed the object, it transitions to the IDLE state to start the cycle again.
	Parameters:
		machine: The instance of the RandomStateMachine that is currently in the PLACE state.
	Returns:
		The next state to transition to, which is typically MachineState.IDLE after successfully handling the PLACE state.
		If there is an issue during handling, it may return None to indicate that the state should remain in PLACE until the issue is resolved.
	'''
	if DEBUG:
		print("[Base] Handling PLACE state...")
	place_handler.place(
		rtde_c=RTDE_C,
		gripper=GRIPPER,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
	)
	GRIPPER.open()  # Open the gripper to release the object
	return MachineState.IDLE


def safe_shutdown() -> None:
	'''
	Performs a safe shutdown of the robot and gripper, ensuring that all movements are stopped and the gripper is deactivated.
	'''
	print("[Base] Starting safe shutdown...")
	try:
		for stop_call in (
			lambda: RTDE_C.stopJ(1.0),
			lambda: RTDE_C.stopL(1.0),
			lambda: RTDE_C.speedStop(1.0),
		):
			try:
				stop_call()
			except Exception:
				pass

		if hasattr(RTDE_C, "stopScript"):
			try:
				RTDE_C.stopScript()
			except Exception:
				pass
	except Exception as exc:
		print(f"[Base] Notice: Robot stop could not be fully executed: {exc}")

	try:
		if hasattr(GRIPPER, "open"):
			GRIPPER.open()
	except Exception as exc:
		print(f"[Base] Notice: gripper could not be opened: {exc}")

	try:
		if hasattr(GRIPPER, "deactivate"):
			GRIPPER.deactivate()
	except Exception as exc:
		print(f"[Base] Notice: gripper could not be deactivated: {exc}")

	print("[Base] Shutdown completed.")


DEFAULT_HANDLERS: Dict[MachineState, StateHandler] = {
	MachineState.IDLE: idle_handling,
	MachineState.MOVE: move_handling,
	MachineState.OBJECT_WAITING: object_waiting_handling,
	MachineState.GRIP: grip_handling,
	MachineState.PLACE: place_handling,
}


if __name__ == '__main__':
	machine = RandomStateMachine(handlers=DEFAULT_HANDLERS)
	try:
		while True:
			handler = machine._handlers[machine.state]
			next_state = handler(machine)
			if next_state is not None:
				machine.set_state(next_state)
			else:
				if DEBUG:
					print(f"[Base] Remaining in state {machine.state.name} due to handler returning None.")
	except KeyboardInterrupt:
		print("\n[Base] Ctrl+C detected. Exiting program...")
	finally:
		safe_shutdown()
