import control_ds3_ml as control
from log_info import log_player_info, log_gundyr_info

import time

locked_on = False


def main():
    # Start the fight
    move_forward()
    enter_fog()
    lock_on()

    while locked_on:
        log_player_info()
        print()
        log_gundyr_info()
        time.sleep(0.1)
    # while True:
    #     # Get the game data
    #     game_data = control.get_game_data()
    #     # Preprocess the data
    #     data = control.preprocess_data(game_data)
    #     # Predict the action
    #     action = model.predict(data)
    #     # Perform the action
    #     control.perform_action(action)
    #     time.sleep(0.1)


def move_forward():
    control.move_forward(2.0)


def enter_fog():
    control.interact()
    time.sleep(2.0)


def lock_on():
    control.keyboard.press('q')
    time.sleep(0.2)
    control.keyboard.release('q')
    global locked_on
    locked_on = True


if __name__ == "__main__":
    main()
