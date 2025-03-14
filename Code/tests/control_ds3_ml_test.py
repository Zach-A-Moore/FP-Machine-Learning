import time
import pandas as pd
import pyautogui
from pynput.keyboard import Key, Controller

# Load the dataset
# Update the path if needed
file_path = r"C:\\Users\\Laween\\OneDrive\Desktop\\MSUM\Spring_2025\\490\\Final_Project\Dark_Souls\\FP-Machine-Learning\\Code\\game_data.csv"
df = pd.read_csv(file_path)

keyboard = Controller()

# Define action functions


def move_forward():
    keyboard.press('w')
    time.sleep(0.5)
    keyboard.release('w')


def move_backward():
    keyboard.press('s')
    time.sleep(0.5)
    keyboard.release('s')


def move_left():
    keyboard.press('a')
    time.sleep(0.5)
    keyboard.release('a')


def move_right():
    keyboard.press('d')
    time.sleep(0.5)
    keyboard.release('d')


def attack():
    pyautogui.click()


def dodge():
    keyboard.press(Key.space)
    time.sleep(0.2)
    keyboard.release(Key.space)


# Mapping actions to functions
action_map = {
    "move_forward": move_forward,
    "move_backward": move_backward,
    "move_left": move_left,
    "move_right": move_right,
    "attack": attack,
    "dodge": dodge
}

print("Starting AI-controlled gameplay...")
time.sleep(3)  # Gives time to switch to the game

# Loop through the dataset and simulate actions
for _, row in df.iterrows():
    action = row["action"]ad
    if action in action_map:
        print(f"Performing action: {action}")
        action_map[action]()
    time.sleep(0.1)  # Small delay between actions

print("Finished executing dataset.")
