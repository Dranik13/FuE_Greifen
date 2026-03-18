import rtde_receive
from runtime_config import load_runtime_config

# 1. IP-Adresse aus deiner Config laden
config = load_runtime_config()

# 2. Verbindung zum Roboter herstellen
print(f"Verbinde mit Roboter unter IP: {config.robot_ip}...")
rtde_r = rtde_receive.RTDEReceiveInterface(config.robot_ip)

# 3. Aktuelle Position (X, Y, Z, Rx, Ry, Rz) abfragen
aktuelle_pose = rtde_r.getActualTCPPose()

# 4. Werte perfekt formatiert ausgeben
print("\n" + "="*50)
print("KOPIERE DIESE LISTE IN DEINE pose.yaml BEI 'Kamera_2_Kalib':")
print(aktuelle_pose)
print("="*50 + "\n")