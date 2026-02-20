import sys
import zmq
from pathlib import Path
from typing import List, Dict, Optional
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
        raise ValueError("[idle_handler] Ungültige oder fehlende 'Start_Conveyor -> TCP Pos' Werte in pose.yaml")

    return [float(value) for value in tcp_pos]

START_CONVEYOR_TCP_POS = _load_start_conveyor_tcp_pos()

pos_x = 0
# Versuche das generierte Python-Protobuf-Modul aus dem zeroMQ-Ordner zu laden
proto_dir = Path(__file__).parent.parent / "zeroMQ"
if str(proto_dir) not in sys.path:
    sys.path.insert(0, str(proto_dir))

try:
    import objects_3D_pb2 as pb2
except Exception as e:
    raise ImportError(
        "[idle_handler] Kann 'objects_3D_pb2' nicht importieren. Erzeuge die Python-Protobuf-Datei mit:\n"
        "protoc --python_out=zeroMQ objects_3D.proto\n"
        "aus dem Verzeichnis '/home/tetripick/UR10_Pick_ws/zeroMQ'.\n"
        f"Fehler: {e}"
    )


class CameraSubscriber:
    """Python-Äquivalent des C++ ZeroMQ-Subscribers.

    Beispiel:
        sub = CameraSubscriber('tcp://localhost:5555')
        objects = sub.receive()  # blockierend
    """

    def __init__(self, address: str):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        # Alle Topics abonnieren
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket.connect(address)

    def receive(self, timeout_ms: Optional[int] = None) -> Optional[List[Dict]]:
        """Wartet blockierend (oder mit Timeout) auf die nächste Nachricht und
        gibt eine Liste von Objekten als Dict zurück.

        Args:
            timeout_ms: Optionaler Timeout in Millisekunden (None = blockierend)

        Returns:
            Liste von Dicts mit den Feldern aus Object3D_msg oder None bei Timeout.
        """
        if timeout_ms is not None:
            self.socket.RCVTIMEO = int(timeout_ms)

        try:
            msg = self.socket.recv()
        except zmq.Again:
            return None

        if not msg:
            return None

        objects_msg = pb2.Objects3D_msg()
        try:
            objects_msg.ParseFromString(msg)
        except Exception:
            # Fallback: ParseFromString kann fehlschlagen, falls Wrapper oder Framing anders ist
            return None

        result = []
        for obj in objects_msg.objects:
            result.append({
                'x': obj.x,
                'y': obj.y,
                'z': obj.z,
                'orientation': obj.orientation,
                'width': obj.width,
                'length': obj.length,
                'height': obj.height,
                'label': obj.label,
            })

        return result

def recive():
    sub = CameraSubscriber('tcp://localhost:5555')
    print('[idle_handler] Waiting for messages on tcp://localhost:5555...')
    while True:
        objs = sub.receive()
        if objs is None:
            continue
        print(f'[idle_handler] Received {len(objs)} objects')
        for i, o in enumerate(objs):
            print(f"[idle_handler]  {i}: {o['label']} @ ({o['x']:.3f}, {o['y']:.3f}, {o['z']:.3f})")
            pos_x = o['x']
            print(f"[idle_handler] x in while: {pos_x}")
        return pos_x
    
def move_to_home(rtde_c):
    new_pos = rtde_c.getInverseKinematics(START_CONVEYOR_TCP_POS)
    print(f"[idle_handler] Moving to Home position: {new_pos}")
    rtde_c.moveJ(new_pos, 0.2, 0.1)
    print("[idle_handler] Reached Home position.")

def idle(rtde_c):
    move_to_home(rtde_c)
    return recive()