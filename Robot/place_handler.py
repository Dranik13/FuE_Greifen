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
        raise ValueError("[place_handler] Invalid or missing 'Move_to_Place -> TCP Pos' values in pose.yaml")

    return [float(value) for value in tcp_pos]

PLACE_TCP_POS = _load_place_tcp_pos()

def place(rtde_c, gripper, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    if debug:
        print(f"[place_handler] Moving to PLACE position: {PLACE_TCP_POS}")
    if save_pos.is_save_position(PLACE_TCP_POS[:3]):
        rtde_c.moveL(PLACE_TCP_POS, robot_speed, robot_acceleration)
    else:
        print(f"[place_handler] Target position {PLACE_TCP_POS[:3]} is outside the workspace. Movement aborted.")
    if debug:
        print("[place_handler] Reached PLACE position.")
    gripper.open()