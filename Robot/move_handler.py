from pathlib import Path
import yaml


def _load_kamera_2_kalib_tcp_pos():
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    start_conveyor = data.get("Kamera_2_Kalib", {})
    tcp_pos = start_conveyor.get("TCP Pos")
    if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
        raise ValueError("[move_handler] Ungültige oder fehlende 'Kamera_2_Kalib -> TCP Pos' Werte in pose.yaml")

    return [float(value) for value in tcp_pos]

KAMERA_2_KALIB_TCP_POS = _load_kamera_2_kalib_tcp_pos()

def move(pos_x, rtde_r, rtde_c, object_speed):
    actual_TCP = rtde_r.getActualTCPPose()
    print("TCP Pos: ", actual_TCP)
    print(f"[move_handler] KAMERA_2_KALIB_TCP_POS[1] : {KAMERA_2_KALIB_TCP_POS[1]}")
    new_y = KAMERA_2_KALIB_TCP_POS[1] + (object_speed*3)
    print(f"[move_handler] new_y: {new_y}")
    new_x = KAMERA_2_KALIB_TCP_POS[0] + (abs(pos_x / 1000))
    print(f"[move_handler] new_x: {new_x}")
    target_tcp = KAMERA_2_KALIB_TCP_POS.copy()
    target_tcp[0] = new_x
    target_tcp[1] = new_y
    target_tcp[2] = 0.10
    print(f"[move_handler] Moving to new TCP: {target_tcp}")
    # new_pos = rtde_c.getInverseKinematics(target_tcp)
    # print(f"[move_handler] new_pos: {new_pos}")
    rtde_c.moveL(target_tcp, 0.8, 0.2)