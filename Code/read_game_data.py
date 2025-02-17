import time

file_path = "C:\\Users\\Laween\\Downloads\\game_data.txt"  # Must match Lua script

print("Listening for game data...")

while True:
    try:
        with open(file_path, "r") as file:
            data = file.read().strip()
            if data:
                health, stamina, x, y, z = map(float, data.split(","))
                print(
                    f"Health: {health}, Stamina: {stamina}, X: {x}, Y: {y}, Z: {z}")
    except Exception as e:
        print(f"Error reading file: {e}")

    time.sleep(0.1)  # Check every 100ms
