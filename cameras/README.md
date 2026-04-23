# Kamera-Package

Dieses Package umfasst die kamerabasierte Objekterkennung des Greifsystems. Es verarbeitet die Bild- und Tiefendaten zweier Intel-RealSense-Kameras, erkennt Objekte auf dem Förderband, verfolgt sie über mehrere Frames und stellt die berechneten Daten über ZeroMQ für die weitere Roboterlogik bereit.

Dabei sind die beiden Kameras klar getrennt:

- Die statische Kamera beobachtet das Förderband, erkennt Objekte und bestimmt ihre Lage im Roboterkoordinatensystem.
- Die Roboterkamera sitzt nah am Greifer und liefert kurz vor dem Zugriff eine lokale Positionsinformation für das aktuell zu greifende Objekt.

## Zweck des Packages

Es soll:

- Objekte auf dem Förderband segmentieren und als 3D-Objekte beschreiben.
- Position, Orientierung, Größe, Farbe und Förderbandgeschwindigkeit abschätzen.
- erkannte Objekte tracken und mit stabilen IDs versehen.
- die Ergebnisse an andere Komponenten des Systems über ZeroMQ publizieren.

## Systemüberblick

Der Ablauf im Gesamtsystem sieht vereinfacht so aus:

1. `camera_static` liest Farb- und Tiefenbilder der fest montierten Kamera ein.
2. Aus den Tiefendaten werden Objektmasken, 3D-Eckpunkte, Objektmitte, Orientierung und Abmessungen berechnet.
3. `tracker.cpp` ordnet neue Detektionen bestehenden Objekten zu und schätzt die Bewegung entlang des Förderbands.
4. Die statische Kamera publiziert die aktuelle Objektliste auf dem Topic `obj_list`.
5. `camera_robot` empfängt diese Objektliste, verwendet das erste Objekt als Referenz und bestimmt mit der Roboterkamera einen lokalen 3D-Punkt für den Greifvorgang.
6. Die Roboterkamera publiziert diese lokale Zielposition auf dem Topic `coordinates`.

## Struktur des Packages

```text
cameras/
|-- camera_reader_base.hpp/.cpp   Gemeinsame Basis für Kamera, Konfiguration und ZeroMQ
|-- camera_static.hpp/.cpp        Verarbeitung der fest montierten Kamera
|-- camera_robot.hpp/.cpp         Verarbeitung der Kamera am Roboter
|-- tracker.hpp/.cpp              Tracking und Geschwindigkeitsabschätzung
|-- color_estimation.hpp          Farbkategorie aus HSV-Werten
|-- Object3D.hpp                  Interne Objektbeschreibung
|-- config_cam_static.yml         Konfiguration der statischen Kamera
|-- config_cam_robot.yml          Konfiguration der Roboterkamera
|-- camera_static_main.cpp        Startpunkt für `camera_static`
|-- camera_robot_main.cpp         Startpunkt für `camera_robot`
```

Zusätzlich wird für die Kommunikation das Protobuf-Schema (objects_3D.proto) verwendet.

## Zentrale Komponenten

### `BaseCameraReader`

Die Klasse `BaseCameraReader` in `camera_reader_base.hpp` und `camera_reader_base.cpp` kapselt die gemeinsame Infrastruktur:

- Laden der YAML-Konfiguration
- Initialisierung der RealSense-Kamera über Seriennummer
- Bereitstellung des ZeroMQ-Publishers
- gemeinsame Hilfsfunktionen für Objektzentrum, Orientierung und Versand
- Hauptschleife über `spin()`, die fortlaufend `processFrames()` aufruft

Die eigentliche Bildverarbeitung ist absichtlich als virtuelle Methode `processFrames()` ausgelegt und wird von den konkreten Kameraklassen implementiert.

### `StaticCamera`

Die Klasse `StaticCamera` in `camera_static.cpp` ist für die globale Objekterkennung über dem Förderband zuständig.

Ihre Hauptaufgaben sind:

- ROI aus dem Kamerabild ausschneiden
- Objekte über Tiefenschwellen segmentieren
- Konturen und minimale umschreibende Rechtecke bestimmen
- 3D-Eckpunkte aus Tiefenwerten rekonstruieren
- Objektzentrum, Orientierung, Länge, Breite und Höhe berechnen
- eine einfache Farbkategorie bestimmen
- erkannte Objekte an den Tracker übergeben
- aktive Tracks als `obj_list` publizieren

### `Tracker`

Der Tracker in `tracker.cpp` verwaltet stabile Objekt-IDs zwischen mehreren Frames.

Er übernimmt:

- Zuordnung neuer Detektionen zu vorhandenen Tracks
- Vorhersage entlang der Förderbandrichtung
- Schätzung der Geschwindigkeit in y-Richtung
- Weiterführen temporär unsichtbarer Objekte

Dadurch steht der nachfolgenden Roboterlogik nicht nur eine Einzelmessung, sondern eine zeitlich stabile Objektliste zur Verfügung.

### `RobotCamera`

Die Klasse `RobotCamera` in `camera_robot.cpp` verarbeitet die Kamera am Roboter.

Sie:

- abonniert die von `camera_static` publizierte Objektliste auf `tcp://127.0.0.1:5555`
- übernimmt aktuell das erste Objekt der Liste als Referenzobjekt
- segmentiert in der Roboterkamera das Objekt am oberen Bildrand
- bestimmt daraus einen repräsentativen 3D-Punkt für den Greifzeitpunkt
- publiziert diesen Punkt auf dem Topic `coordinates`

## Datenmodell

Die interne Objektbeschreibung ist in `Object3D.hpp` definiert. Ein Objekt kann folgende Informationen tragen:

- `id`
- `label`
- `x`, `y`, `z`
- `orientation`
- `width`, `length`, `height`
- `square`
- `vy`

Die Kommunikation zwischen den Prozessen verwendet Protobuf mit den Nachrichten `Object3D_msg` und `Objects3D_msg` aus `objects_3D.proto`.

## ZeroMQ-Schnittstellen

Das Package verwendet zwei Publisher-Topics:

- `camera_static` publiziert eine komplette Objektliste auf Topic `obj_list` über Port `5555`.
- `camera_robot` publiziert Zielkoordinaten auf Topic `coordinates` über Port `5556`.

Wichtig für die Nutzung:

- `obj_list` enthält die vom statischen Kamerapfad erzeugten Objektzustände mit ID, Pose, Größe, Farbe und Geschwindigkeit.
- `coordinates` verwendet ebenfalls `Object3D_msg`, setzt aktuell aber nur `x`, `y` und `z` explizit.

## Konfiguration

Die wichtigsten Parameter stehen in `config_cam_static.yml` und `config_cam_robot.yml`.

Wichtige Felder sind:

- `serial_number`: Seriennummer der zu verwendenden RealSense-Kamera
- `zmq_port`: Port des jeweiligen Publishers
- `debug`: Aktiviert Konsolenausgaben und OpenCV-Fenster
- `roi`: Bildausschnitt für die Verarbeitung der statischen Kamera
- `conveyor_z_dist`: Referenzabstand des Förderbands
- `min_obj_height` und `max_obj_height_mm`: Höhenbereich für gültige Objekte
- `min_contour_area`: Mindestfläche für gültige Konturen
- `pos_tol` und `orientation_tol`: Toleranzen für Wiedererkennung und Tracking
- `calibration`: Extrinsische Transformation von Kamerakoordinaten in das Roboterkoordinatensystem

Beim CMake-Konfigurieren werden die YAML-Dateien in das Build-Verzeichnis kopiert. Die Executables werden standardmäßig mit den Dateinamen `config_cam_static.yml` und `config_cam_robot.yml` gestartet.

## Build

Das Projekt wird über CMake gebaut. Aus dem Wurzelverzeichnis des Repositories:

```bash
cmake -S . -B build
cmake --build build -j
```

Dabei entstehen unter anderem die beiden Executables:

- `build/camera_static`
- `build/camera_robot`

## Nutzung

### 1. Statische Kamera starten

```bash
./build/camera_static
```

Dieser Prozess erkennt und trackt die Objekte auf dem Förderband und sendet die Objektliste an Topic `obj_list`.

### 2. Roboterkamera starten

```bash
./build/camera_robot
```

Dieser Prozess liest die Objektliste der statischen Kamera ein, bestimmt den lokalen Greifpunkt und publiziert ihn auf Topic `coordinates`.

### 3. Verarbeitung beobachten

Bei aktivem `debug` werden OpenCV-Fenster und Konsolenausgaben angezeigt. Beide Programme laufen in einer Schleife und können mit `q` oder `ESC` beendet werden.

## Koordinaten und Einheiten

Für das Verständnis der Ausgaben sind folgende Punkte wichtig:

- Tiefendaten der RealSense werden zunächst in Kamerakoordinaten rekonstruiert.
- Die statische Kamera transformiert 3D-Punkte anschließend in das Roboterkoordinatensystem.
- Positionen werden im restlichen Datenmodell überwiegend in Millimetern weitergegeben.
- Orientierungen werden in Radiant verarbeitet.
