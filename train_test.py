import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import gym_wrapper_bk_1 as gym_wrapper
import dark_souls_api_bk_1 as dark_souls_api

def train_model(total_timesteps, model_path, n_envs):
    """
    Initializes the training environment and trains the PPO agent.

    Args:
        total_timesteps (int): Total timesteps for training.
        model_path (str): Path where the trained model will be saved.
        n_envs (int): Number of parallel environments.
    """
    # Prepare the game for training.
    dark_souls_api.ready_for_training()
    
    # Create a vectorized environment with 'n_envs' parallel instances.
    env = make_vec_env(lambda: gym_wrapper.DarkSoulsGundyrEnv(), n_envs=n_envs)
    
    # Instantiate the PPO agent using the MLP policy.
    model = PPO("MlpPolicy", env, verbose=1)
    
    print(f"Starting training for {total_timesteps} timesteps on {n_envs} environment(s)...")
    model.learn(total_timesteps=total_timesteps)
    
    # Save the trained model.
    model.save(model_path)
    print(f"Training completed and model saved to: {model_path}")
    
    env.close()
    return model

def test_model(model_path, episodes, n_envs):
    """
    Loads a trained model and runs test episodes.

    Args:
        model_path (str): Path from which the trained model will be loaded.
        episodes (int): Number of test episodes to run.
        n_envs (int): Number of parallel environments.
    """
    # Create a vectorized environment for testing.
    env = make_vec_env(lambda: gym_wrapper.DarkSoulsGundyrEnv(), n_envs=n_envs)
    
    # Load the pre-trained model.
    model = PPO.load(model_path)
    print(f"Model loaded from {model_path}. Beginning testing...")
    
    # Run testing episodes.
    for ep in range(1, episodes + 1):
        obs = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            # Get the next action from the model. Use deterministic actions for reproducibility.
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            total_reward += reward
            env.render()  #render the environment.
        
        print(f"Test Episode {ep} - Total Reward: {total_reward}")
    
    env.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Combined Training and Testing script for Dark Souls 3 PPO Agent"
    )
    parser.add_argument("--train", action="store_true", help="Run training mode")
    parser.add_argument("--test", action="store_true", help="Run testing mode")
    parser.add_argument("--timesteps", type=int, default=100000, help="Timesteps for training")
    parser.add_argument("--episodes", type=int, default=1, help="Test episodes to run")
    parser.add_argument("--model_path", type=str, default="ppo_dark_souls_gundyr", help="Path to save/load the model")
    parser.add_argument("--n_envs", type=int, default=1, help="Number of parallel environments to use")
    args = parser.parse_args()
    
    # To run the script, use flags such as --train and/or --test.
    #    To train only:  python train_test.py --train --timesteps 200000 --n_envs 1
    #    To test only:   python train_test.py --test --episodes 5 --n_envs 1 --model_path ppo_dark_souls_gundyr
    #    To train then test sequentially:  
    #            python train_test.py --train --test --timesteps 200000 --episodes 5 --n_envs 1

    # Run training if the flag is set.
    if args.train:
        train_model(total_timesteps=args.timesteps, model_path=args.model_path, n_envs=args.n_envs)
    
    # Run testing if the flag is set.
    if args.test:
        test_model(model_path=args.model_path, episodes=args.episodes, n_envs=args.n_envs)
