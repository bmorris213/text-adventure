# Text Adventure
# 05-30-24
# Brian Morris

import threading
from queue import Queue
from displaymanager import GameWindow
from gamemanager import GameManager

# Main
# program begins execution here
# execution is passed to game manager
def main():
    # start a new game window, hand it the new stdin
    new_stdin = StdinHandler()
    app = GameWindow(new_stdin)

    # initialize game environment
    game_logic = GameManager(new_stdin)
    
    # Start game manager in a separate thread
    gm_thread = threading.Thread(target=game_logic.run)
    gm_thread.daemon = True
    gm_thread.start()

    # run game window with game manager
    app.run()

# handles stdin redirection
class StdinHandler:
    def __init__(self):
        self.input_queue = Queue()

    def get_input(self):
        return self.input_queue.get()

    def put_input(self, input_data):
        self.input_queue.put(input_data)

if __name__ == '__main__':
    main()