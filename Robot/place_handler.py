import yaml
from pathlib import Path
import save_pos

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
    print(f"[place_handler] Moving to PLACE position: {PLACE_TCP_POS}")
    if save_pos.is_save_position(PLACE_TCP_POS[:3]):
        rtde_c.moveL(PLACE_TCP_POS, 0.8, 0.5)
    else:
        print(f"[place_handler] Zielposition {PLACE_TCP_POS[:3]} ist außerhalb des Arbeitsbereichs. Bewegung wird abgebrochen.")
    print("[place_handler] Reached PLACE position.")
    gripper.open()