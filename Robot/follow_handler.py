import time
import sys
import zmq
from pathlib import Path
from typing import Dict, Optional
from camera_to_robot_transform import CameraToRobotTransformer

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
        sub = CameraSubscriber('tcp://localhost:5556')
        objects = sub.receive()  # blockierend
    """

    def __init__(self, address: str, topic: str = "coordinates"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topic = topic
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
        self.socket.connect(address)

    def receive(self, timeout_ms: Optional[int] = None) -> Optional[Dict]:
        """Wartet blockierend (oder mit Timeout) auf die nächste Nachricht und
        gibt ein Objekt als Dict zurück.

        Args:
            timeout_ms: Optionaler Timeout in Millisekunden (None = blockierend)

        Returns:
            Dict mit den Feldern aus Object3D_msg oder None bei Timeout/Fehler.
        """
        if timeout_ms is not None:
            self.socket.RCVTIMEO = int(timeout_ms)

        try:
            parts = self.socket.recv_multipart()
        except zmq.Again:
            return None

        if len(parts) < 2:
            return None

        topic_msg, data_msg = parts[0], parts[1]
        topic = topic_msg.decode("utf-8", errors="replace")
        if topic != self.topic:
            return None

        if not data_msg:
            return None

        obj_msg = pb2.Object3D_msg()
        try:
            obj_msg.ParseFromString(data_msg)
        except Exception:
            return None

        return {
            'x': obj_msg.x,
            'y': obj_msg.y,
            'z': obj_msg.z,
            'orientation': obj_msg.orientation,
            'width': obj_msg.width,
            'length': obj_msg.length,
            'height': obj_msg.height,
            'label': obj_msg.label,
        }

def recive(transformer: CameraToRobotTransformer, sub: CameraSubscriber):
    while True:
        obj = sub.receive()
        if obj is None:
            continue

        print(f"[follow_handler] Object center [mm]: X={obj['x']:.3f}, Y={obj['y']:.3f}, Z={obj['z']:.3f}")
        pos_y = obj['y']/1000
        bx, by, bz = transformer.camera_point_to_base(obj['x'], obj['y'], obj['z'])
        print(f"[follow_handler] Object center [base,m]: X={bx:.4f}, Y={by:.4f}, Z={bz:.4f}")
        return bx, by, pos_y

def _apply_position_correction(base_y: float, object_speed_y: float, dt_s: float) -> float:
    return base_y + (object_speed_y * dt_s)


def follow(rtde_c, rtde_r, object_speed=0.1, robot_step_time=0.1):
    # Einfacher Test: Nachrichten auf localhost:5556 empfangen und ausgeben
    sub = CameraSubscriber('tcp://localhost:5556')
    transformer = CameraToRobotTransformer(rtde_receiver=rtde_r)
    print("[follow_handler] Waiting for 'coordinates' messages on tcp://localhost:5556...")
    measurement_ts = time.monotonic()
    bx, by, pos_y = recive(transformer, sub)
    stop_time = ((0.03436+abs(pos_y))/object_speed)+0.4
    print(f"[follow_handler] Calculated stop time: {stop_time:.3f}s based on pos_y={pos_y:.3f}m and object_speed={object_speed:.3f}m/s")
    time.sleep(stop_time)
    # actual_TCP = rtde_r.getActualTCPPose()
    # print("[follow_handler] TCP Pos: ", actual_TCP)

    # dt_to_motion = time.monotonic() - measurement_ts
    # print(f"[follow_handler] Time until motion start: {dt_to_motion:.3f}s")
    # object_speed_y = object_speed
    # pos_y_corrected = _apply_position_correction(pos_y, object_speed_y, dt_to_motion)

    # new_pose = actual_TCP.copy()
    # new_pose[0] = pos_x
    # new_pose[2] = 0.1
    # new_pose[1] = pos_y_corrected
    # print(f"[follow_handler] Y correction: dt={dt_to_motion:.3f}s, v_obj={object_speed_y:.3f}m/s -> y={pos_y_corrected:.4f}m")
    # print("[follow_handler] Moving to new pose: ", new_pose)
    # rtde_c.moveL(new_pose, 0.7, 0.1)
    # actual_TCP = rtde_r.getActualTCPPose()
    # print("TCP Pos: ", actual_TCP)
    # rtde_c.speedL([0, 1, -1, 0, 0, 0], object_speed, robot_step_time)
    # change_direction(rtde_r, rtde_c)
    # stop(rtde_c)
    # rtde_c.speedL([0, 1, 0, 0, 0, 0], object_speed, robot_step_time)
    # stopping()
    # actual_TCP = rtde_r.getActualTCPPose()
    # print("TCP Pos: ", actual_TCP)


def stop(rtde_c):
    rtde_c.speedStop(0.1)

def change_direction(rtde_r, rtde_c):
    while True:
        t_start = rtde_c.initPeriod()
        actual_TCP = rtde_r.getActualTCPPose()
        # print("TCP Pos: ", actual_TCP)
        if actual_TCP[2] < 0.25:  # Beispielbedingung zum Stoppen
            print("TCP Pos: ", actual_TCP)
            print("Stopping condition met.")
            break
        rtde_c.waitPeriod(t_start)

def stopping():
    time.sleep(1)
    return True
