import sys
import zmq
from pathlib import Path
from typing import List, Dict, Optional
import rtde_receive
import rtde_control

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.96.221")
rtde_c = rtde_control.RTDEControlInterface("192.168.96.221")
pos_x = 0
# Versuche das generierte Python-Protobuf-Modul aus dem zeroMQ-Ordner zu laden
proto_dir = Path(__file__).parent.parent / "zeroMQ"
if str(proto_dir) not in sys.path:
    sys.path.insert(0, str(proto_dir))

try:
    import objects_3D_pb2 as pb2
except Exception as e:
    raise ImportError(
        "Kann 'objects_3D_pb2' nicht importieren. Erzeuge die Python-Protobuf-Datei mit:\n"
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
    while True:
        objs = sub.receive()
        if objs is None:
            continue
        print(f'Received {len(objs)} objects')
        for i, o in enumerate(objs):
            print(f" {i}: {o['label']} @ ({o['x']:.3f}, {o['y']:.3f}, {o['z']:.3f})")
            pos_x = o['x']
            print("x in while", pos_x)
        return pos_x

if __name__ == '__main__':
    # Einfacher Test: Nachrichten auf localhost:5555 empfangen und ausgeben
    sub = CameraSubscriber('tcp://localhost:5555')
    print('Waiting for messages on tcp://localhost:5555...')
    pos_x = recive()
    # while True:
    actual_q = rtde_r.getActualQ()
    print("Joint Pos: ", actual_q)
    print("pos x out of while", pos_x)
    new_x = 0.46987006692897526 + (abs(pos_x/1000))
    print("new_x", new_x)
    new_pos = rtde_c.getInverseKinematics([new_x, -0.6141117468652709, 0.29701407690139925, -2.2319500763632916, 2.2104305473135506, -0.0007869137174410558])
    print("new_pos", new_pos)
    rtde_c.moveJ(new_pos, 0.3, 0.15)
