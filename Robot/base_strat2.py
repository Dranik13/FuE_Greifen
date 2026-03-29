# Muss nochmal getestet werden! Vorsicht!
"""
base_strat2.py
----------------
Handles the base functionality for the robot's state machine. 
ANGEPASST FÜR STRATEGIE 2
"""

from __future__ import annotations
from platform import machine
from enum import Enum, auto
from typing import Callable, Dict, Optional
import rtde_receive
import rtde_control
from pyrobotiqgripper import RobotiqGripper

from runtime_config import load_runtime_config

# --- NEU: Import der neuen Strategie-Skripte ---
# Wir nutzen "as", damit wir den Code unten nicht umschreiben müssen!
import idle_handler_strat2 as idle_handler
import move_handler_strat2 as move_handler
import object_waiting_handler_strat2 as object_waiting_handler
import grip_handler_strat2 as grip_handler
# Der place_handler bleibt der alte, da wir das Bauteil ja vorher senkrecht aufrichten
import place_handler 
# -----------------------------------------------

RUNTIME_CONFIG = load_runtime_config()
DEBUG = RUNTIME_CONFIG.debug

# initialization of Gripper
GRIPPER = RobotiqGripper()
GRIPPER.activate()
GRIPPER.calibrate(0, 130)
GRIPPER.open()

# --- NEU: obj_height hinzugefügt ---
pos_x = 0
pos_y = 0
obj_height = 0  # <--- Wird jetzt für die Z-Achse benötigt
object_speed = 0
obj_label="default"
# -----------------------------------

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
        
    # --- NEU: obj_height in die globalen Variablen aufnehmen ---
    global pos_x, pos_y, obj_height, object_speed, obj_label 
    
    # --- NEU: idle_handler gibt nun 4 Werte zurück (inkl. Höhe) ---
    pos_x, pos_y, obj_height, object_speed, obj_label = idle_handler.idle(
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
    
    # Speichere das Ergebnis des move-Befehls
    # move() gibt im Erfolgsfall "OBJECT_WAITING" zurück, sonst None
    result = move_handler.move(
        pos_x = pos_x,
        pos_y = pos_y,
        obj_height = obj_height,
        rtde_r=RTDE_R,
        rtde_c=RTDE_C,
        object_speed=object_speed,
        robot_speed=ROBOT_SPEED,
        robot_acceleration=ROBOT_ACC,
        debug=DEBUG,
    )
    
    if result is not None:
        return MachineState.OBJECT_WAITING
    else:
        # Falls die Zielposition ungültig war (z.B. außerhalb Workspace),
        # schicken wir ihn zurück in den IDLE, anstatt ins Leere zu greifen.
        if DEBUG:
            print("[Base] Move handler failed. Returning to IDLE.")
        return MachineState.IDLE

# def move_handling(machine: RandomStateMachine) -> Optional[MachineState]:
#     if DEBUG:
#         print("[Base] Handling MOVE state...")
        
#     move_handler.move(
#         pos_x = pos_x,
#         pos_y = pos_y,
#         obj_height = obj_height, # --- NEU: Höhe wird an move_handler übergeben ---
#         rtde_r=RTDE_R,
#         rtde_c=RTDE_C,
#         object_speed=object_speed,
#         robot_speed=ROBOT_SPEED,
#         robot_acceleration=ROBOT_ACC,
#         debug=DEBUG,
#     )
#     return MachineState.OBJECT_WAITING


def object_waiting_handling(machine: RandomStateMachine) -> Optional[MachineState]:
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
        GRIPPER.open()
        idle_handler.move_to_home(rtde_c=RTDE_C, debug=DEBUG)
        return MachineState.IDLE


def grip_handling(machine: RandomStateMachine) -> Optional[MachineState]:
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
        GRIPPER.open()
        idle_handler.move_to_home(rtde_c=RTDE_C, debug=DEBUG)
        return MachineState.IDLE


def place_handling(machine: RandomStateMachine) -> Optional[MachineState]:
    if DEBUG:
        print("[Base] Handling PLACE state...")
    place_handler.place(
        rtde_c=RTDE_C,
        gripper=GRIPPER,
        robot_speed=ROBOT_SPEED,
        robot_acceleration=ROBOT_ACC,
        label=obj_label,
        debug=DEBUG,
    )
    GRIPPER.open()
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