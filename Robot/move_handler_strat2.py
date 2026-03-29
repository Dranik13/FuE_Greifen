# Greifstrategie 2: hinten am Fließband in geneigter Position warten

"""
Behandelt den Zustand "MOVE" in der State-Machine des Roboters. 
Strategie "Spurwechsel" (Ansatz 1): Der Roboter fährt auf der X-Achse genau über 
die Fahrspur des herankommenden Bauteils, passt seine Höhe (Z) an das Bauteil an 
und wartet in einer fest definierten, schrägen Lauerhaltung auf der Y-Achse.
"""

from pathlib import Path
import yaml
import save_pos

# TODO: Den passenden Import für deine State-Machine hier einkommentieren/anpassen
# from state_machine import MachineState 

def _load_kamera_2_kalib_tcp_pos():
    """
    Lädt die fest geteachte, schräge Lauerposition aus der pose.yaml.
    Diese Position dient als Basis: Y, Rx, Ry und Rz werden exakt so übernommen, 
    nur X (Spur) und Z (Höhe) werden später dynamisch überschrieben.
    """
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    start_conveyor = data.get("Kamera_2_Kalib", {})
    tcp_pos = start_conveyor.get("TCP Pos")
    if not isinstance(tcp_pos, list) or len(tcp_pos) != 6:
        raise ValueError("[move_handler] Fehlerhafte oder fehlende 'Kamera_2_Kalib -> TCP Pos' Werte in pose.yaml")

    return [float(value) for value in tcp_pos]

# Globale Konstante: Wird beim Start des Skripts einmalig geladen
KAMERA_2_KALIB_TCP_POS = _load_kamera_2_kalib_tcp_pos()


def _load_camera_mount_to_camera_distance():
    """
    Lädt den statischen Kalibrierungs-Offset (Abstand zwischen Kamera und Roboter-TCP).
    Wird benötigt, um das Bauteil beim Spurwechsel exakt mittig zu treffen.
    """
    pose_file = Path(__file__).with_name("Calibration_results_final.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    camera_mount_to_camera = data.get("camera_mount_to_camera", {})
    camera_to_mount_distance = camera_mount_to_camera.get("y")
    
    if isinstance(camera_to_mount_distance, list):
        if len(camera_to_mount_distance) != 1:
            raise ValueError("[follow_handler] Falsche Anzahl an Werten für 'camera_mount_to_camera -> y' (Erwartet: 1)")
        return float(camera_to_mount_distance[0])

    try:
        return float(camera_to_mount_distance)
    except (TypeError, ValueError):
        raise ValueError("[follow_handler] Ungültiger Wert für 'camera_mount_to_camera -> y' in der Kalibrierungsdatei")

# Globale Konstante: Statischer Offset der Kamera
DISTANCE_TO_CAMERA = _load_camera_mount_to_camera_distance()

KAMERA_MITTE_X = 0.418329

def move(pos_x, pos_y, obj_height, rtde_r, rtde_c, object_speed, robot_speed=0.8, robot_acceleration=0.5, debug=False):
    """
    Führt den Spurwechsel und die Höhenanpassung aus.
    
    Parameter:
    - pos_x: X-Koordinate des Bauteils aus der Deckenkamera (in mm).
    - pos_y: Wird aktuell nicht genutzt (Roboter wartet auf festem Y), bleibt aber der Form halber in der Signatur.
    - obj_height: Höhe des Bauteils (in mm).
    - rtde_r / rtde_c: RTDE Schnittstellen zum Universal Robot.
    - object_speed: Geschwindigkeit des Fließbands (hier optional, wird in der Folge-Stage gebraucht).
    """
    
    target_tcp = KAMERA_2_KALIB_TCP_POS.copy()

    # 2. Wir berechnen die Abweichung von der Mitte
    # pos_x kommt in mm, also rechnen wir in Meter um
    objekt_x_meter = pos_x / 1000.0
    abweichung = objekt_x_meter - KAMERA_MITTE_X

    # 3. Wir addieren diese Abweichung auf deine perfekte geteachte Position (0.876)
    new_x = KAMERA_2_KALIB_TCP_POS[0] + abweichung
    target_tcp[0] = new_x

    # 3. Z-ACHSE (Höhenanpassung):
    # Wir addieren die Bauteilhöhe (in Metern) auf die geteachte Null-Höhe der Lauerposition.
    # So schwebt der schräge Greifer sicher über unterschiedlich hohen Bauteilen.
    hoehe_in_metern = obj_height / 1000.0
    #target_tcp[2] = KAMERA_2_KALIB_TCP_POS[2] + hoehe_in_metern
    #target_tcp[2] = KAMERA_2_KALIB_TCP_POS[2] + (hoehe_in_metern / 2.0)
    target_tcp[2] = KAMERA_2_KALIB_TCP_POS[2]

    # 4. Debug-Ausgaben zur Kontrolle
    if debug:
        print(f"[move_handler] --- NEUE BEWEGUNG ---")
        print(f"[move_handler] Spurwechsel auf X={target_tcp[0]:.4f}")
        print(f"[move_handler] Passe Höhe an Bauteil an (obj_height={obj_height}mm): Ziel-Z={target_tcp[2]:.4f}")
        print(f"[move_handler] Starte asynchrone Fahrt in schräge Lauerhaltung...")

    # 5. Sicherheitsprüfung & Ausführung:
    # is_save_position prüft (anhand der ersten 3 Elemente = X,Y,Z), ob der Punkt im erlaubten Arbeitsraum liegt.
    if save_pos.is_save_position(target_tcp[:3]):
        # Roboter bewegt sich linear zum berechneten Zielpunkt
        rtde_c.moveL(target_tcp, robot_speed, robot_acceleration, False)
    else:
        # Schutzschalter: Ziel liegt z.B. neben dem Fließband
        print(f"[move_handler] ABBRUCH: Ziel-Position {target_tcp[:3]} liegt außerhalb des konfigurierten Workspaces!")
        return None # Gibt None zurück, damit die State-Machine den Fehler abfangen und in den Idle-Zustand wechseln kann

    # 6. Erfolgreicher Übergang:
    # Gib den nächsten Zustand für die State-Machine zurück. 
    # TODO: An dein spezifisches State-Format anpassen (z.B. MachineState.OBJECT_WAITING)
    return "OBJECT_WAITING"