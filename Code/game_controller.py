import time
import pyautogui


class DarkSoulsController:
    def __init__(self, delay=0.1):
        self.delay = delay

    def attack(self):
        # Simulates an attack action.
        print("Performing attack...")
        pyautogui.press('j')  # Adjust the key mapping as needed.
        time.sleep(self.delay)

    def block(self):
        # Simulates blocking.
        print("Blocking...")
        pyautogui.press('k')  # Adjust the key mapping as needed.
        time.sleep(self.delay)

    def roll(self):
        # Simulates a roll/dodge action.
        print("Rolling...")
        pyautogui.press('space')  # Adjust the key mapping as needed.
        time.sleep(self.delay)

    def move_forward(self, duration=1):
        # Simulates moving forward by holding down 'w'.
        print(f"Moving forward for {duration} seconds...")
        pyautogui.keyDown('w')
        time.sleep(duration)
        pyautogui.keyUp('w')
        time.sleep(self.delay)

    def get_game_data(self):
        # Placeholder for retrieving game data.
        # In practice, game data would be extracted via logs, memory reading,
        # or a game API if available. This returns example data.
        print("Retrieving game data...")
        data = {
            "player_health": 100,
            "enemy_count": 5,
            "current_area": "Firelink Shrine"
        }
        return data


def main():
    controller = DarkSoulsController()

    print("Dark Souls 3 Controller")
    print("Available commands: attack, block, roll, move, data, quit")

    while True:
        cmd = input("Enter command: ").strip().lower()
        if cmd == "attack":
            controller.attack()
        elif cmd == "block":
            controller.block()
        elif cmd == "roll":
            controller.roll()
        elif cmd == "move":
            duration = input("Enter duration to move forward (seconds): ")
            try:
                duration = float(duration)
            except ValueError:
                print("Invalid duration - using default 1 second.")
                duration = 1
            controller.move_forward(duration)
        elif cmd == "data":
            data = controller.get_game_data()
            print("Game Data:", data)
        elif cmd == "quit":
            print("Exiting controller.")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    main()
