"""
camera_sub.py
----------------
Provides the CameraSubscriber class for subscribing to object detection messages from different camera sources (static and robot camera).
Handles different message formats for each port (5555 and 5556).

Example usage:
    from camera_sub import CameraSubscriber
    
    # For static camera (port 5555):
    sub = CameraSubscriber('tcp://localhost:5555')
    objects = sub.receive_5555()

    # For robot camera (port 5556):
    sub = CameraSubscriber('tcp://localhost:5556', topic='coordinates')
    obj = sub.receive_5556()
"""

import sys
import zmq
from pathlib import Path
from typing import List, Dict, Optional
from pathlib import Path

# Try to load the generated Python-Protobuf module from the zeroMQ folder
proto_dir = Path(__file__).parent.parent / "zeroMQ"
if str(proto_dir) not in sys.path:
    sys.path.insert(0, str(proto_dir))

try:
    import objects_3D_pb2 as pb2
except Exception as e:
    raise ImportError(
        "[camera_sub] Cannot import 'objects_3D_pb2'. Generate the Python-Protobuf file with:\n"
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

    def __init__(self, address: str, topic: str = ""):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.topic = topic
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
        self.socket.connect(address)


    def receive_5555(self, timeout_ms: Optional[int] = None) -> Optional[List[Dict]]:
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
    
    def receive_5556(self, timeout_ms: Optional[int] = None) -> Optional[Dict]:
        """
        Waits (blocking or with timeout) for the next message and returns an object as a dict.

        Args:
            timeout_ms: Optional timeout in milliseconds (None = blocking).

        Returns:
            Tuple of (dict with fields from Object3D_msg, stop flag) or (None, stop) on timeout/error.
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