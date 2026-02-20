import yaml
from pathlib import Path

def _load_place_tcp_pos():
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    place = data.get("Move_to_Place", {})

    tcp_pos = place.get("TCP Pos")
    if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
        raise ValueError("[place_handler] Ungültige oder fehlende 'Move_to_Place -> TCP Pos' Werte in pose.yaml")

    return [float(value) for value in tcp_pos]

PLACE_TCP_POS = _load_place_tcp_pos()

def place(rtde_c, gripper):
    new_pos = rtde_c.getInverseKinematics(PLACE_TCP_POS)
    print(f"[place_handler] Moving to PLACE position: {new_pos}")
    rtde_c.moveJ(new_pos, 0.8, 0.2)
    print("[place_handler] Reached PLACE position.")
    gripper.open()