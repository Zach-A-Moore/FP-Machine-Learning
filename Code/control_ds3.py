import time
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()

# Simulate movement


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


# Simulate attack (LMB)


def attack():
    pyautogui.click()

# Simulate dodge (Roll - B button on Xbox, Space on PC)


def dodge():
    keyboard.press(Key.space)
    time.sleep(0.2)
    keyboard.release(Key.space)


# Example usage
if __name__ == "__main__":
    time.sleep(3)  # Gives you 3 seconds to switch to the game
    move_forward(2)  # Move forward for 2 seconds
    attack()  # Attack
    attack()  # Attack
    dodge()  # Dodge
    move_left(3)  # Move left for 1 second
    move_right(1)  # Move right for 1 second
    move_backward(1)  # Move backward for 1 second
    attack()  # Attack
