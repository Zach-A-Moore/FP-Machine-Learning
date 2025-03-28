import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import time
import random
import os
import pydirectinput as direct_input
import pyautogui
import logging
import argparse
from threading import Lock

# Command-line argument for console ID
parser = argparse.ArgumentParser(description="Dark Souls III NN Training")
parser.add_argument("--console-id", type=str, default="1", help="Unique ID for this console instance")
args = parser.parse_args()
CONSOLE_ID = args.console_id

# Setup logging
logging.basicConfig(filename=f"ds3_nn_{CONSOLE_ID}.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# File paths (unique per console)
base_dir = os.path.dirname(os.path.abspath(__file__))
PLAYER_INFO_PATH = os.path.join(base_dir, "data", f"player_info_{CONSOLE_ID}.txt")
GUNDYR_INFO_PATH = os.path.join(base_dir, "data", f"gundyr_info_{CONSOLE_ID}.txt")
MODEL_SAVE_PATH = os.path.join(base_dir, "models", f"best_model_{CONSOLE_ID}.h5")
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)

# Lock for file access (multi-threading safety)
file_lock = Lock()

# Game input functions
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
        with file_lock:
            with open(PLAYER_INFO_PATH, 'r') as f:
                player_data = f.read().strip()
            with open(GUNDYR_INFO_PATH, 'r') as f:
                gundyr_data = f.read().strip()
        
        if player_data and gundyr_data:
            p_parts = player_data.split(',')
            player = [float(x) for x in p_parts[:7]]  # health, stamina, estus, x, y, z, angle
            
            g_parts = gundyr_data.split(',')
            gundyr = [float(x) for x in g_parts[:5]]  # health, x, y, z, angle
            
            state = player + gundyr
            return np.array(state, dtype=np.float32)
        else:
            return np.array([-999] * 12, dtype=np.float32)
    except Exception as e:
        logging.error(f"Error reading game state: {e}")
        return np.array([-999] * 12, dtype=np.float32)

def get_combat_performance(start_time):
    state = get_game_state()
    player_hp, gundyr_hp = state[0], state[7]
    duration = time.time() - start_time
    if player_hp <= 0:
        return [0, 100, duration]
    elif gundyr_hp <= 0:
        return [1000, 100 - player_hp / 10, duration]
    else:
        return [max(0, 1037 - gundyr_hp), 100 - player_hp / 10, duration]

# Neural Network Model
class DarkSoulsNN:
    def __init__(self):
        self.model = self.build_model()
    
    def build_model(self):
        model = tf.keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(12,)),  # Increased capacity
            layers.Dense(32, activation='relu'),
            layers.Dense(7, activation='softmax')  # 7 actions
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model
    
    def predict(self, state):
        state = np.expand_dims(state, axis=0)
        probabilities = self.model.predict(state, verbose=0)[0]
        return np.argmax(probabilities)
    
    def set_weights(self, weights):
        self.model.set_weights(weights)
    
    def get_weights(self):
        return self.model.get_weights()
    
    def save(self, path):
        self.model.save(path)
        logging.info(f"Model saved to {path}")

# Evolutionary Algorithm
class Evolution:
    def __init__(self, population_size=10):
        self.population_size = population_size
        self.population = [DarkSoulsNN() for _ in range(population_size)]
        self.best_model = None
        self.best_fitness = -float('inf')
        self.last_save_time = time.time()
    
    def evaluate_fitness(self, nn):
        start_time = time.time()
        steps = 0
        max_steps = 600  # ~60s
        while steps < max_steps:
            state = get_game_state()
            if np.all(state == -999):  # Invalid state, retry
                time.sleep(0.1)
                continue
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
            elif action == 6 and state[2] > 0:  # Estus check
                heal()
            
            perf = get_combat_performance(start_time)
            if perf[0] >= 1000 or perf[1] >= 100:  # Win/loss
                break
            time.sleep(0.1)
            steps += 1
        
        fitness = perf[0] - perf[1] * 2 + perf[2] * 0.5
        logging.info(f"Fitness: {fitness}, Perf: {perf}")
        return fitness
    
    def evolve(self):
        fitness_scores = []
        for nn in self.population:
            try:
                fitness = self.evaluate_fitness(nn)
                fitness_scores.append(fitness)
            except Exception as e:
                logging.error(f"Error in fitness evaluation: {e}")
                fitness_scores.append(-float('inf'))
        
        max_fitness = max(fitness_scores)
        if max_fitness > self.best_fitness:
            self.best_fitness = max_fitness
            self.best_model = self.population[np.argmax(fitness_scores)]
            logging.info(f"New best fitness: {self.best_fitness}")
        
        sorted_indices = np.argsort(fitness_scores)[::-1]
        elite_size = max(1, self.population_size // 5)
        elite = [self.population[i] for i in sorted_indices[:elite_size]]
        
        new_population = elite.copy()
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(elite, 2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)
        
        self.population = new_population
        
        # Save best model every 20 minutes
        current_time = time.time()
        if current_time - self.last_save_time >= 1200:  # 20 minutes
            if self.best_model:
                self.best_model.save(MODEL_SAVE_PATH)
            self.last_save_time = current_time
    
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
    logging.info(f"Starting NN training on console {CONSOLE_ID}")
    evolution = Evolution(population_size=10)
    
    # Load existing model if available
    if os.path.exists(MODEL_SAVE_PATH):
        evolution.best_model = DarkSoulsNN()
        evolution.best_model.model = tf.keras.models.load_model(MODEL_SAVE_PATH)
        evolution.best_fitness = -float('inf')  # Re-evaluate
        logging.info(f"Loaded existing model from {MODEL_SAVE_PATH}")
    
    start_time = time.time()
    generation = 0
    while time.time() - start_time < 30 * 24 * 60 * 60:  # 1 month
        generation += 1
        logging.info(f"Generation {generation}")
        try:
            evolution.evolve()
        except Exception as e:
            logging.error(f"Error in generation {generation}: {e}")
        time.sleep(2)
    
    # Final save
    if evolution.best_model:
        evolution.best_model.save(MODEL_SAVE_PATH)
        logging.info("Final model saved")

if __name__ == "__main__":
    print(f"Starting in 5 seconds on console {CONSOLE_ID}... Switch to Dark Souls III!")
    time.sleep(5)
    main()