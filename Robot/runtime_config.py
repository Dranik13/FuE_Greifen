from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass(frozen=True)
class RuntimeConfig:
    debug: bool = True
    robot_speed: float = 0.8
    robot_acceleration: float = 0.5
    robot_ip: str = "192.168.96.221"
    

def _as_bool(value, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    return default


def _as_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_str(value, default: str) -> str:
    if value is None:
        return default
    return str(value)


def load_runtime_config(config_path: Optional[Path] = None) -> RuntimeConfig:
    path = config_path or Path(__file__).with_name("config.yaml")

    if not path.exists():
        return RuntimeConfig()

    with path.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}

    return RuntimeConfig(
        debug=_as_bool(data.get("debug"), RuntimeConfig.debug),
        robot_speed=_as_float(data.get("robot_speed"), RuntimeConfig.robot_speed),
        robot_acceleration=_as_float(data.get("robot_acceleration"), RuntimeConfig.robot_acceleration),
        robot_ip=_as_str(data.get("robot_ip"), RuntimeConfig.robot_ip),
    )