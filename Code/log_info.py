def log_player_info():
    # file_path = "C:\\Users\\thanos\\OneDrive - MNSCU\\Desktop\\school\\dark_souls_ai_code\\FP-Machine-Learning\\Code\\player_info.txt"  # Ben's path
    # file_path = "/mnt/c/Users/Laween/OneDrive/Desktop/MSUM/Spring_2025/490/Final_Project/Dark_Souls/FP-Machine-Learning/Code/data/player_info.txt" # Laween's path
    file_path = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\player_info.txt"  # Laween's path

    print("Listening for game data...")

    while True:
        try:
            with open(file_path, "r") as file:
                data = file.read().strip()
                if data:
                    health, stamina, estus, x, y, z, a = map(
                        float, data.split(","))
                    # TODO: FIX ESTUS
                    print(
                        f"Health: {health}, Stamina: {stamina}, Estus Flasks: {0}, X: {x}, Y: {y}, Z: {z}, angle: {a}")
        except Exception as e:
            print(f"Error reading file: {e}")

        # time.sleep(0.1)  # Check every 100ms


def log_gundyr_info():
    # file_path = "C:\\Users\\thanos\\OneDrive - MNSCU\\Desktop\\school\\dark_souls_ai_code\\FP-Machine-Learning\\Code\\gundyr_info.txt"  # Ben's path
    # file_path = "/mnt/c/Users/Laween/OneDrive/Desktop/MSUM/Spring_2025/490/Final_Project/Dark_Souls/FP-Machine-Learning/Code/data/gundyr_info.txt" # Laween's path
    file_path = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\gundyr_info.txt"  # Laween's path

    print("Listening for game data...")

    while True:
        try:
            with open(file_path, "r") as file:
                data = file.read().strip()
                if data:
                    health, x, y, z, a = map(float, data.split(","))
                    print(
                        f"Health: {health}, X: {x}, Y: {y}, Z: {z}, angle: {a}")
        except Exception as e:
            print(f"Error reading file: {e}")

        # time.sleep(0.1)  # Check every 100ms
