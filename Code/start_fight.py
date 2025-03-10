import threading
import control_ds3_ml as control
from log_info import log_player_info, log_gundyr_info
from pynput.keyboard import Key  # add this import at the top if not present
import pydirectinput as direct_input
import time

locked_on = False
running = True  # flag for stopping logging threads


def main():
    control.focus_on_game()
    control.move_forward(2)
    control.interact()
    control.lock_on()

    # Start logging functions in separate threads without setting daemon=True
    player_thread = threading.Thread(
        target=log_player_info, args=(lambda: running,))
    gundyr_thread = threading.Thread(
        target=log_gundyr_info, args=(lambda: running,))
    player_thread.start()
    gundyr_thread.start()

    while locked_on:
        time.sleep(0.1)

    # Signal threads to stop and wait for them to exit gracefully
    global running
    running = False
    player_thread.join()
    gundyr_thread.join()


def move_forward():
    control.keyboard.press('w')
    time.sleep(2)
    control.keyboard.release('w')


def enter_fog():
    control.keyboard.press('e')
    time.sleep(0.2)
    control.keyboard.release('e')


def lock_on():
    control.keyboard.press('q')
    time.sleep(0.2)
    control.keyboard.release('q')
    global locked_on
    locked_on = True


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


if __name__ == "__main__":
    main()
