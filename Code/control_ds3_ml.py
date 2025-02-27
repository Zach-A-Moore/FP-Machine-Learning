import time
import pyautogui
from pynput.keyboard import Key, Controller
# from tensorflow.keras.models import load_model


# Controller from pynput
keyboard = Controller()

# Check if locked on to boss or not
LockedOn = False
estus = 3

# Movement

# TODO: RESET ESTUS


def move_forward(duration=1.0):
    keyboard.press('w')
    time.sleep(duration)
    keyboard.release('w')


def move_backward(duration=1.0):
    keyboard.press('s')
    time.sleep(duration)
    keyboard.release('s')


def move_left(duration=1.0):
    keyboard.press('a')
    time.sleep(duration)
    keyboard.release('a')


def move_right(duration=1.0):
    keyboard.press('d')
    time.sleep(duration)
    keyboard.release('d')

# Actions


def interact():
    keyboard.press('e')
    time.sleep(0.2)
    keyboard.release('e')


def lock_on():
    keyboard.press('q')
    time.sleep(0.2)
    keyboard.release('q')


def heal():
    if estus == 0:
        return
    keyboard.press('r')
    time.sleep(0.2)
    keyboard.release('r')
    estus -= 1


def attack():
    pyautogui.click()


def dodge():
    keyboard.press(Key.space)
    time.sleep(0.2)
    keyboard.release(Key.space)


# def LockOn():
#     if LockedOn == False:
#         keyboard.press('q')
#         time.sleep(0.2)
#         keyboard.release('q')
#     else:
#         return


# def main():
#     # Same file as Cheat Engine script
#     file_path = "C:\\Users\\Laween\\Downloads\\game_data.txt"


#     print("Listening for game data...")
#     while True:
#         try:
#             with open(file_path, "r") as file:
#                 data = file.read().strip()
#                 if data:
#                     health, stamina, x, y, z = map(float, data.split(","))

#                     # Example AI logic (replace with ML model later)
#                     if health < 50:
#                         print("Low health! Dodging...")
#                         dodge()
#                     elif stamina > 30:
#                         print("Attacking...")
#                         attack()
#                     else:
#                         print("Moving forward...")
#                         move_forward()

#         except Exception as e:
#             print(f"Error reading file: {e}")

#         time.sleep(0.1)  # Adjust based on performance


# model = load_model("ds3_ai_model.h5")  # Load trained AI

# def predict_action(health, stamina, x, y, z):
#     input_data = [[health, stamina, x, y, z]]
#     action_index = model.predict(input_data).argmax()
#     return ["move", "attack", "dodge"][action_index]  # Example action list
# action = predict_action(health, stamina, x, y, z)
# if action == "move":
#     move_forward()
# elif action == "attack":
#     attack()
# elif action == "dodge":
#     dodge()
