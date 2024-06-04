# Text Adventure
# 05-30-24
# Brian Morris

import os
import sys

import errormanager
import filemanager
import textmanager
import partymanager
import worldmanager
import encountermanager
from mode import Mode

# Game Manager
# Stores and Mutates all game states
# Handles all program delegation
class GameManager():
    MAIN_MENU_SIGNITURES = ["try"]
    # initialize game environment
    def __init__(self, input_handler, command_queue):
        # initialize configuration options and variables
        self.text_delay = 0.15
        self.modes = {}
        self.current_mode = None
        self.last_mode = None

        self.input_handler = input_handler
        self.command_queue = command_queue

        # initialize modes
        only_mode = Mode("This is a game")
        def dummy_command(objects, nouns=None):
            return "Yes, this is a game."
        only_mode.add_command("try", dummy_command)
        self.modes["try"] = only_mode
    
    # run a session of game
    def run(self):
        self.current_mode = self.modes["try"]
        self.current_signiture = "try"

        # begin gameplay loop
        while(True):
            verb, nouns = textmanager.get_input(self.input_handler)

            if verb == None:
                textmanager.display_text("You've entered invalid characters. I only take spaces and a-z.", self.text_delay)
                continue

            mode_return = self.current_mode.run_command(verb, nouns)

            if mode_return == None:
                if verb == None:
                    continue

                display_text = f"I didn't quite understand \"{verb}"
                if nouns != None and len(nouns) != 0:
                    for noun in nouns:
                        display_text += f" {noun}"
                textmanager.display_text(f"{display_text}\"...\nTry typing \"help {verb}\" for help with that command.", self.text_delay)
                continue
            
            if len(mode_return) < len(Mode.CHANGE_MODE):
                textmanager.display_text(mode_return, self.text_delay)
                continue

            mode_signiture = mode_return[len(Mode.CHANGE_MODE):]
            new_mode = None

            if mode_signiture == Mode.QUIT_SIGNITURE:
                can_quit = True
                if self.current_signiture not in self.MAIN_MENU_SIGNITURES:
                    can_quit = textmanager.ask_yes_or_no("Are you sure you want to quit? You will lose any unsaved progress.", self.text_delay)

                if can_quit==False:
                    textmanager.display_text("Understood.", self.text_delay)
                    continue
                else:
                    textmanager.display_text("Goodbye!", self.text_delay)
                    break
            elif mode_signiture == Mode.BACK_SIGNITURE:
                new_mode = self.last_mode
            else:
                for key_string, mode in self.modes.items():
                    if mode_signiture == key_string:
                        new_mode = mode
                        break
            
            if new_mode == None:
                # new mode is longer than CHANGE_MODE string, but isn't change mode
                textmanager.display_text(mode_return, self.text_delay)
                continue
            
            self.last_mode = self.current_mode
            self.current_mode = new_mode

            textmanager.display_text("Changing modes...", self.text_delay)
            command_queue.put("clear") # send clear command to controlling window

            textmanager.display_text(new_mode.prompt, self.text_delay)

            for key, value in self.modes.items():
                if value == self.current_mode:
                    self.current_signiture = key
                    break
