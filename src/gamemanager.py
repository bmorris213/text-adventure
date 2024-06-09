# Text Adventure
# 06-10-2024
# Brian Morris

import os
import sys

import errormanager
import filemanager
import textmanager
from worldmanager import WorldManager
from mode import Mode

# Game Manager
# Stores and Mutates all game states
# Handles all program delegation
class GameManager():
    # configuration data struct
    # holds options for game manager for serialization
    # initialization will always use default
    class Configuration:
        def __init__(self):
            # options menu
            self.sound_volume = 1
            self.music_volume = 1
            self.master_volume = 0.75
            self.text_delay = 0.01
            self.display_welcome = True
            
            # save data
            self.saves = {}
            self.most_recent_save = None
        
        def __str__(self):
            rep = f"[SOUND] sound volume: {int(10 * self.sound_volume)}\n"
            rep += f"[MUSIC] music volume: {int(10 * self.music_volume)}\n"
            rep += f"[MASTER] master volume: {int(10 * self.master_volume)}\n"
            rep += "[DELAY] speed of text: "
            if self.text_delay == GameManager.SLOW_TEXT:
                rep += "slow\n"
            elif self.text_delay == GameManager.NORMAL_TEXT:
                rep += "normal\n"
            elif self.text_delay == GameManager.QUICK_TEXT:
                rep += "quick\n"
            rep += "[WELCOME] display welcome message: "
            if self.display_welcome == True:
                rep += "yes\n"
            else:
                rep += "no\n"
            return rep
        
        def change_value(self, target, new_value):
            if target == "sound" or target == "music" or target == "master":
                if new_value.isnumeric() == False or int(new_value) > 10:
                    textmanager.display_text("Volume is set using a number from 1 to 10.")
                    return False
            
            if target == "delay":
                if new_value != "slow" and new_value != "normal" and (new_value != "quick" and new_value != "fast"):
                    textmanager.display_text("The speed of text should be set to \"slow\", \"normal\", or \"quick\".")
                    return False
            
            if target == "welcome":
                if new_value != "no" and new_value != "yes":
                    textmanager.display_text("The value required for this setting is \"yes\" or \"no\".")
                    return False

            if target == "sound":
                self.sound_volume = (float(new_value) / 10)
            elif target == "music":
                self.music_volume = (float(new_value) / 10)
            elif target == "master":
                self.master_volume = (float(new_value) / 10)
            elif target == "delay":
                if new_value == "slow":
                    self.text_delay = GameManager.SLOW_TEXT
                elif new_value == "normal":
                    self.text_delay = GameManager.NORMAL_TEXT
                elif new_value == "quick" or new_value == "fast":
                    self.text_delay = GameManager.QUICK_TEXT
            elif target == "welcome":
                self.display_welcome = new_value == "yes"
            else:
                textmanager.display_text(f"There is no option \"{target}\" to change.")
                return False
            
            return True

    # mode signatures
    MAIN_MENU_MODE = "main menu"
    LOAD_MENU_MODE = "load game"
    OPTION_MENU_MODE = "options"
    START_ADVENTURE = "begin playing game"
    COMPLETE_BREAK = "break out of gameplay, restart game conditions"

    # command queue commands
    CHANGE_TITLE = "change title:"
    CLEAR_COMMAND = "clear"
    CHANGE_SPEED = "change animation speed:"

    MAIN_MENU_TITLE = "Main Menu"

    # text speeds
    SLOW_TEXT = 0.05
    NORMAL_TEXT = 0.03
    QUICK_TEXT = 0.01

    # ==== main menu mode functions ====

    def _main_new_funct(self, objects, targets=None):
        if targets != None and len(targets) != 0 and targets[0] != "game":
            return "The \"new\" command only makes sense here with target \"game\"."
        # get name for new save file
        textmanager.display_text("Starting new adventure!\nFirst thing's first: what is your name?")

        new_name = None
        has_name = False
        while has_name != None:
            # grab user input
            new_name = self.input_handler.get_input()
            new_name = textmanager.clean_name(new_name)

            # ensure name is valid
            if new_name == None:
                textmanager.display_text("I can't use that name; try to use only a-z and spaces.")
                continue

            # add break to loop
            if new_name == "quit" or new_name == "back" or new_name == "stop":
                # print out text_argument, and wait for return from user
                textmanager.display_text("Understood. Taking you back to the main menu.")
                self.command_queue.put(self.CLEAR_COMMAND)
                buffer = textmanager.get_input(self.input_handler)

                # print out new prompt after clear screen
                textmanager.display_text(f"{self.current_mode.prompt}\n{textmanager.END_MARKER}", True)
                return f"\n"
                
            # look for existing name
            if new_name in self.config.saves.keys():
                textmanager.display_text(f"There is already a save file with the name \"{new_name}\".")

            # check user is sure
            has_name = textmanager.ask_yes_or_no(f"Should I call you \"{new_name}\"?", self.input_handler)

            # repeat if not
            if has_name == "quit":
                # print out text_argument, and wait for return from user
                textmanager.display_text("Understood. Taking you back to the main menu.")
                self.command_queue.put(self.CLEAR_COMMAND)
                buffer = textmanager.get_input(self.input_handler)

                # print out new prompt after clear screen
                textmanager.display_text(f"{self.current_mode.prompt}\n{textmanager.END_MARKER}", True)
                return f"\n"
            elif has_name != None:
                textmanager.display_text("Understood. What should I call you then?")

        # for new games we rely on the constructor to initialize the new world
        self.world_state = WorldManager()
            
        # hand world manager the new name
        self.world_state.name(new_name)

        # switch to gameplay mode from worldmanager
        return f"{Mode.CHANGE_MODE}{GameManager.START_ADVENTURE}"

    def _main_continue_funct(self, objects, targets=None):
        if targets != None and len(targets) != 0 and targets[0] != "game":
            return "The \"continue\" command only makes sense here with target \"game\"."
        # there is nothing to continue if there are no saves
        if len(self.config.saves) == 0 or most_recent_save == None:
            return "There is no progress to continue. Try starting a new adventure!"

        # for new games we rely on the constructor to initialize the new world
        self.world_state = WorldManager()

        # name world
        self.world_state.name(self.most_recent_save)

        # remove spaces from file's name
        clean_name = ""
        for char in t_file:
            if char == " ":
                clean_name += "-"
            else:
                clean_name += char

        # grab world data
        world_data = filemanager.read_data(clean_name, WorldManager.World)
        self.world_state.load(world_data)
            
        # switch to gameplay mode from worldmanager
        return f"{Mode.CHANGE_MODE}{self.START_ADVENTURE}"

    def _main_load_funct(self, objects, targets=None):
        if targets != None and len(targets) != 0 and targets[0] != "game":
            return "The \"load\" command only makes sense here with target \"game\"."
        # there is nothing to do in the load menu if there are no saves
        if len(self.config.saves) == 0:
            return "There are no saves to load."
        # pass to load submenu
        return f"{Mode.CHANGE_MODE}load game"

    def _main_option_funct(self, objects, targets=None):
        if targets != None:
            return "The \"options\" command only makes sense here without specifying targets."
        # pass to options submenu
        return f"{Mode.CHANGE_MODE}options"

    def _init_main_menu(self):
        prompt = "MAIN MENU\n => New\n => Continue\n => Load\n => Options\n => Quit"
        result = Mode(prompt)
        result.add_command("new", self._main_new_funct, "Begin a new adventure!")
        result.add_command("continue", self._main_continue_funct, "Continue where you last left off.")
        result.add_command("load", self._main_load_funct, "Continue one of your saved adventures.")
        result.add_command("options", self._main_option_funct, "Change settings for the game.")
        return result

    # ==== load game submenu functions ====

    def _load_game_funct(self, objects, targets=None):
        # ensure targets is list type
        if isinstance(targets, str) == True:
            targets = [targets]
            
        # load only works if there are targets for load
        if len(objects) == 0:
            return "There are no files to load."
            
        # load game needs target file
        if targets == None:
            return "I need to know which file you'll be loading... Try \"look\" to see which files I have saved."
        elif len(targets) > 1 or targets[0] == Mode.ALL_OBJECTS:
            return "I can only load one file at a time."

        # remove spaces from file's name
        clean_name = ""
        for char in targets[0]:
            if char == " ":
                clean_name += "-"
            else:
                clean_name += char
            
        # validate target file exists
        if filemanager.locate_file(clean_name) == None:
            return f"There's no file here named \"{targets[0]}\". Try \"look\" to see which files I have saved."
            
        # grab world data from file
        world_data = filemanager.read_data(clean_name, WorldManager.World)
        self.world_state = WorldManager()
        self.world_state.load(world_data)
            
        # hand world manager the file's name
        self.world_state.name(targets[0])

        # switch to gameplay mode from world manager
        return f"{textmanager.CHANGE_MODE}{WorldManager.START_ADVENTURE}"

    def _load_delete_funct(self, objects, targets=None):
        # ensure targets is a list type
        if isinstance(targets, str) == True:
            targets = [targets]
            
        # delete only works if there are targets for load
        if len(objects) == 0:
            return "There are no files to delete."

        # delete file needs a target
        if targets == None:
            return "I need to know which file you'll be deleting...\nTry \"look\" to see which files I have saved."
        
        if targets[0] == Mode.ALL_OBJECTS:
            targets = []
            for save in self.config.saves.keys():
                targets.append(save)

        files_to_delete = []
        for target in targets:
            # remove spaces from file's name
            clean_name = ""
            for char in target:
                if char == " ":
                    clean_name += "-"
                else:
                    clean_name += char
            
            # validate target file exists
            if filemanager.locate_file(clean_name) == None:
                return f"There's no file here named \"{target}\". Try \"look\" to see which files I have saved."
            files_to_delete.append(clean_name)

            can_delete = textmanager.ask_yes_or_no("Are you sure you want to delete these files?", self.input_handler)

        if can_delete != None:
            return f"Understood."
            
        # delete save files, change save listing
        new_save_list = {}
        for file, data in self.config.saves.items():
            # add spaces to file's name
            clean_name = ""
            for char in file:
                if char == " ":
                    clean_name += "-"
                else:
                    clean_name += char
                
            if file in targets:
                # remove from mode
                self.current_mode.delete_object(file)

                # remove from disk
                filemanager.delete_file(clean_name)
            else:
                new_save_list[file] = data
            
        # return config saves to remaining objects
        self.config.saves = {}
        for file, data in new_save_list.items():
            self.config.saves[file] = data

        return "Files deleted..."

    def _init_load_menu(self):
        result = Mode("LOAD MENU\n => Look\n => Load\n => Delete\n => Back")
        result.add_command("load", self._load_game_funct, "Load one of the files saved to disk.")
        result.add_command("delete", self._load_delete_funct, "Delete one or more save files.")

        # add all files on disk as objects in this mode
        for file, data in self.config.saves.items():
            result.add_object(file, data)
        return result

    # ==== options menu functions ====

    def _option_set_funct(self, objects, targets=None):
        if targets == None or len(targets) == 0:
            return "I need to know what option you want to change."

        if len(targets) == 1:
            return "I need to know what value to change the option to."
            
        if len(targets) > 2 or targets[0] == Mode.ALL_OBJECTS:
            return "I can't change more than one setting at a time."
            
        # changing options to target value
        # options each have their own logic
        successful_change = self.config.change_value(targets[0], targets[1])

        if successful_change == False:
            return f"\n"
            
        # settings have been updated
        filemanager.write_data(filemanager.CURRENT_CONFIG, self.config)
            
        # clear the screen
        textmanager.display_text("Successfully set new option value.")
        self.command_queue.put(self.CLEAR_COMMAND)
        buffer = self.input_handler.get_input()
        textmanager.display_text(f"{self.current_mode.prompt}\n", True)
        textmanager.display_text(f"{textmanager.END_MARKER}\n{self.config}\n{textmanager.END_MARKER}", True) # prints out all options

        # send command to change speed if speed setting was changed
        if targets[0] == "delay":
            self.command_queue.put(f"{self.CHANGE_SPEED}{self.config.text_delay}")

        return f"\n"
        
    def _option_default_funct(self, objects, targets=None):
        if targets != None:
            return "The \"reset\" command only makes sense here without specifying targets."
            
        # restore settings from default
        can_reset = textmanager.ask_yes_or_no("Are you sure you want to restore settings to default?", self.input_handler)

        if can_reset != None:
            return "Understood."
            
        # delete current config file
        filemanager.delete_file(filemanager.CURRENT_CONFIG)

        # create new config object
        new_config = GameManager.Configuration()
            
        # keeping save
        new_config.saves = self.config.saves
            
        # add new config object
        filemanager.add_config(new_config)

        # set current settings to new object
        self.config = new_config

        # clear the screen
        textmanager.display_text("Restored settings to default.")
        self.command_queue.put(self.CLEAR_COMMAND)
        buffer = self.input_handler.get_input()
        textmanager.display_text(f"{self.current_mode.prompt}\n", True)
        textmanager.display_text(f"{textmanager.END_MARKER}\n{self.config}\n{textmanager.END_MARKER}", True) # prints out all options

        return "\n"
        
    def _option_wipe_funct(self, objects, targets=None):
        if targets != None:
            return "The \"wipe\" command only makes sense here without specifying targets."
            
        if self.last_signature != self.MAIN_MENU_MODE:
            return "You cannot \"wipe\" data without returning to main menu..."

        can_reset = textmanager.ask_yes_or_no("Are you sure you want to completely wipe save data?", self.input_handler)

        if can_reset != None:
            return "Understood."
            
        can_reset = textmanager.ask_yes_or_no("This will wipe options saved, as well as ALL saves! Are you sure?", self.input_handler)

        if can_reset != None:
            return "Understood."
            
        # delete all save files
        for file in self.config.saves.keys():
            # remove spaces from file's name
            clean_name = ""
            for char in file:
                if char == " ":
                    clean_name += "-"
                else:
                    clean_name += char
                    
            filemanager.delete_file(clean_name)
            
        # reset configuration, clearing acheivement data
        self.config = self.Configuration()

        textmanager.display_text("Wiping all saved options, and all save data...")
        self.command_queue.put(self.CLEAR_COMMAND)
        buffer = self.input_handler.get_input()

        # we need to reset the game to initial game running state
        return f"{Mode.CHANGE_MODE}{self.COMPLETE_BREAK}"

    def _init_option_menu(self):
        # add string representation of current values
        # WIPE not available in gameplay mode
        result_text = "OPTIONS\n => Set\n => Reset\n => Wipe\n => Back\n"

        result = Mode(result_text)
        result.add_command("set", self._option_set_funct, "Change a setting.")
        result.add_command("reset", self._option_default_funct, "Restore default settings.")
        result.add_command("wipe", self._option_wipe_funct, "Wipe all data from disk.")

        return result
        
    # ==== End Function Definitions ====

    # INIT MODES
    # used to initialize gamerunning modes for main menu
    def _init_modes(self):
        self.modes = {}
        self.modes[self.MAIN_MENU_MODE] = self._init_main_menu()
        self.modes[self.LOAD_MENU_MODE] = self._init_load_menu()
        self.modes[self.OPTION_MENU_MODE] = self._init_option_menu()

    # initialize game environment
    def __init__(self, input_handler, command_queue):
        # ensure package files are present
        if filemanager.validate_files() != 0:
            errormanager.log_error("Cannot validate dependencies")
            errormanager.close_program()

        # check for presence of CURRENT_CONFIG
        config_location = filemanager.locate_file(filemanager.CURRENT_CONFIG)
        self._is_first_open = config_location == None
        
        # create new config object if it's needed
        if self._is_first_open == True:
            new_config = GameManager.Configuration() # default options
            filemanager.add_config(new_config)

        # retrieve configuration options
        self.config = filemanager.read_data(filemanager.CURRENT_CONFIG, self.Configuration)

        # initialize stdin and window command variables
        self.input_handler = input_handler
        self.command_queue = command_queue

        # set up mode variables
        self.modes = {}
        self.current_mode = None
        self.last_mode = None
        
        self.current_signature = None
        self.last_signature = None

        # initialize modes
        self._init_modes()

        # create world
        self.world_state = WorldManager()
        
        # grab world manager's modes
        for key, value in self.world_state.modes.items():
            self.modes[key] = value

        self.game_running = False
    
    # run a session of game
    def run(self, skip_initial_buffer=False):
        # set the title
        self.command_queue.put(f"{self.CHANGE_TITLE}{self.MAIN_MENU_TITLE}")

        # initial buffer
        if skip_initial_buffer != True:
            buffer = textmanager.get_input(self.input_handler)

        # test for first open to display welcome to my game message
        if self._is_first_open == True:
            initial_text = "Welcome to the game. Initializing new setup...\n\n"
            initial_text += "This game is played using the keyboard. There are no clickable interfaces."
            initial_text += "\nYou, the player, can type commands into the entry bar at the bottom."
            initial_text += "\nI, the terminal, respond here in this log."
            initial_text += "\nSometimes the page ends, and when that happens just press enter to continue on the next page."
            initial_text += "\nFor instance, this \"page\" ends here, after this initial welcoming message."
            initial_text += "\nTo reset the game to a state where this initial message shows up again, use the \"wipe\" command in the options menu."
            textmanager.display_text(initial_text, True)
            self.command_queue.put(self.CLEAR_COMMAND)
            buffer = textmanager.get_input(self.input_handler)

            self._is_first_open = False

        # for game startup, display welcome message, explain how to play the game, and wait for buffer
        if self.config.display_welcome == True:
            welcome_message = "Welcome to Text Adventure!\nControls: type commands using a list of words.\n"
            welcome_message += "(To skip long chains of typing dialog like this, just hit enter while I'm still typing)\n"
            welcome_message += "The first word (the command word) tells me what command you want to use.\n"
            welcome_message += "You can then follow it up with as many noun words as you need.\n"
            welcome_message += "To see which commands are valid at any time use \"help\".\n"
            welcome_message += "To see which targets you can reference, use \"look\".\n"
            welcome_message += "To return to the previous menu use \"back\".\nYou can also target \"all\" for all targets.\n"
            welcome_message += "To exit the game, type \"quit\".\nTo keep this message from popping up on startup,"
            welcome_message += "set the \"welcome\" setting to \"no\".\n"
            textmanager.display_text(welcome_message, True)
            self.command_queue.put(self.CLEAR_COMMAND)
            buffer = textmanager.get_input(self.input_handler)

        self.current_mode = self.modes[self.MAIN_MENU_MODE]
        self.current_signature = self.MAIN_MENU_MODE
        self.last_mode = self.modes[self.MAIN_MENU_MODE]
        self.last_signature = self.MAIN_MENU_MODE

        # start game with main menu prompt
        textmanager.display_text(f"{self.current_mode.prompt}\n{textmanager.END_MARKER}", True)

        self.game_running = True

        # begin gameplay loop
        self.run_modes()

        # gameplay loop exits with QUIT and program falls out of execution here
    
    def run_modes(self):
        # gameplay loop continues running CURRENT_MODE commands until user exits game

        while(self.game_running == True):
            # get input
            if self.current_signature == self.OPTION_MENU_MODE:
                verb, nouns = textmanager.get_input(self.input_handler, False)
            else:
                verb, nouns = textmanager.get_input(self.input_handler)

            # input may have included invalid characters
            if verb == None:
                textmanager.display_text("You've entered invalid characters. I only take spaces and a-z.")
                continue

            # input command might not be a command
            if self.current_mode.is_command(verb) == False:
                textmanager.display_text(f"\"{verb}\" isn't a valid command.\nTry \"help\" for a list of commands.")
                continue

            # check for special command all as first noun: should be only noun
            if nouns != None and len(nouns) > 0:
                if nouns[0] == Mode.ALL_OBJECTS:
                    if len(nouns) > 1:
                        textmanager.display_text(f"\"{Mode.ALL_OBJECTS}\" should be the only listed target.")
                        continue
            
            # otherwise run the mode_return with verb-nouns
            mode_return = self.current_mode.run_command(verb, nouns)

            # if mode return executed NONE, command logic couldn't understand what was asserted
            if mode_return == None:
                result_text = f"I didn't quite understand \"{verb}"
                if nouns != None and len(nouns) != 0:
                    for noun in nouns:
                        result_text += f" {noun}"
                
                textmanager.display_text(f"{result_text}\"...\nTry typing \"help {verb}\" for help with that command.")
                continue

            # mode return can contain items in a list or dict with NONE value: which means target speicified doesn't exist
            invalid_noun = None
            if isinstance(mode_return, str) == False:
                # try list
                if isinstance(mode_return, list) == True:
                    if None in mode_return:
                        for noun in nouns:
                            if self.current_mode.is_valid(noun) == False:
                                invalid_noun = target
                                break
                # try dict
                if isinstance(mode_return, dict) == True:
                    for target, result in mode_return.items():
                        if result == None:
                            invalid_noun = target
                            break
            
            # test for invalid noun used
            if invalid_noun != None:
                textmanager.display_text(f"There is nothing like \"{invalid_noun}\" here.\nTry typing \"look\" to see what is around.")
                continue

            # check for specific commands which world can send gamemanager
            return_handled = self.handle_world_commands(mode_return)

            if return_handled == True:
                continue
            
            # check for mode return CHANGE_MODE
            return_handled = self.handle_change_mode(mode_return)

            if return_handled == True:
                continue
            
            # if there were no special command returns, print mode return and keep running
            if mode_return != "\n":
                textmanager.display_text(mode_return)
        
        # self.game_running was set to false: we are escaping gameplay
    
    # Handle World Commands
    # tests to see if WORLD_COMMAND command was used, and if so, handles it
    # returns False only if there was no WORLD_COMMAND item used
    def handle_world_commands(self, mode_return):
        # WORLD_COMMAND command not used if return is shorter
        if len(mode_return) <= len(WorldManager.GAME_COMMAND) + 1:
            return False
        
        # WORLD_COMMAND command not used if it isn't in the string
        if mode_return[:len(WorldManager.GAME_COMMAND)] != WorldManager.GAME_COMMAND:
            return False
        
        # WORLD_COMMAND command is followed up by some kind of command word
        command_string = mode_return[len(WorldManager.GAME_COMMAND):]

        # handle world command based on supported results
        if command_string == WorldManager.SAVE_SIGNATURE:
            # clean name
            clean_name = ""
            for char in self.world_state.user_name:
                if char == " ":
                    clean_name += "-"
                else:
                    clean_name += char
            
            world_data = self.world_state.get_world_data()

            # check to see if we are overwriting save data
            if filemanager.locate_file(clean_name) != None:
                can_overwrite = textmanager.ask_yes_or_no("Are you sure you want to overwrite save data?", self.input_handler)

                if can_overwrite != None:
                    textmanager.display_text("Understood.")
                    return True
                
                # we can overwrite
                filemanager.write_data(clean_name, world_data)
            else:
                # we must create a new save object with the data
                filemanager.add_save(clean_name, world_data)
            
            # now we must store our updated file summary
            self.saves[self.world_state.user_name] = self.world_state.get_summary()

            # and update this object as the one to continue
            self.config.most_recent_save = self.world_state.user_name

            # and finally overwrite configuration with new updates
            filemanager.write_data(filemanager.CURRENT_CONFIG, self.config)
            
            # if we are saving the game, after save operation we can just return
            textmanager.display_text("Game saved!")
            return True
        elif command_string == WorldManager.OPTION_SIGNATURE:
            # use gamemanager config options menu: back will return us to the game
            return self.handle_change_mode(f"{Mode.CHANGE_MODE}{self.OPTION_MENU_MODE}")
 
    # Handle Change Mode
    # tests to see if CHANGE_MODE command was used, and if so, handles it
    # returns False only if change_mode isn't used, else returns true
    def handle_change_mode(self, mode_return):
        # command not used if return is shorter
        if len(mode_return) <= len(Mode.CHANGE_MODE) + 1:
            return False
        
        # command not used CHANGE_MODE isn't in the string
        if mode_return[:len(Mode.CHANGE_MODE)] != Mode.CHANGE_MODE:
            return False
        
        mode_signature = mode_return[len(Mode.CHANGE_MODE):]
        
        # find associated new mode
        new_mode = None
        new_signature = None

        # look for exact matches
        if mode_signature == Mode.QUIT_SIGNATURE:
            # from the main menu (or its submenus) we can just exit the game
            can_quit = None
            if self.current_signature != self.MAIN_MENU_MODE and self.last_signature != self.MAIN_MENU_MODE:
                can_quit = textmanager.ask_yes_or_no("Are you sure you want to quit? You will lose any unsaved progress.", self.input_handler)

            if can_quit!=None:
                textmanager.display_text("Understood.")
                return True
            else:
                if self.current_signature == self.MAIN_MENU_MODE or self.last_signature == self.MAIN_MENU_MODE:
                    textmanager.display_text("Goodbye!")
                    self.game_running = False
                    return True # return to desktop
                else:
                    # return to main menu
                    return self.handle_change_mode(f"{Mode.CHANGE_MODE}{self.MAIN_MENU_MODE}") # recur with MAIN MENU MODE
        elif mode_signature == self.COMPLETE_BREAK:
            # used to escape gameloop and start game from initial bootup conditions : USED ONLY IN WIPE SAVE MECHANIC

            # delete config file
            filemanager.delete_file(filemanager.CURRENT_CONFIG)

            # initialize a new version of game manager
            self.__class__.__init__(self, self.input_handler, self.command_queue)

            # call run again
            self.run(True)

            # finally, once inner loop escapes from previous self.run, escape fully from here too
            self.game_running = False
            return True
        elif mode_signature == Mode.BACK_SIGNATURE:
            # cannot go back from MAIN MENU
            if self.current_signature == self.MAIN_MENU_MODE:
                textmanager.display_text("You can't go \"back\" any further than the main menu!")
                return True
            
            # back is invalid if last_signature is ever set to None
            if self.last_signature == None or self.last_mode == None:
                textmanager.display_text("You cannot go \"back\" when there's nowhere to go back to!")
                return True
            
            # else use whatever the last mode was
            new_mode = self.last_mode
            new_signature = self.last_signature
        elif mode_signature == GameManager.START_ADVENTURE:
            # beginning a new adventure using whatever world has been loaded
            textmanager.display_text(f"Starting adventure!!!")

            # grab the mode we are supposed to use and change to that
            new_mode = self.world_state.get_initial_mode()
            for key, value in self.world_state.modes.items():
                if new_mode == value:
                    new_signature = key
                    break
        else:
            for key_string, mode in self.modes.items():
                if mode_signature == key_string:
                    new_mode = mode
                    new_signature = key_string
                    break
        
        # if CHANGE_MODE is not a mode, something returned it incorrectly
        if new_mode == None:
            textmanager.display_text(f"There is no such page \"{mode_signature}\".")
            return True
        
        # if main menu is new mode change title, in case we quit a game
        if new_mode == self.MAIN_MENU_MODE:
            self.command_queue.put(f"{self.CHANGE_TITLE}{self.MAIN_MENU_TITLE}")
        
        # change to new mode
        self.last_mode = self.current_mode
        self.last_signature = self.current_signature
        self.current_mode = new_mode
        self.current_signature = new_signature

        textmanager.display_text("Changing page...")
        self.command_queue.put(self.CLEAR_COMMAND) # send clear command to controlling window which waits on input buffer
        buffer = textmanager.get_input(self.input_handler) # hold execution here to buffer the terminal for screen clear
        if mode_signature == self.START_ADVENTURE:
            # disable the 'back' command
            self.last_mode = None
            self.last_signature = None
            # grab the location we are supposed to be in to change title
            self.command_queue.put(f"{self.CHANGE_TITLE}{self.world_state.get_location_title()}")
            
        textmanager.display_text(f"{self.current_mode.prompt}\n{textmanager.END_MARKER}", True)

        if self.current_signature == self.OPTION_MENU_MODE:
            # need to also print out the actual options menu after the prompt
            textmanager.display_text(f"\n{self.config}\n{textmanager.END_MARKER}", True)

        return True
