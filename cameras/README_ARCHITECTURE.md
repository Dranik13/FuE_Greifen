# Multi-Camera Architecture

## Overview

Diese Refaktorierung implementiert eine **abstrakte Basis-Klasse** für Multi-Kamera-Support:

- **BaseCameraReader**: Abstrakte Basis-Klasse mit gemeinsamen Funktionen
- **CameraReader1**: Spezialisierung für Kamera am Förderband
- **CameraReader2**: Spezialisierung für fixe Kamera (Template)

## Dateien

```
cameras/
├── BaseCameraReader.hpp           # Abstrakte Schnittstelle
├── BaseCameraReader.cpp           # Gemeinsamer Code
├── CameraReader1.hpp              # Förderband-Kamera
├── CameraReader1.cpp              # Förderband-Logik (z > 60mm Filter)
├── CameraReader2.hpp              # Fixe Kamera (Template)
├── CameraReader2.cpp              # Fixe Kamera Logik (z 100-500mm)
├── camera_reader_main.cpp         # Hauptprogramm (Backward-Compat)
├── camera_reader1_main.cpp        # CameraReader1 Programm
├── camera_reader2_main.cpp        # CameraReader2 Programm
├── config.yml                     # Config für CameraReader1
└── config2.yml                    # Config für CameraReader2
```

## Build-Prozess

### 1. Abhängigkeiten installieren:
```bash
sudo apt update
sudo apt install -y build-essential cmake pkg-config \
  libopencv-dev libzmq3-dev libprotobuf-dev protobuf-compiler \
  librealsense2-dev librealsense2-utils
```

### 2. Protobuf-Datei generieren (falls nötig):
```bash
cd /home/tetripick/UR10_Pick_ws/zeroMQ
protoc --python_out=. objects_3D.proto
```

### 3. Build:
```bash
cd /home/tetripick/UR10_Pick_ws
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel
```

### 4. Ausführen:

**Kamera 1 (Förderband):**
```bash
./build/camera_reader1
# oder mit Backward-Compatibility:
./build/camera_reader
```

**Kamera 2 (Fixe Kamera):**
```bash
./build/camera_reader2
```

**Beide parallel:**
```bash
./build/camera_reader1 &
./build/camera_reader2 &
```

## Architektur-Vorteile

| Feature | Nutzen |
|---------|---------|
| **Abstrakte Basis** | Code-Sharing, z.B. RealSense Init, ZMQ |
| **Spezialisierte Subklassen** | Unterschiedliche `processFrames()` Logik |
| **Separate Configs** | Jede Kamera hat eigene Parameter |
| **Saubere Struktur** | Einfach erweiterbar (3. Kamera = neue Subklasse) |
| **Unabhängige Executables** | Können parallel laufen |

## Anpassungen für deine zweite Kamera

In `CameraReader2.cpp` findest du TODOs zur Anpassung:

```cpp
// TODO: Implementiere hier eigene Logik für CameraReader2
// z.B.:
// - Andere Objekterkennungsalgorithmen
// - Andere Filter
// - Andere Ausgabe/ZMQ-Port
```

Beispiele:
- **Anderer ZMQ-Port**: `socket_.bind("tcp://*:5556");` in Konstruktor
- **Andere Filter**: Eigene Algorithmen in `processFrames()`
- **Andere Tiefengrenzen**: Custom Depth Processing

## Integration mit Robot.py

Die Python-Klasse `CameraSubscriber` in [Robot.py](../Robot/Robot.py) empfängt von beiden Kameras über ZMQ:

```python
from Robot import CameraSubscriber

# Von CameraReader1 (Port 5555)
sub1 = CameraSubscriber('tcp://localhost:5555')
objects1 = sub1.receive()

# Von CameraReader2 (Port 5556 - falls angepasst)
sub2 = CameraSubscriber('tcp://localhost:5556')
objects2 = sub2.receive()
```

## Debugging

Aktiviere `debug: 1` in `config.yml` oder `config2.yml`, um:
- Erkannte Objekte zu visualisieren
- Konsolenausgaben zu sehen
- Filter-Vorgänge zu tracen

```bash
./build/camera_reader1    # Bei debug=1: OpenCV Fenster öffnen
```

## Nächste Schritte

1. **Kalibriere CameraReader2**: Passe `config2.yml` an (ROI, ref_pt, Tiefenwerte)
2. **Fein-Tuning**: Teste verschiedene Canny-Schwellwerte
3. **Integration**: Verbinde beide Kameras mit Roboter über Robot.py
4. **Multi-Threading** (optional): Starte beide im gleichen Prozess mit std::thread
