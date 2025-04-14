class DarkSoulsGundyrEnv(gym.Env):
    def __init__(self):
        super(DarkSoulsGundyrEnv, self).__init__()
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32)
        self.action_space = spaces.MultiDiscrete([3, 21])
        self.current_state = None
        self.steps = 0
        self.max_steps = 1000
        self.start_time = None  # Track episode start time

    def reset(self):
        self.current_state = reset_environment()
        self.steps = 0
        self.start_time = time.time()  # Record start time
        return self.current_state

    def step(self, action):
        self.steps += 1
        command = int(action[0])
        movement = (action[1] - 10) / 10
        act = {"command": command, "movement": movement}
        next_state, reward, done, info = step_environment(act)
        self.current_state = next_state
        reward -= 0.01  # Time penalty
        if self.steps >= self.max_steps:
            done = True
        # Check timeout
        done = done or check_done(self.current_state, self.start_time)
        return self.current_state, reward, done, info