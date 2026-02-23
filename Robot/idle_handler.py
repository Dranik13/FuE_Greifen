import sys
import save_pos
import zmq
from pathlib import Path
from typing import List, Dict, Optional
from pathlib import Path
import yaml


def _load_start_conveyor_tcp_pos():
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    start_conveyor = data.get("Start_Conveyor", {})
    tcp_pos = start_conveyor.get("TCP Pos")
    if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
        raise ValueError("[idle_handler] Invalid or missing 'Start_Conveyor -> TCP Pos' values in pose.yaml")

    return [float(value) for value in tcp_pos]


START_CONVEYOR_TCP_POS = _load_start_conveyor_tcp_pos()
id_counter = 1
pos_x = 0


# Try to load the generated Python-Protobuf module from the zeroMQ folder
proto_dir = Path(__file__).parent.parent / "zeroMQ"
if str(proto_dir) not in sys.path:
    sys.path.insert(0, str(proto_dir))


try:
    import objects_3D_pb2 as pb2
except Exception as e:
    raise ImportError(
        "[idle_handler] Cannot import 'objects_3D_pb2'. Generate the Python-Protobuf file with:\n"
        "protoc --python_out=zeroMQ objects_3D.proto\n"
        "from the directory '/home/tetripick/UR10_Pick_ws/zeroMQ'.\n"
        f"Error: {e}"
    )


class CameraSubscriber:
    """Python equivalent of the C++ ZeroMQ subscriber.

    Example:
        sub = CameraSubscriber('tcp://localhost:5555')
        objects = sub.receive()  # blocking
    """

    def __init__(self, address: str):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        # Subscribe to all topics
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.socket.connect(address)


    def receive(self, timeout_ms: Optional[int] = None) -> Optional[List[Dict]]:
        """Waits blocking (or with timeout) for the next message and
        returns a list of objects as Dicts.

        Args:
            timeout_ms: Optional timeout in milliseconds (None = blocking)

        Returns:
            List of Dicts with the fields from Object3D_msg or None on timeout.
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
                'id': obj.id,
                'x': obj.x,
                'y': obj.y,
                'z': obj.z,
                'orientation': obj.orientation,
                'width': obj.width,
                'length': obj.length,
                'height': obj.height,
                'label': obj.label,
                'vy': obj.vy,
            })
        return result


def receive(debug=False, gripper=None):
    sub = CameraSubscriber('tcp://localhost:5555')
    if debug:
        print('[idle_handler] Waiting for messages on tcp://localhost:5555...')
    global id_counter
    counter = 0
    speed = []
    while True:
        objs = sub.receive()
        if objs is None:
            continue
        # print(f'[idle_handler] Received objects: {objs}')
        objs = next((o for o in objs if o.get("id") == id_counter), None)
        if objs is None:
            continue
        # print(f'[idle_handler] Filtered objects: {objs}')
        # for i, o in enumerate(objs):
        # print(f"[idle_handler]  {objs['label']} @ ({objs['x']:.3f}, {objs['y']:.3f}, {objs['z']:.3f}), vy={objs.get('vy', 0):.3f}")
        object_speed = objs.get('vy', 0)  # Geschwindigkeit in y-Richtung
        object_speed = object_speed/1000
        pos_x = objs['x']
        pos_y = objs['y']
        width = objs['width']
        if object_speed >= 0.05:
            counter += 1
            if counter >= 7:
                speed.append(object_speed)
            if counter >= 10:  # wait for multiple measurements with speed to reduce noise
                object_speed = sum(speed) / (len(speed))  # mean last 3 measurements
                break
    if debug:
        print(f"[idle_handler] x, y and speed from Camera: {pos_x},{pos_y}, vy: {object_speed}")
        print(f"[idle_handler] gripper: {gripper}, width: {width}")
        
    if gripper is not None:
        gripper.goTomm(int(width)+20) # Close the gripper based on the measured width + some tolerance
        if debug:
            print(f"[idle_handler] Gripper closed with width: {width+20}")
    id_counter += 1
    return pos_x, pos_y, object_speed
    

def move_to_home(rtde_c, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    if save_pos.is_save_position(START_CONVEYOR_TCP_POS[:3]):
        if debug:
            print(f"[idle_handler] Moving to Home position: {START_CONVEYOR_TCP_POS}")
        rtde_c.moveL(START_CONVEYOR_TCP_POS, robot_speed, robot_acceleration)
        if debug:
            print("[idle_handler] Reached Home position.")
    else:
        if debug:
            print(f"[idle_handler] target position {START_CONVEYOR_TCP_POS[:3]} is outside the workspace. Movement aborted.")


def idle(rtde_c, robot_speed=0.8, robot_acceleration=0.5, gripper=None, debug=False):
    global id_counter
    if id_counter == 1:
        if debug:
            print("[idle_handler] First ID, moving to Home position.")
        move_to_home(rtde_c, robot_speed=robot_speed, robot_acceleration=robot_acceleration, debug=debug)
    return receive(debug=debug, gripper=gripper)