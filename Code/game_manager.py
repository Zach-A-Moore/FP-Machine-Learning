import time
import os
import start_fight
# File paths for  game data
PLAYER_INFO_PATH = "data\\player_info.txt"
GUNDYR_INFO_PATH = "data\\gundyr_info.txt"

# Global counters for tracking wins and losses
wins = 0
losses = 0
estus = 3


def run_lua_script(script_path, params=""):
    """
    Executes a LUA script via Cheat Engine.
    NOTE: Replace 'cheatengine_command' with the actual command for your setup.
    """
    command = f"cheatengine_command --script {script_path} {params}"
    print("Executing command:", command)
    os.system(command)


def auto_enable_flags():
    """
    Auto-enables the cheat engine flags by running a LUA script that sets your custom flags.
    Create a LUA script (e.g., Code/enable_flags.lua) that checks the table and enables your two custom flags.
    """
    print("Auto-enabling cheat engine flags...")
    run_lua_script("enable_flags.lua")
    time.sleep(1)


def reset_player():
    """
    Resets the player's position using your set_position.lua script.
    Also resets the estus count to 3 (as you plan to track it manually).
    """
    print("Player defeated! Resetting player position...")
    run_lua_script("set_position.lua")
    # TODO: Reset estus manually if needed:
    # TODO: reset lock on range to 100 again
    # TODO: Move postion
    print("Resetting Estus count to 3.")
    time.sleep(1)


def reset_boss():
    """
    Resets the boss encounter by reviving the boss and ensuring the sword is drawn.
    Create a LUA script (e.g., Code/revive_boss.lua) that does this.
    """
    print("Boss defeated! Resetting boss encounter...")
    run_lua_script("revive_boss.lua")
    time.sleep(1)


def get_player_data():
    """
    Reads the player info file and returns a dictionary.
    Expected format: health, stamina, estus, x, y, z, angle
    """
    try:
        with open(PLAYER_INFO_PATH, 'r') as f:
            data = f.read().strip()
        if data:
            parts = data.split(',')
            return {
                "health": float(parts[0]),
                "stamina": float(parts[1]),
                # Manual tracking; default is 3 at reset.
                "estus": int(parts[2]),
                "x": float(parts[3]),
                "y": float(parts[4]),
                "z": float(parts[5]),
                "angle": float(parts[6])
            }
    except Exception as e:
        print("Error reading player info:", e)
    return None


def get_gundyr_data():
    """
    Reads the Gundyr (boss) info file and returns a dictionary.
    Expected format: health, x, y, z, angle
    """
    try:
        with open(GUNDYR_INFO_PATH, 'r') as f:
            data = f.read().strip()
        if data:
            parts = data.split(',')
            return {
                "health": float(parts[0]),
                "x": float(parts[1]),
                "y": float(parts[2]),
                "z": float(parts[3]),
                "angle": float(parts[4])
            }
    except Exception as e:
        print("Error reading Gundyr info:", e)
    return None


def monitor_fight():
    """
    Monitors the fight: starts a timer at fight initiation and continuously checks player and boss health.
    If the player's health falls to zero or below, a loss is recorded and the player reset is called.
    If the boss's health falls to zero or below, a victory is recorded and the boss reset is called.
    """
    global wins, losses
    fight_active = True
    start_time = time.time()
    print("Fight started.")

    while fight_active:
        player = get_player_data()
        boss = get_gundyr_data()
        if player is None or boss is None:
            time.sleep(0.1)
            continue

        # Check for defeat conditions
        if player["health"] <= 0:
            print("Player health is 0 or less.")
            losses += 1
            duration = time.time() - start_time
            print(
                f"Fight duration: {duration:.2f} seconds. Total Losses: {losses}")
            # reset_player() # FIXME: Uncomment this line when you have the reset_player function ready.
            fight_active = False
            start_fight.isrunning = False
        elif boss["health"] <= 0:
            print("Boss health is 0 or less.")
            wins += 1
            duration = time.time() - start_time
            print(
                f"Fight duration: {duration:.2f} seconds. Total Wins: {wins}")
            reset_boss() #FIXME: Uncomment this line when you have the reset_boss function ready.
            fight_active = False
            start_fight.isrunning = False

        time.sleep(0.1)  # Matches your data logging rate


def main():
    """
    Main loop: Auto-enables cheat engine flags once and then continuously runs fight cycles.
    In a full implementation, you’d call your fight-start functions (move_forward, enter_fog, lock_on)
    before entering the fight monitoring loop.
    """
    # Enable cheat engine table flags automatically.
    # FIXME: Uncomment this line when you have the enable_flags.lua script ready.
    # auto_enable_flags()

    while True:
        print("Starting a new fight cycle...")
        start_fight.main()
        # At this point you could call functions to:
        # - Move forward
        # - Interact with the fog wall
        # - Lock on to the boss
        # (These actions are handled in your start_fight script.)
        monitor_fight()
        print("Reset complete. Preparing for next fight cycle.\n")
        time.sleep(2)  # Pause before starting the next cycle


if __name__ == "__main__":
    main()
