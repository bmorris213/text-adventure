# Text Adventure
# 06-10-2024
# Brian Morris

import threading
from queue import Queue
from displaymanager import GameWindow
from gamemanager import GameManager

# Main
# program begins execution here
# execution is passed to game manager
def main():
    # define a new stdin behavior
    new_stdin = StdinHandler()
    
    # define a method of interaction from game manager to window
    command_queue = Queue()

    # initialize game environment
    game_logic = GameManager(new_stdin, command_queue)
    
    # Start game manager in a separate thread
    gm_thread = threading.Thread(target=game_logic.run)
    gm_thread.daemon = True
    gm_thread.start()

    # start the game window with the new stdin, the subprocess thread, and the command queue
    app = GameWindow(new_stdin, gm_thread, command_queue)

    # grab animation speed from game_manager
    animation_speed = game_logic.config.text_delay

    # grab the command_queue command words
    clear_command = game_logic.CLEAR_COMMAND
    change_title = game_logic.CHANGE_TITLE
    change_speed = game_logic.CHANGE_SPEED

    # set animation speed
    app.set_speed(animation_speed)

    # set command words
    app.set_commands(clear_command, change_title, change_speed)

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