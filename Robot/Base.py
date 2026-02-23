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
import follow_handler
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
	FOLLOW = auto()
	GRIP = auto()
	PLACE = auto()


StateHandler = Callable[["RandomStateMachine"], Optional[MachineState]]


class RandomStateMachine:
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
	return MachineState.FOLLOW


def follow_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	if DEBUG:
		print("[Base] Handling FOLLOW state...")
	follow_handler.follow(
		rtde_c=RTDE_C,
		rtde_r=RTDE_R,
		object_speed=object_speed,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
	)
	return MachineState.GRIP


def grip_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	if DEBUG:
		print("[Base] Handling GRIP state...")
	grip_handler.grip(
		rtde_r=RTDE_R,
		rtde_c=RTDE_C,
		gripper=GRIPPER,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
	)
	return MachineState.PLACE


def place_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	if DEBUG:
		print("[Base] Handling PLACE state...")
	place_handler.place(
		rtde_c=RTDE_C,
		gripper=GRIPPER,
		robot_speed=ROBOT_SPEED,
		robot_acceleration=ROBOT_ACC,
		debug=DEBUG,
	)
	return MachineState.IDLE


def safe_shutdown() -> None:
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
	MachineState.FOLLOW: follow_handling,
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
	except KeyboardInterrupt:
		print("\n[Base] Ctrl+C detected. Exiting program...")
	finally:
		safe_shutdown()
