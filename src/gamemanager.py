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
    MAIN_MENU_SIGNITURES = ["main menu", "options", "load game", "extras"]

    # main menu functions
    def _main_new_funct(self, objects, targets=None):
        # get name for new save file
        textmanager.display_text("Starting new adventure!", self.text_delay)
        textmanager.display_text("First thing's first: what is your name?", self.text_delay)

        new_name = None
        has_name = False
        while has_name == False:
            new_name = textmanager.get_input(self.input_handler)

            has_name = textmanager.ask_yes_or_no(f"Should I call you \"{new_name}\"?", self.text_delay)
        
        # hand party manager the new name

        # read in default world data to give to worldmanager

        # switch to new_game mode from worldmanager
        self.command_queue.put(f"change title:{new_name}")
        return f"{Mode.CHANGE_MODE}start new game"
    def _main_continue_funct(self, objects, targets=None):
        # run load menu load function on most_recent_save
        return f"{Mode.CHANGE_MODE}continue"
    def _main_load_funct(self, objects, targets=None):
        # pass to load submenu
        return f"{Mode.CHANGE_MODE}load game"
    def _main_option_funct(self, objects, targets=None):
        # pass to options submenu
        return f"{Mode.CHANGE_MODE}options"
    def _main_extra_funct(self, objects, targets=None):
        # pass to extras submenu
        return f"{Mode.CHANGE_MODE}extras"
    def _init_main_menu(self):
        prompt = "MAIN MENU"
        if(False):
            prompt += "\n => Continue"
        prompt += "\n => New\n => Load\n => Options\n => Extras\n => Quit"
        result = Mode(prompt)
        result.add_command("new", self._main_new_funct, "Begin a new adventure!")
        result.add_command("continue", self._main_continue_funct, "Continue where you last left off.")
        result.add_command("load", self._main_load_funct, "Continue one of your saved adventures.")
        result.add_command("options", self._main_option_funct, "Change settings for the game.")
        result.add_command("extras", self._main_extra_funct, "View achievements and credits.")
        return result

    # load game submenu functions
    def _load_game_funct(self, objects, targets=None):
        # ensure targets is list type
        if isinstance(targets, str) == True:
            targets = [targets]
        
        # load game needs target file
        if targets == None:
            return "I need to know which file you'll be loading... Try \"look\" to see which files I have saved."
        elif len(targets) > 1:
            return "I can only load one file at a time."
        
        # validate target file exists
        t_file = targets[0]
        if t_file not in objects.keys():
            return f"There's no file here named \"{t_file}\". Try \"look\" to see which files I have saved."
        
        # hand party manager the file's name

        # read in save data from file's name

        # switch to continue_game mode from worldmanager
        self.command_queue.put(f"change title:{t_file}")
        return f"{textmanager.CHANGE_MODE}load world"
    def _load_delete_funct(self, objects, targets=None):
        # ensure targets is a list type
        if isinstance(targets, str) == True:
            targets = [targets]
        
        # delete file needs a target
        if targets == None:
            return "I need to know which file you'll be deleting... Try \"look\" to see which files I have saved."

        files_to_delete = []
        for target in targets:
            if target not in objects.keys():
                return f"There is no file here named \"{target}\". Try \"look\" to see which files I have saved."
            files_to_delete.append(target)

        can_delete = textmanager.ask_yes_or_no("Are you sure you want to delete these files?", self.text_delay)

        if can_delete == False:
            return f"Understood."
        
        # delete save files
        return "Files deleted..."
    def _init_load_menu(self):
        result = Mode("Load Game\nTry \"look\" to inspect files I have saved.")
        result.add_command("load", self._load_game_funct, "Load one of the files saved to disk.")
        result.add_command("delete", self._load_delete_funct, "Delete one or more save files.")
        # add all files on disk as objects in this mode
        return result

    # initialize game environment
    def __init__(self, input_handler, command_queue):
        # initialize configuration options and variables
        self.text_delay = textmanager.NORMAL_TEXT
        self.display_welcome = True

        # initialize default variables
        self.input_handler = input_handler
        self.command_queue = command_queue
        self.user_name = None

        # set up mode variables
        self.modes = {}
        self.current_mode = None
        self.last_mode = None
        
        self.current_signature = None
        self.last_signature = None

        # initialize modes
        self.modes["main menu"] = self._init_main_menu()
        self.modes["load game"] = self._init_load_menu()
    
    # run a session of game
    def run(self):
        if self.display_welcome == True:
            # for game startup, display welcome message, explain how to play the game, and wait for buffer
            self.command_queue.put("display text:Welcome to Text Adventure!\n ")
            self.command_queue.put("display text:To play, give me a command followed by any amount of targets.")
            self.command_queue.put("display text:To see which commands are valid at any time use \"help\".")
            self.command_queue.put("display text:To see which targets you can reference, use \"look\".")
            self.command_queue.put("display text:To exit the game, type \"quit\".")
            self.command_queue.put("display text:To keep this message from popping up on startup, go to options and set \"display welcome message\" to \"no\".\n ")
            self.command_queue.put("clear")
            buffer = textmanager.get_input(self.input_handler)

        self.current_mode = self.modes["main menu"]
        self.current_signature = "main menu"

        for line in self.current_mode.prompt.split('\n'):
            self.command_queue.put(f"display text:{line}")
        self.command_queue.put("display text:-------------------\n")

        # begin gameplay loop
        while(True):
            verb, nouns = textmanager.get_input(self.input_handler)

            if verb == None:
                textmanager.display_text("You've entered invalid characters. I only take spaces and a-z.", self.text_delay)
                continue

            mode_return = self.current_mode.run_command(verb, nouns)

            if mode_return == None:
                if self.current_mode.is_command(verb) == False:
                    textmanager.display_text(f"\"{verb}\" isn't a valid command.\nTry \"help\" for a list of commands.", self.text_delay)
                    continue

                display_text = f"I didn't quite understand \"{verb}"
                if nouns != None and len(nouns) != 0:
                    for noun in nouns:
                        display_text += f" {noun}"
                
                textmanager.display_text(f"{display_text}\"...\nTry typing \"help {verb}\" for help with that command.", self.text_delay)
                continue

            # test for mode return types other than string
            has_invalid_noun = False
            if isinstance(mode_return, str) == False:
                # try list
                if isinstance(mode_return, list) == True:
                    if None in mode_return:
                        for noun in nouns:
                            if self.current_mode.is_valid(noun) == False:
                                textmanager.display_text(f"There is nothing like \"{noun}\" here.\nTry typing \"look\" to see what is around.", self.text_delay)
                                has_invalid_noun = True
                                break
                
                # try dict
                if isinstance(mode_return, dict) == True:
                    for target, result in mode_return.items():
                        if result == None:
                            textmanager.display_text(f"There is nothing like \"{target}\" here.\nTry typing \"look\" to see what is around.", self.text_delay)
                            has_invalid_noun = True
                            break
            
            # test for invalid noun used
            if has_invalid_noun == True:
                continue
            
            # just print whatever is smaller than CHANGE_MODE
            if len(mode_return) < len(Mode.CHANGE_MODE):
                textmanager.display_text(mode_return, self.text_delay)
                continue

            # if it doesn't contain CHANGE_MODE, just print it
            if mode_return[:len(Mode.CHANGE_MODE)] != Mode.CHANGE_MODE:
                textmanager.display_text(mode_return, self.text_delay)
                continue

            mode_signature = mode_return[len(Mode.CHANGE_MODE):]
            new_mode = None

            if mode_signature == Mode.QUIT_SIGNITURE:
                can_quit = True
                if self.current_signature not in self.MAIN_MENU_SIGNITURES: # we can skip confirming from main menu
                    can_quit = textmanager.ask_yes_or_no("Are you sure you want to quit? You will lose any unsaved progress.", self.text_delay)

                if can_quit==False:
                    textmanager.display_text("Understood.", self.text_delay)
                    continue
                else:
                    textmanager.display_text("Goodbye!", self.text_delay)
                    break
            elif mode_signature == Mode.BACK_SIGNITURE:
                if self.current_signature == "main menu":
                    textmanager.display_text("Can't go back any further than main menu!", self.text_delay)
                    continue
                new_mode = self.last_mode
            else:
                for key_string, mode in self.modes.items():
                    if mode_signature == key_string:
                        new_mode = mode
                        break

            # mode to change to was invalid
            
            if new_mode == None:
                textmanager.display_text(f"I don't understand what \"{mode_signature}\" means.", self.text_delay)
                continue

            if mode_signature == "back":
                temp = self.current_signature
                self.current_signature = self.last_signature
                self.last_signature = temp
            else:
                self.last_signature = self.current_signature
                self.current_signature = mode_signature
            self.last_mode = self.current_mode
            self.current_mode = new_mode

            textmanager.display_text("Changing modes...", self.text_delay)
            self.command_queue.put("clear") # send clear command to controlling window which waits on input buffer
            buffer = textmanager.get_input(self.input_handler) # hold execution here to buffer the terminal for screen clear
            
            for line in self.current_mode.prompt.split('\n'):
                self.command_queue.put(f"display text:{line}")
            self.command_queue.put("display text:-------------------\n")
