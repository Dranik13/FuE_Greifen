import time
import sys
import zmq
import yaml
from pathlib import Path
from typing import Dict, Optional
from camera_to_robot_transform import CameraToRobotTransformer


def _load_camera_mount_to_camera_distance():
    pose_file = Path(__file__).with_name("Calibration_results_final.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    camera_mount_to_camera = data.get("camera_mount_to_camera", {})
    camera_to_mount_distance = camera_mount_to_camera.get("x")
    # print(f"[follow_handler] Loaded camera_to_mount_distance from YAML: {camera_to_mount_distance}")
    if isinstance(camera_to_mount_distance, list):
        if len(camera_to_mount_distance) != 1:
            raise ValueError("[follow_handler] Invalid values for 'camera_mount_to_camera -> x' in Calibration_results_final.yaml (expected: 1 value)")
        return float(camera_to_mount_distance[0])

    try:
        return float(camera_to_mount_distance)
    except (TypeError, ValueError):
        raise ValueError("[follow_handler] Invalid or missing value for 'camera_mount_to_camera -> x' in Calibration_results_final.yaml")


distance_to_camera = _load_camera_mount_to_camera_distance()


# Try to load the generated Python-Protobuf module from the zeroMQ folder
proto_dir = Path(__file__).parent.parent / "zeroMQ"
if str(proto_dir) not in sys.path:
    sys.path.insert(0, str(proto_dir))


try:
    import objects_3D_pb2 as pb2
except Exception as e:
    raise ImportError(
        "[follow_handler] Cannot import 'objects_3D_pb2'. Generate the Python-Protobuf file with:\n"
        "protoc --python_out=zeroMQ objects_3D.proto\n"
        "from the directory '/home/tetripick/UR10_Pick_ws/zeroMQ'.\n"
        f"Error: {e}"
    )


class CameraSubscriber:
    """Python equivalent of the C++ ZeroMQ subscriber.

    Example:
        sub = CameraSubscriber('tcp://localhost:5556')
        objects = sub.receive()  # blocking
    """

    def __init__(self, address: str, topic: str = "coordinates"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topic = topic
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
        self.socket.connect(address)


    def receive(self, timeout_ms: Optional[int] = None) -> Optional[Dict]:
        """Waits blocking (or with timeout) for the next message and
        returns an object as a Dict.

        Args:
            timeout_ms: Optional timeout in milliseconds (None = blocking)

        Returns:
            Dict with the fields from Object3D_msg or None on timeout/error.
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


def receive(transformer: CameraToRobotTransformer, sub: CameraSubscriber, debug=False):
    while True:
        obj = sub.receive()
        if obj is None:
            continue

        if debug:
            print(f"[follow_handler] Object center [mm]: X={obj['x']:.3f}, Y={obj['y']:.3f}, Z={obj['z']:.3f}")
        pos_y = obj['y']/1000
        # Transformation in Robot coordinates
        # bx, by, bz = transformer.camera_point_to_base(obj['x'], obj['y'], obj['z'])
        # print(f"[follow_handler] Object center [base,m]: X={bx:.4f}, Y={by:.4f}, Z={bz:.4f}")
        return pos_y


def follow(rtde_c, rtde_r, object_speed=0.1, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    # Simple test: receive and print messages on localhost:5556
    sub = CameraSubscriber('tcp://localhost:5556')
    transformer = CameraToRobotTransformer(rtde_receiver=rtde_r)
    if debug:
        print("[follow_handler] Waiting for 'coordinates' messages on tcp://localhost:5556...")
    pos_y = receive(transformer, sub, debug=debug)
    stop_time = ((distance_to_camera + abs(pos_y)) / object_speed)
    if debug:
        print(f"[follow_handler] Calculated stop time: {stop_time:.3f}s based on pos_y={pos_y:.3f}m and object_speed={object_speed:.3f}m/s")
    time.sleep(stop_time)


def stop(rtde_c):
    rtde_c.speedStop(0.1)


def stopping():
    time.sleep(1)
    return True