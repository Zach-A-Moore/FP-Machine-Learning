import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import time
import random
import os
import pydirectinput as direct_input
import pyautogui

# File paths (match your setup)
base_dir = os.path.dirname(os.path.abspath(__file__))
PLAYER_INFO_PATH = os.path.join(base_dir, "data", "player_info.txt")
GUNDYR_INFO_PATH = os.path.join(base_dir, "data", "gundyr_info.txt")

# Game input functions (from your code)
def move_forward(duration=0.5):
    direct_input.keyDown('w')
    time.sleep(duration)
    direct_input.keyUp('w')

def move_backward(duration=0.5):
    direct_input.keyDown('s')
    time.sleep(duration)
    direct_input.keyUp('s')

def move_left(duration=0.5):
    direct_input.keyDown('a')
    time.sleep(duration)
    direct_input.keyUp('a')

def move_right(duration=0.5):
    direct_input.keyDown('d')
    time.sleep(duration)
    direct_input.keyUp('d')

def attack():
    pyautogui.click()

def dodge():
    direct_input.keyDown('space')
    time.sleep(0.2)
    direct_input.keyUp('space')

def heal():
    direct_input.keyDown('r')
    time.sleep(0.2)
    direct_input.keyUp('r')

# Game state reading
def get_game_state():
    try:
        # Player data: health, stamina, estus, x, y, z, angle
        with open(PLAYER_INFO_PATH, 'r') as f:
            player_data = f.read().strip()
        if player_data:
            p_parts = player_data.split(',')
            player = [float(p_parts[0]), float(p_parts[1]), float(p_parts[2]),
                      float(p_parts[3]), float(p_parts[4]), float(p_parts[5]), float(p_parts[6])]
        else:
            player = [-999, -999, -999, -999, -999, -999, -999]
        
        # Gundyr data: health, x, y, z, angle
        with open(GUNDYR_INFO_PATH, 'r') as f:
            gundyr_data = f.read().strip()
        if gundyr_data:
            g_parts = gundyr_data.split(',')
            gundyr = [float(g_parts[0]), float(g_parts[1]), float(g_parts[2]), float(g_parts[3]), float(g_parts[4])]
        else:
            gundyr = [-999, -999, -999, -999, -999]
        
        # Combine into state vector
        state = player + gundyr
        return np.array(state, dtype=np.float32)
    except Exception as e:
        print(f"Error reading game state: {e}")
        return np.array([-999] * 12, dtype=np.float32)  # 7 player + 5 gundyr

def get_combat_performance():
    # Use your monitor_fight logic to determine outcome
    player = get_game_state()[:7]  # First 7 are player stats
    gundyr = get_game_state()[7:]  # Last 5 are Gundyr stats
    duration = time.time() - start_time  # Global start_time set in run_fight
    if player[0] <= 0:  # Player health
        return [0, 100, duration]  # [damage_dealt, damage_taken, survival_time]
    elif gundyr[0] <= 0:  # Gundyr health
        return [1000, 100 - player[0] / 10, duration]  # Rough estimate of damage dealt
    else:
        return [max(0, 1037 - gundyr[0]), 100 - player[0] / 10, duration]  # Ongoing fight

# Neural Network Model
class DarkSoulsNN:
    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(32, activation='relu', input_shape=(12,)),  # 12 inputs: 7 player + 5 Gundyr
            layers.Dense(16, activation='relu'),
            layers.Dense(7, activation='softmax')  # 7 actions: forward, back, left, right, attack, dodge, heal
        ])
        return model
    
    def predict(self, state):
        state = np.expand_dims(state, axis=0)
        probabilities = self.model.predict(state, verbose=0)[0]
        return np.argmax(probabilities)  # Action index
    
    def set_weights(self, weights):
        self.model.set_weights(weights)
    
    def get_weights(self):
        return self.model.get_weights()

# Evolutionary Algorithm
class Evolution:
    def __init__(self, population_size=10):
        self.population_size = population_size
        self.population = [DarkSoulsNN() for _ in range(population_size)]
        self.best_model = None
        self.best_fitness = -float('inf')
    
    def evaluate_fitness(self, nn):
        global start_time
        start_time = time.time()
        fight_duration = 60  # Max 60 seconds per fight
        steps = 0
        while steps < 600:  # ~60 seconds at 100ms intervals
            state = get_game_state()
            action = nn.predict(state)
            if action == 0:
                move_forward()
            elif action == 1:
                move_backward()
            elif action == 2:
                move_left()
            elif action == 3:
                move_right()
            elif action == 4:
                attack()
            elif action == 5:
                dodge()
            elif action == 6 and state[2] > 0:  # Heal if estus available
                heal()
            
            performance = get_combat_performance()
            if performance[0] >= 1000 or performance[1] >= 100:  # Win or loss
                break
            time.sleep(0.1)
            steps += 1
        
        # Fitness: reward damage dealt, penalize damage taken, bonus for survival
        fitness = performance[0] - performance[1] * 2 + performance[2] * 0.5
        return fitness
    
    def evolve(self):
        fitness_scores = [self.evaluate_fitness(nn) for nn in self.population]
        max_fitness = max(fitness_scores)
        if max_fitness > self.best_fitness:
            self.best_fitness = max_fitness
            self.best_model = self.population[np.argmax(fitness_scores)]
            print(f"New best fitness: {self.best_fitness}")
        
        sorted_indices = np.argsort(fitness_scores)[::-1]
        elite_size = self.population_size // 5
        elite = [self.population[i] for i in sorted_indices[:elite_size]]
        
        new_population = elite.copy()
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(elite, 2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        
        self.population = new_population
    
    def crossover(self, parent1, parent2):
        child = DarkSoulsNN()
        weights1 = parent1.get_weights()
        weights2 = parent2.get_weights()
        child_weights = []
        for w1, w2 in zip(weights1, weights2):
            mask = np.random.rand(*w1.shape) > 0.5
            child_weights.append(np.where(mask, w1, w2))
        child.set_weights(child_weights)
        return child
    
    def mutate(self, nn):
        weights = nn.get_weights()
        mutated_weights = []
        for w in weights:
            if random.random() < 0.1:
                mutation = np.random.normal(0, 0.1, w.shape)
                mutated_weights.append(w + mutation)
            else:
                mutated_weights.append(w)
        nn.set_weights(mutated_weights)
        return nn

# Main loop
def main():
    # Assuming your Cheat Engine scripts are running
    evolution = Evolution(population_size=10)
    for generation in range(20):
        print(f"Generation {generation + 1}")
        evolution.evolve()
        time.sleep(2)  # Pause between generations
    
    # Test the best model
    print("Testing best model...")
    best_nn = evolution.best_model
    start_time = time.time()
    for _ in range(600):  # ~60 seconds
        state = get_game_state()
        action = best_nn.predict(state)
        if action == 0:
            move_forward()
        elif action == 1:
            move_backward()
        elif action == 2:
            move_left()
        elif action == 3:
            move_right()
        elif action == 4:
            attack()
        elif action == 5:
            dodge()
        elif action == 6 and state[2] > 0:
            heal()
        time.sleep(0.1)

if __name__ == "__main__":
    print("Starting in 5 seconds... Switch to Dark Souls III!")
    time.sleep(5)
    main()