# Text Adventure
# 05-27-24
# Brian Morris

import errormanager

CHANGE_MODE = "change mode to new command structure with signiture: "
QUIT_SIGNITURE = "quit"
BACK_SIGNITURE = "back"

# Mode
# Encapsulates a mode of operation
# in which the user interacts with Text Adventure
class Mode():
    # Function Signiture
    # a bundle of information needed to use a function stored
    class FunctionSigniture():
        def __init__(self, funct, minargs, hint_text):
            self.funct = funct
            self.minargs = minargs
            self.hint_text = hint_text
    
    # Object Details
    # a bundle of information needed to reference game objects
    class ObjectDetails():
        def __init__(self, key_string, description, hint_text):
            self.key_string = key_string
            self.description = description
            self.hint_text = hint_text
    
    # all modes have HELP, LOOK, BACK, and QUIT commands
    def _back_funct(self, targets=None):
        return f"{CHANGE_MODE}{BACK_SIGNITURE}"
    def _quit_funct(self, targets=None):
        return f"{CHANGE_MODE}{QUIT_SIGNITURE}"
    def _look_funct(self, targets=None):
        if targets:
            # targets should be any number of objects in the current mode
            result = {}
            for target in targets:
                for object_detail in self.objects:
                    if target == object_detail.key_string:
                        result[target] = object_detail.description
            for target in targets:
                if target not in result:
                    result[target] = None
            return result
        else:
            # if no targets were specified, we should return a list of all valid objects
            if len(result) == 0:
                result = []
                for object_detail in self.objects:
                    result.append(object_detail.key_string)
            return result
    def _help_funct(self, targets=None):
        # targets should be any object or function
        # any non-matching targets are None
        result = {}
        for target in targets:
            for object_detail in self.objects:
                if target == object_detail.key_string:
                    result[target] = object_detail.hint_text
                    continue
            for function_sig, verbs in self.command_dict.items():
                if target in verbs:
                    result[target] = function_sig.hint_text
                    continue
        for target in targets:
            if target not in result:
                result[target] = None
        return result

    # define mode
    def __init__(self, signiture):
        self.signiture = signiture
        self.command_dict = {}
        self.objects = []
        # all modes have HELP, LOOK, BACK, and QUIT
        back_funct = FunctionSigniture(_back_funct, 0, "used to go back to the previous menu")
        self.command_dict[back_funct] = [ "back", "return" ]
        quit_funct = FunctionSigniture(_quit_funct, 0, "used to exit the game to main menu or desktop")
        self.command_dict[quit_funct] = [ "quit" ]
        help_funct = FunctionSigniture(_help_funct, 0, "used to get a hint about anything")
        self.command_dict[help_funct] = [ "help", "hint" ]
        look_funct = FunctionSigniture(_look_funct, 0, "used to see more details about your environment")
        self.command_dict[look_funct] = [ "look", "list" ]
    
    # Add Object
    # adds a new valid object target
    # mutates object if already in self.objects
    def add_object(self, key_string, description, hint_text):
        # check if object already exists
        for item in self.objects:
            if item.key_string == key_string:
                item.description = description
                item.hint_text = hint_text
                return
        new_object = ObjectDetails(key_string, description, hint_text)
        self.objects.append(new_object)
    
    # Clear Objects
    # removes all objects from Mode
    def clear_objects(self):
        self.objects = []
    
    # Add Function
    # adds a new function to mode's command dictionary
    def add_function(self, funct, minargs, hint_text, verb_list):
        new_sig = FunctionSigniture(funct, minargs, hint_text)
        self.command_dict[new_sig] = verb_list
    
    # Run Command
    # runs a command stored in command_dict if it can
    # returns None if command could not be ran, otherwise returns result
    def run_command(self, verb, noun_list=None):
        # look for a matching command
        command_to_run = None

        for function_sig, verb_list in self.command_dict.items():
            if verb in verb_list:
                command_to_run = function_sig
        
        if command_to_run == None:
            return None
        
        command_to_run = command_to_run.funct
        
        # if no nouns were specified, return function result with no args
        if noun_list == None:
            if command_to_run.minargs != 0:
                return None
            return self.command_to_run()

        # validate noun_list can be given to command
        valid_noun_count

        for object_detail in self.objects:
            if object_detail.key_string in noun_list:
                valid_noun_count += 1

        if valid_noun_count < command_to_run.minargs:
            return None
        
        # try to run command
        try:
            # if nouns are invalid, we still want to use them
            # ensure noun_list is list type
            if isinstance(noun_list, str):
                noun_list = [noun_list]
            return self.command_to_run(noun_list)
        except Exception as e:
            # command could still not execute
            errormanager.log_error(e)
            return None
        