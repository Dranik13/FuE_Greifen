from __future__ import annotations

from platform import machine
import random
from enum import Enum, auto
from typing import Callable, Dict, Optional
import rtde_receive
import rtde_control
import idle_handler
import move_handler
import place_handler
import follow_handler
import grip_handler
import time
from pymodbus.client import ModbusSerialClient
from pyrobotiqgripper import RobotiqGripper
import time

debug = True

gripper = RobotiqGripper()
gripper.activate()
gripper.open()

pos_x = 0
pos_y = 0
object_speed = 0
robot_speed = 0.1
ROBOT_IP = "192.168.96.221"
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

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
			raise ValueError(f"[Base] Fehlende Handler für Zustände: {missing_names}")

		self._handlers = handlers
		self.state = start_state if start_state is not None else MachineState.IDLE

	def set_state(self, new_state: MachineState) -> None:
		self.state = new_state


def idle_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	
	if debug:
		print("[Base] Handling IDLE state...")
	global pos_x, pos_y, object_speed
	pos_x, pos_y, object_speed = idle_handler.idle(rtde_c)
	return MachineState.MOVE

def move_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	if debug:
		print("[Base] Handling MOVE state...")
	move_handler.move(pos_x, pos_y, rtde_r, rtde_c, object_speed)
	return MachineState.FOLLOW


def follow_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	if debug:
		print("[Base] Handling FOLLOW state...")
	follow_handler.follow(rtde_c, rtde_r, object_speed=object_speed)
	return MachineState.GRIP


def grip_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	if debug:
		print("[Base] Handling GRIP state...")
	grip_handler.grip(rtde_r, rtde_c, gripper, speed=object_speed)
	# gripper.close()
	return MachineState.PLACE

def place_handling(machine: RandomStateMachine) -> Optional[MachineState]:
	if debug:
		print("[Base] Handling PLACE state...")
	place_handler.place(rtde_c, gripper)
	# place_handler.place(gripper, rtde_c)
	return MachineState.IDLE


def safe_shutdown() -> None:
	print("[Base] Starte sauberen Shutdown...")
	try:
		for stop_call in (
			lambda: rtde_c.stopJ(2.0),
			lambda: rtde_c.stopL(2.0),
			lambda: rtde_c.speedStop(2.0),
		):
			try:
				stop_call()
			except Exception:
				pass

		if hasattr(rtde_c, "stopScript"):
			try:
				rtde_c.stopScript()
			except Exception:
				pass
	except Exception as exc:
		print(f"[Base] Hinweis: Robot-Stopp konnte nicht vollständig ausgeführt werden: {exc}")

	try:
		if hasattr(gripper, "open"):
			gripper.open()
	except Exception as exc:
		print(f"[Base] Hinweis: Greifer konnte nicht geöffnet werden: {exc}")

	try:
		if hasattr(gripper, "deactivate"):
			gripper.deactivate()
	except Exception as exc:
		print(f"[Base] Hinweis: Greifer konnte nicht deaktiviert werden: {exc}")

	print("[Base] Shutdown abgeschlossen.")


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
		print("\n[Base] Strg+C erkannt. Beende Programm...")
	finally:
		safe_shutdown()
