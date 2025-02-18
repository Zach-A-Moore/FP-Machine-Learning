import time

file_path = "C:\\Users\\thanos\\OneDrive - MNSCU\\Desktop\\school\\dark_souls_ai_code\\FP-Machine-Learning\\Code\\gundyr_info.txt"  # Must match Lua script

print("Listening for game data...")

while True:
    try:
        with open(file_path, "r") as file:
            data = file.read().strip()
            if data:
                health, x, y, z, a = map(float, data.split(","))
                print(
                    f"Stamina: {health}, X: {x}, Y: {y}, Z: {z}, angle: {a}")
    except Exception as e:
        print(f"Error reading file: {e}")

    time.sleep(0.1)  # Check every 100ms
