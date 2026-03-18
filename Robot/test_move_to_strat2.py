import rtde_control
import yaml
from pathlib import Path
from runtime_config import load_runtime_config

# 1. IP aus der runtime_config laden
config = load_runtime_config()
ROBOT_IP = config.robot_ip

def test_drive():
    # 2. Werte aus deiner pose.yaml laden
    pose_file = Path(__file__).with_name("pose.yaml")
    with pose_file.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    
    target = data.get("Kamera_2_Kalib", {}).get("TCP Pos")
    
    if not target:
        print("Fehler: 'Kamera_2_Kalib' wurde in der pose.yaml nicht gefunden!")
        return

    print(f"Verbinde mit Roboter {ROBOT_IP}...")
    try:
        rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
        
        print(f"Starte Fahrt zur Zielposition: {target}")
        print("Achtung: Der Roboter bewegt sich jetzt!")
        
        # Wir nutzen moveL für eine geradlinige Bewegung zum Ziel
        # Geschwindigkeit: 0.1 m/s, Beschleunigung: 0.1 m/s^2 (schön langsam für den Test)
        rtde_c.moveL(target, 0.1, 0.1)
        
        print("\nErfolg! Der Roboter steht jetzt in der schrägen Lauerposition.")
        print("Prüfe jetzt, ob der Winkel für die Kamera und den Greifer so passt.")
        
    except Exception as e:
        print(f"\nFehler bei der Fahrt: {e}")
    finally:
        print("Script beendet.")

if __name__ == "__main__":
    test_drive()