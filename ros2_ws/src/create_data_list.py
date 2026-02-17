import os

# --- DEINE PFADE ---
BASE_PATH = "/home/tetripick/UR10_Pick_ws/ros2_ws/src"
POSE_DIR = os.path.join(BASE_PATH, "poses")
IMAGE_DIR = os.path.join(BASE_PATH, "images")
OUTPUT_FILE = os.path.join(BASE_PATH, "cal_data.yaml")
# -------------------

def main():
    # Wir suchen nach den neuen .yaml Posen und den Bildern
    # WICHTIG: Wir sortieren, damit img_01 auch pose_01 zugeordnet wird!
    images = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".png") or f.endswith(".jpg")])
    poses = sorted([f for f in os.listdir(POSE_DIR) if f.endswith(".yaml")])

    # Sicherheitscheck
    if len(images) != len(poses):
        print(f"ACHTUNG: Anzahl ungleich! Bilder: {len(images)}, Posen: {len(poses)}")
        print("Bitte prüfen, ob für jedes Bild eine .yaml Pose existiert.")
        return

    print(f"Erstelle Liste für {len(images)} Paare...")

    with open(OUTPUT_FILE, "w") as f:
        f.write("data:\n")
        for img_name, pose_name in zip(images, poses):
            # Wir schreiben absolute Pfade in die Datei
            abs_img_path = os.path.join(IMAGE_DIR, img_name)
            abs_pose_path = os.path.join(POSE_DIR, pose_name)
            
            f.write(f"  - image: {abs_img_path}\n")
            f.write(f"    pose:  {abs_pose_path}\n")

    print(f"Fertig! Datei erstellt: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()