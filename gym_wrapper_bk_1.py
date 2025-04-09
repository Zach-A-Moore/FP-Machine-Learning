import gym
from gym import spaces
import numpy as np
import time
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import os
from dark_souls_api_bk_1 import reset_environment, step_environment, get_state, compute_reward, check_done


# class dark_souls_api:
#     @staticmethod
#     def reset_environment():
#          """
#         Reset the game environment:
#         - Teleport the player to just before the fog wall.
#         - Step forward, press E to interact with the fog wall, and press Q to lock on.
#         Returns the initial state vector.
#         """
#         # Here, you would call your existing Lua scripts (or another mechanism)
#         # to reset the player's position, angle, and lock-on state.

#         print("Resetting environment (teleport, interact, lock on)...")
#         # Wait a bit for the game to settle:
#         time.sleep(2)
#         # For now, we return a dummy initial state:
#         return dark_souls_api.get_state()

#     @staticmethod
#     def step_environment(action):
#         """
#         Apply the action to the game, wait a bit, then return:
#         (new_state, reward, done, info)
#         'action' is a dictionary with:
#             'command': 0 (light attack), 1 (dodge), or 2 (heal)
#             'movement': continuous scalar (e.g., desired forward movement)
#         """
#         # Simulate sending the movement command and performing the command.
#         # print(
#         #     f"Applying action: command={action['command']}, movement={action['movement']}")
#         command = int(action[0])
#         movement = (action[1] - 10) / 10  # convert 0–20 to -1.0 to 1.0

#         print(f"Applying action: command={command}, movement={movement}")

#         # Here you would:
#         # - For movement: Write the new player position relative to current position
#         # - For command: Simulate the corresponding key press or call game function
#         # For now, we simulate a step delay:
#         time.sleep(0.1)

#         # Compute dummy reward values:
#         # (For example, positive reward for boss damage, negative for player damage, etc.)
#         state = dark_souls_api.get_state()
#         reward = dark_souls_api.compute_reward(
#             state, {"command": command, "movement": movement})
#         # reward = dark_souls_api.compute_reward(state, action)
#         done = dark_souls_api.check_done(state)
#         info = {}  # additional info if needed
#         return state, reward, done, info

#     @staticmethod
#     def get_state():
#         """
#         Read the game state from memory and return a feature vector.
#         For example:
#           - Player: health, stamina, x, y, z, angle.
#           - Boss: health, boss flag (converted to a float or one-hot).
#         For now, we return a dummy numpy array.
#         """
#         # Example state vector (length 10):
#         # [player_health, player_stamina, player_x, player_y, player_z, player_angle,
#         #  boss_health, boss_flag, boss_x, boss_z]
#         # Replace with actual memory reads.
#         state = np.array([
#             500.0,  # player health
#             100.0,  # player stamina
#             0.0,    # player x
#             0.0,    # player y
#             0.0,    # player z
#             -2.78,  # player angle
#             1037.0,  # boss health
#             0.0,    # boss flag (e.g., 0 means alive, 1 means defeated)
#             10.0,   # boss x
#             10.0    # boss z
#         ], dtype=np.float32)
#         return state

#     @staticmethod
#     def compute_reward(state, action):
#         """
#         Compute reward based on state and action.
#         Example:
#           - Reward positive for decrease in boss health.
#           - Negative reward for player taking damage.
#           - Time penalty.
#         For now, return a dummy reward.
#         """
#         # For demonstration, return a random reward:
#         return np.random.rand() - 0.5

#     @staticmethod
#     def check_done(state):
#         """
#         Check if the episode is done.
#         Episode might be done if:
#           - Boss is defeated, or
#           - Player is dead.
#         For now, we simulate done condition:
#         """
#         # If boss health is below a threshold or player health is 0, episode is done.
#         if state[6] <= 0 or state[0] <= 0:
#             return True
#         return False

# =============================================================================
# Custom Gym Environment for Dark Souls Gundyr
# =============================================================================


class DarkSoulsGundyrEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self):
        super(DarkSoulsGundyrEnv, self).__init__()

        # Define observation space (example: 10 continuous features)
        # Adjust the dimension to match your state vector.
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32
        )

        # Define action space:
        # "command": discrete: 0: light attack, 1: dodge, 2: heal.
        # "movement": continuous: a scalar (e.g., desired forward displacement, in range -1 to 1).
        # self.action_space = spaces.Dict({
        #     "command": spaces.Discrete(3),
        #     "movement": spaces.Box(low=-1.0, high=1.0, shape=(1,), dtype=np.float32)
        # })

        # Use MultiDiscrete for mixed discrete-continuous encoded as discrete buckets
        # 3 commands × 21 movement bins (-1.0 to 1.0)
        self.action_space = spaces.MultiDiscrete([3, 21])

        # Optionally, define any additional variables
        self.current_state = None
        self.steps = 0
        self.max_steps = 1000  # For example, end episode after 1000 steps

    def seed(self, seed=None):
        np.random.seed(seed)
        return [seed]

    def reset(self):
        """
        Reset the game environment. This function will:
          - Teleport the player to just before the fog wall,
          - Step forward,
          - Interact with the fog wall (press E) and lock on (press Q),
          and then return the initial state vector.
        """
        # Call the API reset function. In practice, this will use your Lua scripts or
        # other interfacing code to reset the game state.
        self.current_state = reset_environment()
        self.steps = 0
        return self.current_state

    def step(self, action):
        """
        Apply the given action to the game, then return (state, reward, done, info).
        """
        self.steps += 1
        command = int(action[0])
        movement = (action[1] - 10) / 10  # map 0–20 to -1.0 to 1.0
        # act = {"command": command, "movement": np.array(
        #     [movement], dtype=np.float32)}

        act = {"command": command, "movement": movement}

        # Apply the action via your API
        next_state, reward, done, info = step_environment(
            act)

        self.current_state = next_state

        # Optionally add a time penalty to reward (to encourage faster boss defeat)
        reward = reward - 0.01  # small penalty per step

        # If max steps reached, set done to True
        if self.steps >= self.max_steps:
            done = True

        return self.current_state, reward, done, info

    def render(self, mode="human"):
        """
        Optionally, implement rendering (e.g., by showing the current game screen).
        For now, we can print the state or leave it blank.
        """
        print("Current State:", self.current_state)

    def close(self):
        """
        Any necessary cleanup.
        """
        pass

# =============================================================================
# Training Code Example Using Stable-Baselines3 (PPO)
# =============================================================================


if __name__ == "__main__":

    # Create a vectorized environment (using 4 parallel instances)
    env = make_vec_env(lambda: DarkSoulsGundyrEnv(), n_envs=4)

    # Create the PPO model with the default MLP policy
    # model = PPO("MlpPolicy", env, verbose=1)
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        gae_lambda=0.95,
        clip_range=0.2,
    )


    # Train the model for a number of timesteps
    total_timesteps = 100000  # adjust as needed
    model.learn(total_timesteps=total_timesteps)

    # Save the trained model
    model.save("ppo_dark_souls_gundyr")

    # Optionally, run a test episode
    obs = env.reset()
    done = False
    total_reward = 0
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        env.render()
    print("Test episode total reward:", total_reward)

    env.close()
