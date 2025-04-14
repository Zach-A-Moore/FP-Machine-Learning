import os
import time
import numpy as np
import triggers


# Paths to the logger output files
PLAYER_INFO_PATH = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\player_info.txt"
GUNDYR_INFO_PATH = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\gundyr_info.txt"
# Path to the action trigger file
ACTION_TRIGGER_PATH = "C:\\Users\\Laween\\OneDrive\\Desktop\\MSUM\\Spring_2025\\490\\Final_Project\\Dark_Souls\\FP-Machine-Learning\\Code\\data\\action_trigger.txt"

action_dict = {
    0: "light attack",
    1: "dodge",
    2: "heal"
}


def reset_environment():
    """
    Reset the game environment.
    """
    print("Resetting environment: Teleporting player to boss arena, stepping forward, interacting...")
    triggers.env_trigger()
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
    print(
        f"Python: Applying action: command={action['command']}, movement={action['movement']}")
    # Write the action to the trigger file:
    with open(ACTION_TRIGGER_PATH, "w") as f:
        f.write(f"{action['command']},{action['movement']}")
    # Simulate step delay
    time.sleep(0.1)
    state = get_state()
    reward = compute_reward(state, action)
    done = check_done(state)
    info = {}
    return state, reward, done, info


def get_state():
    """
    Read the game state from your log files.
    Expected format:
      - PLAYER_INFO_PATH contains: playerHealth,playerStamina,playerX,playerY,playerZ,playerAngle
      - GUNDYR_INFO_PATH contains: bossHealth,bossX,bossY,bossZ,bossAngle,bossAnimState
    We combine these into one state vector.
    """
    # Default values if file reading fails.
    player_state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    boss_state = [1037.0, 0.0, 0.0, 0.0, 0.0, "idle"]

    try:
        with open(PLAYER_INFO_PATH, "r") as f:
            line = f.readline().strip()
            parts = line.split(",")
            if len(parts) >= 6:
                player_state = [float(p) for p in parts[:6]]
    except Exception as e:
        print("Error reading player info:", e)

    try:
        with open(GUNDYR_INFO_PATH, "r") as f:
            line = f.readline().strip()
            parts = line.split(",")
            if len(parts) >= 6:
                # boss_state: health, x, y, z, angle, animState (animState remains a string)
                boss_state = [float(p) for p in parts[:5]] + [parts[5]]
    except Exception as e:
        print("Error reading boss info:", e)

    # Convert the boss animation state to a numeric value.
    anim_map = {"idle": 0, "attack": 1, "damage": 2, "death": 3}
    boss_anim = anim_map.get(boss_state[5], 0)

    # Final state vector: [playerHealth, playerStamina, playerX, playerY, playerZ, playerAngle,
    #                      bossHealth, bossX, bossY, bossZ, bossAngle, bossAnim]
    state = np.array(
        player_state + boss_state[:5] + [boss_anim], dtype=np.float32)
    return state


def compute_reward(state, action):
    """
    Compute the reward for the current state and action.
    For example, you may consider:
      - Positive reward for decreasing boss health.
      - Negative reward for taking damage (decrease in player health).
      - A small time penalty per step.
    For this stub, we create a simple heuristic.
    """
    # State indices:
    # player state: [0]: health, [1]: stamina, [2]: x, [3]: y, [4]: z, [5]: angle
    # boss state: [6]: health, [7]: x, [8]: y, [9]: z, [10]: angle, [11]: animState

    player_health = state[0]
    boss_health = state[6]

    # For a reward, we can do:
    # Reward = (damage to boss) - (damage taken by player) - (small step penalty)
    # Here, assume baseline boss health is 1037.0; damage dealt = 1037 - current boss health.
    boss_damage = 1037.0 - boss_health
    # For player, assume full health is 500.
    player_damage = 500.0 - player_health

    # Small penalty per step
    time_penalty = 0.01

    reward = boss_damage * 0.1 - player_damage * 0.1 - time_penalty
    return reward


def check_done(state):
    """
    Check whether the episode is finished.
    An episode is done if the boss is defeated (boss health <= 0) or if the player dies (player health <= 0).
    """
    player_health = state[0]
    boss_health = state[6]
    if boss_health <= 0 or player_health <= 0:
        return True
    return False
