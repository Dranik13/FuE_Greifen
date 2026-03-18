# Bildverarbeitung im Projekt `FuE_Greifen`

## 1. Ziel und Gesamtidee
Dieses Dokument beschreibt den Aufbau und die Funktionsweise der Bildverarbeitung in diesem Projekt. Die Loesung besteht aus zwei kooperierenden Kamerapipelines:

1. Eine **statische Kamera** ueber dem Foerderband erkennt Objekte, bestimmt ihre Geometrie und schaetzt ihre Bewegung.
2. Eine **Roboterkamera** (nahe Endeffektor) nutzt diese Informationen, lokalisiert das relevante Objekt im Nahbereich und sendet Greifkoordinaten.

Der Datenaustausch laeuft ueber **ZeroMQ** mit **Protobuf**-Nachrichten.

---

## 2. Wichtige Dateien und Verantwortlichkeiten

### Einstiegspunkte (Executables)
- `cameras/camera_static_main.cpp`: Startpunkt fuer die statische Kamera.
- `cameras/camera_robot_main.cpp`: Startpunkt fuer die Roboterkamera.

### Gemeinsame Basis
- `cameras/camera_reader_base.hpp`
- `cameras/camera_reader_base.cpp`

Diese Basisklasse kapselt Konfigurationsladen, Kamera-Initialisierung, Hauptloop und gemeinsame Hilfsfunktionen.

### Spezifische Pipelines
- `cameras/camera_static.hpp`
- `cameras/camera_static.cpp`
- `cameras/camera_robot.hpp`
- `cameras/camera_robot.cpp`

### Tracking und Datenstruktur
- `cameras/tracker.hpp`
- `cameras/tracker.cpp`
- `cameras/Object3D.hpp`

### Nachrichtenformat
- `zeroMQ/objects_3D.proto`

### Konfiguration
- `cameras/config_cam_static.yml`
- `cameras/config_cam_robot.yml`

### Build-Definition
- `CMakeLists.txt`

---

## 3. Build- und Laufzeitarchitektur
In `CMakeLists.txt` wird die gemeinsame Bibliothek `camera_base` aufgebaut. Diese Bibliothek enthaelt:

- Basislogik (`BaseCameraReader`)
- die beiden konkreten Kameraimplementierungen (`StaticCamera`, `RobotCamera`)
- den Tracker
- den generierten Protobuf-Code (`objects_3D.pb.cc`)

Darauf aufbauend entstehen zwei Programme:

1. `camera_static`
2. `camera_robot`

Beim Konfigurieren/Bauen werden die YAML-Dateien ins Build-Verzeichnis kopiert, damit die Programme dort mit den erwarteten Dateinamen starten koennen.

---

## 4. Die Basisklasse `BaseCameraReader`

### 4.1 Kernaufgaben
Die Klasse dient als technisches Rueckgrat fuer beide Kamerapipelines:

1. **Konfiguration laden** (`loadConfig`)
2. **RealSense initialisieren** (`initializeRealSense`)
3. **Dauerloop ausfuehren** (`spin`)
4. **gemeinsame Hilfsfunktionen bereitstellen**
5. **ZeroMQ-Publisher bereitstellen**

### 4.2 Initialisierung und Kameraauswahl
Beim Erzeugen eines Readers passiert in dieser Reihenfolge:

1. Konfigurationsdatei laden
2. PUB-Socket auf `tcp://*:<zmq_port>` binden
3. RealSense-Geraet ueber `serial_number` suchen und starten

Wird keine Kamera gefunden oder stimmt die Seriennummer nicht, wird dies geloggt und `running_` bleibt `false`.

### 4.3 Hauptloop
`spin()` laeuft in einer Endlosschleife und ruft immer die virtuelle Funktion `processFrames()` auf. Diese Funktion wird in den abgeleiteten Klassen implementiert.

### 4.4 Konfigurationswerte (Auszug)
Die Basis liest unter anderem:

- `debug`
- `roi` (optional)
- `conveyor_z_dist`, `min_obj_height`, `z_offset`
- `ref_pt`
- `pos_tol`, `orientation_tol`
- `zmq_port`
- `serial_number`
- `max_obj_height_mm`, `min_contour_area`
- `search_area_y_min`, `search_area_y_max`
- optional `T_cam_to_board`

Wenn Felder fehlen, werden sinnvolle Defaults gesetzt.

### 4.5 Gemeinsame Hilfen
- `computeCenter(...)`: Mittelwert eines 3D-Punktsatzes
- `computeOrientation2D(...)`: Winkel aus zwei Eckpunkten in der XY-Ebene
- `sendObjList()`: versendet die aktuelle Objektliste als `Objects3D_msg` mit Topic `obj_list`
- `sendCoordinates(...)`: versendet Zielkoordinaten als `Object3D_msg` mit Topic `coordinates`

---

## 5. Pipeline der statischen Kamera (`StaticCamera`)

### 5.1 Ziel
Die statische Kamera erkennt Objekte auf dem Foerderband, misst ihre Lage/Groesse und liefert getrackte Objekte inklusive Geschwindigkeit in y-Richtung.

### 5.2 Verarbeitungsablauf pro Zyklus
`processFrames()` in `camera_static.cpp` arbeitet grob in diesen Schritten:

1. **Frames holen und ausrichten**
   - Farb- und Tiefenframe werden geladen
   - Tiefenframe wird auf Farbframe ausgerichtet (`rs2::align`)

2. **Frame-Skipping**
   - Es wird nur jeder `FRAME_SKIP`-te Frame ausgewertet (derzeit 3), um Rechenlast zu senken.

3. **ROI anwenden**
   - Wenn ROI gesetzt ist, wird nur dieser Bereich verarbeitet.
   - Sonst wird das gesamte Bild benutzt.

4. **Referenzpunkt in 3D initialisieren (einmalig)**
   - `ref_pt` aus der YAML wird in einen 3D-Punkt deprojiziert.
   - Dieser Punkt dient als lokales Bezugskoordinatensystem fuer Objektkoordinaten.

5. **Tiefenbasierte Segmentierung**
   - Fuer jeden Pixel wird aus Tiefe ein 3D-Punkt bestimmt.
   - Punkte im erwarteten Objekthoehenbereich werden in eine Binarmaske uebernommen.

6. **Masken-Nachbearbeitung**
   - Glattziehen/Schwellwert
   - Konturen extrahieren

7. **Objektgeometrie je Kontur berechnen**
   - Minimum-Rect und 3D-Eckpunkte
   - Zentrum, Orientierung, Laenge, Breite
   - Hoehe aus mittlerer Tiefe innerhalb der Kontur
   - Filter nach gueltigem Suchbereich (`search_area_y_*`)

8. **Tracking und Geschwindigkeitsmodell**
   - Die momentanen Detektionen gehen an `tracker_.update(...)`.
   - Der Tracker weist IDs zu, schaetzt `vy` und fuehrt kurzzeitige Praediktion aus.
   - Eine geglaettete globale y-Geschwindigkeit (`filtered_velocity_y_`) dient als Fallback.

9. **Publikation**
   - Aktive Tracks werden in `obj_list_` uebernommen.
   - Versand per `sendObjList()` auf Topic `obj_list`.

### 5.3 Koordinatensystem und Einheiten
- Viele Tiefenwerte kommen zunaechst in Metern von RealSense und werden in Millimeter umgerechnet.
- `object.y` wird invertiert (`* -1000`), damit die Richtung zum Robotersystem passt.

---

## 6. Tracker-Logik (`Tracker`)

### 6.1 Ziel
Der Tracker sorgt fuer stabile Objekt-IDs ueber Zeit und liefert eine robustere Bewegungsschaetzung als Einzelbilder.

### 6.2 Matching-Strategie
- Greedy Nearest-Neighbor in 3D
- Distanzgrenze: `max_match_distance_mm`
- Track-Praediktion nutzt vorhandenes `vy` oder Fallback-Geschwindigkeit

### 6.3 Kandidatenstufe
Unbestaetigte Objekte werden zuerst als Kandidaten gefuehrt. Erst bei passender Wiedererkennung wird ein echter Track erzeugt. Das reduziert Fehltracks durch Einzelrauschen.

### 6.4 Missed-Handling und Loeschung
Nicht gematchte Tracks werden praediziert und erhalten `missed++`. Loeschung erfolgt kontextabhaengig:

- in der vertrauenswuerdigen Geschwindigkeitsregion: strenger (`max_missed_in_region`)
- ausserhalb: toleranter, bis y-Grenzen verletzt sind (`min_tracked_y_mm`, `max_tracked_y_mm`)

### 6.5 Ergebnis
`getActiveObjects()` liefert die aktuelle Liste inklusive praedizierter, kurzzeitig unsichtbarer Objekte.

---

## 7. Pipeline der Roboterkamera (`RobotCamera`)

### 7.1 Ziel
Die Roboterkamera verfeinert die Zielposition fuer den Greifprozess im Nahbereich und publiziert laufend Koordinaten.

### 7.2 Eingehende Informationen
`RobotCamera` erstellt zusaetzlich einen SUB-Socket:

- Subscribe auf Topic `obj_list`
- Verbindung nach `tcp://127.0.0.1:5555`

Damit wird die von der statischen Kamera publizierte Objektliste empfangen.

### 7.3 Verarbeitungsablauf pro Zyklus
1. Optional ein statisches Referenzobjekt empfangen (`receiveStaticObject`)
2. Eigene Farb-/Tiefenframes laden und ausrichten
3. Aus Tiefendaten eine Objektmaske bestimmen
4. Groesste Kontur als Zielregion waehlen
5. Relevanten unteren Objektbereich auswerten (Bottom-Edge-Heuristik)
6. Relevanten Pixel in 3D deprojizieren
7. Zielkoordinaten per `sendCoordinates(...)` auf Topic `coordinates` versenden

Die aktuelle Implementierung nutzt aus der Objektliste stets das erste Objekt als Referenz.

---

## 8. Nachrichten und Datenschnittstelle

### 8.1 Datenstruktur in C++
`Object3D` in `cameras/Object3D.hpp` enthaelt:

- `id`, `label`
- `x`, `y`, `z`
- `orientation`
- `width`, `length`, `height`
- `vy`

### 8.2 Protobuf-Vertrag
In `zeroMQ/objects_3D.proto`:

- `Object3D_msg`: einzelnes Objekt
- `Objects3D_msg`: wiederholte Liste von Objekten

Damit ist die Schnittstelle zwischen Publisher und Subscriber klar formalisiert und sprachunabhaengig.

---

## 9. Konfigurationsdateien und Parameterwirkung

### 9.1 `config_cam_static.yml`
Relevante Parameter:

- `serial_number`: waehlt die konkrete RealSense
- `roi`: begrenzt Suchbereich im Bild
- `conveyor_z_dist`, `min_obj_height`, `max_obj_height_mm`: Hoehenmodell fuer Segmentierung
- `min_contour_area`: Rauschunterdrueckung bei Konturen
- `search_area_y_min/max`: zusaetzliche geometrische Plausibilisierung
- `zmq_port`: Publisher-Port fuer `obj_list`

### 9.2 `config_cam_robot.yml`
Relevante Parameter:

- `serial_number`: waehlt Roboterkamera
- `zmq_port`: Publisher-Port fuer `coordinates`
- Toleranzen und Debugoptionen

---

## 10. End-to-End-Datenfluss (Kurzfassung)

1. `camera_static` erfasst Szene und erzeugt getrackte Objektliste.
2. Objektliste wird als `Objects3D_msg` auf Topic `obj_list` publiziert.
3. `camera_robot` abonniert `obj_list`.
4. `camera_robot` kombiniert lokale Tiefenwahrnehmung mit empfangenen Objektinfos.
5. Ergebnis wird als Koordinaten-Message auf Topic `coordinates` publiziert.

---

## 11. Hinweise fuer die technische Doku
Fuer eine spaetere Ausarbeitung (z. B. Bachelor-/Projektbericht) sind diese Abschnitte meist hilfreich:

1. **Messaufbau und Koordinatensysteme** (Kameraachsen, Referenzpunkt, Vorzeichenkonvention)
2. **Kalibrierannahmen** (Tiefe, Offset, Bezug zum Foerderband)
3. **Robustheit** (Umgang mit fehlender Tiefe, Tracking-Praediktion, Kandidatenlogik)
4. **Laufzeitverhalten** (Frame-Skipping, reale FPS, Latenz bis `coordinates`)
5. **Grenzen** (starke Reflexionen, Verdeckungen, Mehrfachobjekte im Nahbereich)

Diese Punkte helfen spaeter bei Nachvollziehbarkeit und Reproduzierbarkeit der Bildverarbeitung.
