import time
import pyautogui
# replaced pynput keyboard with pyDirectInput
import pydirectinput as direct_input
# from tensorflow.keras.models import load_model

# Check if locked on to boss or not
LockedOn = False
estus = 3

# Movement

# TODO: RESET ESTUS


def move_forward(duration=1.0):
    direct_input.keyDown('w')
    time.sleep(duration)
    direct_input.keyUp('w')


def move_backward(duration=1.0):
    direct_input.keyDown('s')
    time.sleep(duration)
    direct_input.keyUp('s')


def move_left(duration=1.0):
    direct_input.keyDown('a')
    time.sleep(duration)
    direct_input.keyUp('a')


def move_right(duration=1.0):
    direct_input.keyDown('d')
    time.sleep(duration)
    direct_input.keyUp('d')

# Actions


def interact():
    direct_input.keyDown('e')
    time.sleep(0.2)
    direct_input.keyUp('e')


def lock_on():
    direct_input.keyDown('q')
    time.sleep(0.2)
    direct_input.keyUp('q')


def heal():
    global estus
    if estus == 0:
        return
    direct_input.keyDown('r')
    time.sleep(0.2)
    direct_input.keyUp('r')
    estus -= 1


def attack():
    pyautogui.click()


def dodge():
    direct_input.keyDown('space')
    time.sleep(0.2)
    direct_input.keyUp('space')

# Helper functions


def focus_on_game():
    # Hold alt and press tab with extended delays
    direct_input.keyDown('alt')
    time.sleep(0.2)
    direct_input.press('tab')
    time.sleep(0.2)
    direct_input.keyUp('alt')
    time.sleep(0.3)  # give OS time to switch
    # Release alt and tab keys
    direct_input.keyUp('alt')
    time.sleep(0.1)

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
