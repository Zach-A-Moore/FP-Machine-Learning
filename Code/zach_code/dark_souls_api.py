import os
import time
import numpy as np
import pydirectinput as direct_input
from control_ds3_ml import attack, dodge, heal, move_forward, move_backward

# Paths to the logger output files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLAYER_INFO_PATH = os.path.join(BASE_DIR, "data", "player_info.txt")
GUNDYR_INFO_PATH = os.path.join(BASE_DIR, "data", "gundyr_info.txt")
ACTION_TRIGGER_PATH = os.path.join(BASE_DIR, "data", "action_trigger.txt")

action_dict = {
    0: "light attack",
    1: "dodge",
    2: "heal"
}

def run_lua_script(script_path, params=""):
    """
    Execute a Lua script via Cheat Engine.
    Replace with your actual Cheat Engine command or mechanism.
    """
    abs_script_path = os.path.join(BASE_DIR, script_path)
    command = f"cheatengine_command --script {abs_script_path} {params}"  # TODO: Replace with actual command
    print(f"Executing Lua script: {command}")
    os.system(command)
    time.sleep(0.5)  # Wait for script execution

def reset_environment():
    """
    Reset the game environment without relying on triggers module.
    - Teleport player to boss arena.
    - Reset boss state.
    - Move forward, interact with fog wall, lock onto boss.
    Returns the initial state.
    """
    print("Resetting environment...")

    # Ensure loggers are active
    run_lua_script("archive/enable_flags.lua")  # Enables player_logger.LUA, gundyr_logger.LUA

    # Reset boss state
    print("Resetting boss...")
    run_lua_script("archive/Boss_Reset.lua")  # Or create revive_boss.LUA

    # Teleport player
    print("Teleporting player to boss arena...")
    run_lua_script("archive/TP_to_Boss.LUA")

    # Focus on game window
    print("Focusing on game window...")
    direct_input.keyDown('alt')
    time.sleep(0.2)
    direct_input.press('tab')
    time.sleep(0.2)
    direct_input.keyUp('alt')
    time.sleep(0.3)
    direct_input.keyUp('alt')
    time.sleep(0.1)

    # Move forward for 2 seconds
    print("Moving forward to fog wall...")
    direct_input.keyDown('w')
    time.sleep(2)
    direct_input.keyUp('w')

    # Interact with fog wall (press E)
    print("Interacting with fog wall...")
    direct_input.keyDown('e')
    time.sleep(0.2)
    direct_input.keyUp('e')

    # Wait for transition
    time.sleep(1)

    # Lock onto boss (press Q)
    print("Locking onto boss...")
    direct_input.keyDown('q')
    time.sleep(0.2)
    direct_input.keyUp('q')

    # Allow game state to stabilize
    time.sleep(0.5)

    # Return initial state
    return get_state()

# def reset_environment():
#     """
#     Reset the game environment without relying on triggers module.
#     - Teleport player to boss arena.
#     - Move forward, interact with fog wall, lock onto boss.
#     Returns the initial state.
#     """
#     print("Resetting environment: Teleporting player to boss arena...")
    
#     # Teleport player
#     run_lua_script("archive/TP_to_Boss.LUA")
    
#     # Focus on game window
#     print("Focusing on game window...")
#     direct_input.keyDown('alt')
#     time.sleep(0.2)
#     direct_input.press('tab')
#     time.sleep(0.2)
#     direct_input.keyUp('alt')
#     time.sleep(0.3)
#     direct_input.keyUp('alt')
#     time.sleep(0.1)
    
#     # Move forward for 2 seconds
#     print("Moving forward to fog wall...")
#     direct_input.keyDown('w')
#     time.sleep(2)
#     direct_input.keyUp('w')
    
#     # Interact with fog wall (press E)
#     print("Interacting with fog wall...")
#     direct_input.keyDown('e')
#     time.sleep(0.2)
#     direct_input.keyUp('e')
    
#     # Wait for transition (adjust based on game timing)
#     time.sleep(1)
    
#     # Lock onto boss (press Q)
#     print("Locking onto boss...")
#     direct_input.keyDown('q')
#     time.sleep(0.2)
#     direct_input.keyUp('q')
    
#     # Allow game state to stabilize
#     time.sleep(0.5)
    
#     # Return initial state
#     return get_state()


# def step_environment(action):
#     """
#     Apply an action to the game.
#     'action' is a dictionary with:
#        - 'command': integer (0: light attack, 1: dodge, 2: heal)
#        - 'movement': float (a continuous value representing forward/backward movement)

#     In your final implementation, you would send these commands to the game (e.g. by writing to a file
#     that a Lua script reads). Here we just simulate a short delay.
#     """
#     print(
#         f"Python: Applying action: command={action['command']}, movement={action['movement']}")
#     # Here you could write the action to a file that your Lua script will read.
#     time.sleep(0.1)
#     # Get the new state, compute reward, and check if episode is done.
#     state = get_state()
#     reward = compute_reward(state, action)
#     done = check_done(state)
#     info = {}
#     return state, reward, done, info


def step_environment(action):
    """
    Apply an action to the game.
    action: dict with 'command' (0: light attack, 1: dodge, 2: heal) and 'movement' (float, -1 to 1).
    Returns: state, reward, done, info.
    """
    command = action['command']
    movement = action['movement']
    print(f"Python: Applying action: command={action_dict[command]}, movement={movement}")

    # Apply command
    if command == 0:
        attack()
    elif command == 1:
        dodge()
    elif command == 2:
        heal()

    # Apply movement
    if movement > 0:
        move_forward(duration=movement)  # Scale duration by positive movement
    elif movement < 0:
        move_backward(duration=-movement)  # Scale duration by negative movement

    # Simulate step delay
    time.sleep(0.1)

    state = get_state()
    reward = compute_reward(state, action)
    done = check_done(state)
    info = {}
    return state, reward, done, info


def get_state(max_retries=3, retry_delay=0.05):
    """
    Read game state from log files with retries.
    Returns: np.array of [playerHealth, playerStamina, playerX, playerY, playerZ, playerAngle,
                         bossHealth, bossX, bossY, bossZ, bossAngle, bossAnim].
    """
    player_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    boss_state = [1037.0, 0.0, 0.0, 0.0, 0.0, "idle"]

    # Retry reading player info
    for attempt in range(max_retries):
        try:
            with open(PLAYER_INFO_PATH, "r") as f:
                line = f.readline().strip()
                parts = line.split(",")
                if len(parts) >= 7:  # Include estus
                    player_state = [float(p) for p in parts[:6]]
                    if player_state[0] < 0:  # Validate health
                        player_state[0] = 0.0
                    if player_state[1] < 0:  # Validate stamina
                        player_state[1] = 0.0
            break
        except Exception as e:
            print(f"Error reading player info (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    else:
        print("Failed to read player info after retries.")

    # Retry reading boss info
    for attempt in range(max_retries):
        try:
            with open(GUNDYR_INFO_PATH, "r") as f:
                line = f.readline().strip()
                parts = line.split(",")
                if len(parts) >= 6:
                    boss_state = [float(p) for p in parts[:5]] + [parts[5]]
                    if boss_state[0] < 0:  # Validate health
                        boss_state[0] = 0.0
            break
        except Exception as e:
            print(f"Error reading boss info (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(retry_delay)
    else:
        print("Failed to read boss info after retries.")

    # Map animation to numeric value
    anim_map = {"Idle": 0, "Attack": 1, "Damage": 2, "Death": 3}
    boss_anim = anim_map.get(boss_state[5].capitalize(), 0)

    # Combine states (exclude estus for now)
    state = np.array(player_state + boss_state[:5] + [boss_anim], dtype=np.float32)
    return state


MAX_PLAYER_HEALTH = 500.0  # Adjust based on your game setup
MAX_BOSS_HEALTH = 1037.0   # Adjust for Iudex Gundyr
EPISODE_TIMEOUT = 120.0    # 2 minutes max per episode

def compute_reward(state, action):
    """
    Compute reward based on state and action.
    """
    player_health = state[0]
    boss_health = state[6]

    boss_damage = MAX_BOSS_HEALTH - boss_health
    player_damage = MAX_PLAYER_HEALTH - player_health
    time_penalty = 0.01

    reward = boss_damage * 0.1 - player_damage * 0.1 - time_penalty
    return reward

def check_done(state, start_time=None):
    """
    Check if episode is done (boss or player dead, or timeout).
    """
    player_health = state[0]
    boss_health = state[6]
    if boss_health <= 0 or player_health <= 0:
        return True
    if start_time and (time.time() - start_time >= EPISODE_TIMEOUT):
        print("Episode timed out.")
        return True
    return False
