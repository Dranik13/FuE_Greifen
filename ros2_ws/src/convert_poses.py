import os
import yaml
from scipy.spatial.transform import Rotation as R


BASE_PATH = "/home/tetripick/UR10_Pick_ws/ros2_ws/src"
POSE_DIR = os.path.join(BASE_PATH, "poses")

def read_ur_pose(filepath):
    """
    Liest die UR-Pose aus der Textdatei und ignoriert Metadaten wie ''.
    """
    with open(filepath, 'r') as f:
        content = f.read().strip()
        
        # Alles bereinigen: Klammern weg, Aufsplitten
        # Beispiel Input: "-0.009 ... -0.785 ..."
        cleaned_content = content.replace('[', ' ').replace(']', ' ').replace(':', ' ')
        parts = cleaned_content.split()
        
        # Wir suchen nach Zahlen (Floats). Alles was keine Zahl ist, fliegt raus.
        numbers = []
        for p in parts:
            try:
                numbers.append(float(p))
            except ValueError:
                continue # War Text oder Müll, ignorieren
        
        # Eine korrekte Pose hat immer 6 Werte (X,Y,Z,Rx,Ry,Rz).
        # Falls durch "" noch eine "1" dabei ist, nehmen wir einfach
        # die LETZTEN 6 Zahlen, das sind sicher die Koordinaten.
        if len(numbers) >= 6:
            return numbers[-6:] # Die letzten 6 Elemente zurückgeben
        else:
            print(f"FEHLER in Datei {filepath}: Konnte keine 6 Koordinaten finden!")
            return None

def main():
    # Prüfen ob der Ordner existiert
    if not os.path.exists(POSE_DIR):
        print(f"Fehler: Der Ordner existiert nicht: {POSE_DIR}")
        return

    # Alle .txt Dateien finden
    files = sorted([f for f in os.listdir(POSE_DIR) if f.endswith(".txt")])
    print(f"Suche in: {POSE_DIR}")
    print(f"Gefunden: {len(files)} Pose-Dateien (.txt). Starte Konvertierung...")

    count = 0
    for filename in files:
        in_path = os.path.join(POSE_DIR, filename)
        
        # 1. Daten einlesen und bereinigen
        ur_pose = read_ur_pose(in_path)
        if ur_pose is None: continue
        
        # UR Format: [X, Y, Z, Rx, Ry, Rz]
        x, y, z, rx, ry, rz = ur_pose

        # 2. Umrechnen: Rotationsvektor -> Quaternion
        rot = R.from_rotvec([rx, ry, rz])
        quat = rot.as_quat() # Gibt [x, y, z, w] zurück

        # 3. Neue Datenstruktur bauen (WICHTIG: Quaternionen!)
        yaml_data = {
            'x': float(x),
            'y': float(y),
            'z': float(z),
            'qx': float(quat[0]),
            'qy': float(quat[1]),
            'qz': float(quat[2]),
            'qw': float(quat[3])
        }

        # 4. Speichern als .yaml im gleichen Ordner
        out_filename = filename.replace(".txt", ".yaml")
        out_path = os.path.join(POSE_DIR, out_filename)
        
        with open(out_path, 'w') as outfile:
            yaml.dump(yaml_data, outfile, default_flow_style=False)
            
        count += 1

    print("------------------------------------------------")
    print(f"Fertig! {count} Dateien wurden erfolgreich konvertiert.")
    print(f"Die neuen .yaml Dateien liegen in: {POSE_DIR}")

if __name__ == "__main__":
    main()