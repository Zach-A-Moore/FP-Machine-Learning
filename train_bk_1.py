from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gym_wrapper_bk_1 as gym_wrapper
import dark_souls_api_bk_1 as dark_souls_api
if __name__ == "__main__":
    dark_souls_api.ready_for_training()

    # Create a vectorized environment with 1 parallel instances.
    # NOTE: we can think about 4 parallel instances for faster training.
    env = make_vec_env(lambda: gym_wrapper.DarkSoulsGundyrEnv(), n_envs=1)
    model = PPO("MlpPolicy", env, verbose=1)
    total_timesteps = 100000  # Adjust timesteps as needed.
    model.learn(total_timesteps=total_timesteps)
    model.save("ppo_dark_souls_gundyr")
    # ✅ Waits until CE Lua script writes "True"
    # dark_souls_api.wait_until_in_arena()

    # Run a test episode.
    obs = env.reset()
    done = False
    total_reward = 0

    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        total_reward += reward
        env.render()

    print("Test episode total reward:", total_reward)
    env.close()
