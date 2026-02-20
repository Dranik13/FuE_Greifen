from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

import numpy as np
import yaml


def _rodrigues(rotation_vector: Sequence[float]) -> np.ndarray:
    rv = np.asarray(rotation_vector, dtype=float)
    theta = np.linalg.norm(rv)
    if theta < 1e-12:
        return np.eye(3)

    axis = rv / theta
    kx, ky, kz = axis
    k_matrix = np.array(
        [[0.0, -kz, ky], [kz, 0.0, -kx], [-ky, kx, 0.0]],
        dtype=float,
    )
    return np.eye(3) + np.sin(theta) * k_matrix + (1.0 - np.cos(theta)) * (k_matrix @ k_matrix)


def _homogeneous_from_xyz_rvec(x: float, y: float, z: float, rx: float, ry: float, rz: float) -> np.ndarray:
    transform = np.eye(4)
    transform[:3, :3] = _rodrigues((rx, ry, rz))
    transform[:3, 3] = [x, y, z]
    return transform


def _homogeneous_from_yaml_pose(pose_data: dict) -> np.ndarray:
    qw = float(pose_data["qw"])
    qx = float(pose_data["qx"])
    qy = float(pose_data["qy"])
    qz = float(pose_data["qz"])

    rotation = np.array(
        [
            [1.0 - 2.0 * (qy * qy + qz * qz), 2.0 * (qx * qy - qz * qw), 2.0 * (qx * qz + qy * qw)],
            [2.0 * (qx * qy + qz * qw), 1.0 - 2.0 * (qx * qx + qz * qz), 2.0 * (qy * qz - qx * qw)],
            [2.0 * (qx * qz - qy * qw), 2.0 * (qy * qz + qx * qw), 1.0 - 2.0 * (qx * qx + qy * qy)],
        ],
        dtype=float,
    )

    transform = np.eye(4)
    transform[:3, :3] = rotation
    transform[:3, 3] = [float(pose_data["x"]), float(pose_data["y"]), float(pose_data["z"])]
    return transform


class CameraToRobotTransformer:
    """Rechnet Kamera-Koordinaten ins Roboter-Basis-Koordinatensystem um.

    Erwartete Kette:
        base_T_object = base_T_mount @ mount_T_camera @ camera_T_object
    """

    def __init__(
        self,
        rtde_receiver,
        calibration_file: Optional[Path] = None,
        coordinates_in_mm: bool = True,
    ):
        self.rtde_receiver = rtde_receiver
        self.coordinates_in_mm = coordinates_in_mm

        if calibration_file is None:
            calibration_file = Path(__file__).with_name("Calibration_results_final.yaml")

        with open(calibration_file, "r", encoding="utf-8") as file:
            calibration_data = yaml.safe_load(file)

        self.mount_t_camera = _homogeneous_from_yaml_pose(calibration_data["camera_mount_to_camera"])

    def camera_point_to_base(
        self,
        x: float,
        y: float,
        z: float,
        tcp_pose: Optional[Iterable[float]] = None,
    ) -> Tuple[float, float, float]:
        """Konvertiert einen 3D-Punkt aus dem Kamera-Frame in den Base-Frame."""
        if self.coordinates_in_mm:
            x, y, z = x / 1000.0, y / 1000.0, z / 1000.0

        if tcp_pose is None:
            tcp_pose = self.rtde_receiver.getActualTCPPose()

        base_t_mount = _homogeneous_from_xyz_rvec(*tcp_pose)
        point_camera = np.array([x, y, z, 1.0], dtype=float)
        point_base = base_t_mount @ self.mount_t_camera @ point_camera
        return float(point_base[0]), float(point_base[1]), float(point_base[2])
