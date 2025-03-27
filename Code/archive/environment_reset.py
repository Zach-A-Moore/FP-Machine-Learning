import time
import os

# File paths
PLAYER_DATA_FILE = "data/player_info.txt"
BOSS_DATA_FILE = "data/gundyr_info.txt"

# Define the reset coordinates for the player (adjust these values as needed)
TODO: make this refer to the lua script set_poisition.lua
RESET_POSITION = {
    "x": 100.0,  # Example value: change to your desired X coordinate
    "y": 50.0,   # Example value: change to your desired Y coordinate
    "z": 0.0     # Example value: change to your desired Z coordinate
}

def run_lua_script(script_path, params=""):
    """
    Executes a LUA script via Cheat Engine.
    NOTE: The command below is a placeholder.
          Replace 'cheatengine_command' and the parameter syntax
          with the correct commands for your setup.
    """
    command = f"cheatengine_command --script {script_path} {params}"
    print("Executing command:", command)
    os.system(command)

def reset_player():
    """
    Reset the player by teleporting to a preset location.
    This function calls a LUA script (set_position.LUA) that should
    read the provided parameters (x, y, z) and set the player's position.
    """
    print("Player health reached zero. Resetting player position...")
    # Build command parameters; make sure your LUA script is designed to accept these
    params = f"--x {RESET_POSITION['x']} --y {RESET_POSITION['y']} --z {RESET_POSITION['z']}"
    run_lua_script("Code/set_position.LUA", params)
    # Allow some time for the reset to take effect
    time.sleep(1)

def reset_boss():
    """
    Reset the boss encounter by reviving the boss and ensuring the sword is drawn.
    You may need to create or modify a LUA script (e.g., revive_boss.LUA)
    to enable the necessary Cheat Engine flags.
    """
    print("Boss health reached zero. Resetting boss encounter...")
    # Run the LUA script that revives the boss and sets up the encounter.
    # If you don't have one yet, create a script (e.g., Code/revive_boss.LUA) that:
    #  - Revives Gundyr (or your designated boss)
    #  - Sets the flag to indicate that the sword is already drawn
    run_lua_script("Code/revive_boss.LUA")
    time.sleep(1)

def read_game_data(file_path):
    """
    Reads the first line of the given file and returns the data as a list.
    Assumes the file is formatted as a CSV string.
    """
    try:
        with open(file_path, 'r') as file:
            line = file.readline().strip()
            return line.split(',')
    except Exception as e:
        print("Error reading", file_path, ":", e)
        return None

def monitor_game():
    """
    Continuously monitors the player's and boss's health.
    If the player or boss is determined to be "dead" (health <= 0),
    the appropriate reset function is triggered.
    """
    while True:
        player_data = read_game_data(PLAYER_DATA_FILE)
        boss_data = read_game_data(BOSS_DATA_FILE)
        
        if player_data and boss_data:
            try:
                # Assuming the first value in each file is the health.
                player_health = float(player_data[0])
                boss_health = float(boss_data[0])
                
                if player_health <= 0:
                    reset_player()
                if boss_health <= 0:
                    reset_boss()
            except Exception as e:
                print("Error parsing game data:", e)
        time.sleep(0.1)  # 100ms delay to match your data logging rate

if __name__ == "__main__":
    monitor_game()
