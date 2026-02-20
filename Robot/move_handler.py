import rtde_control
from pathlib import Path
import yaml


def _load_start_conveyor_tcp_pos():
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    start_conveyor = data.get("Start_Conveyor", {})
    tcp_pos = start_conveyor.get("TCP Pos")
    if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
        raise ValueError("[move_handler] Ungültige oder fehlende 'Start_Conveyor -> TCP Pos' Werte in pose.yaml")

    return [float(value) for value in tcp_pos]

START_CONVEYOR_TCP_POS = _load_start_conveyor_tcp_pos()

def move(pos_x, rtde_c):
    new_x = START_CONVEYOR_TCP_POS[0] + (abs(pos_x / 1000))
    print(f"[move_handler] new_x: {new_x}")
    target_tcp = START_CONVEYOR_TCP_POS.copy()
    target_tcp[0] = new_x
    new_pos = rtde_c.getInverseKinematics(target_tcp)
    print(f"[move_handler] new_pos: {new_pos}")
    rtde_c.moveJ(new_pos, 0.3, 0.15)