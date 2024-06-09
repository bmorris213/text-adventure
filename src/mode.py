# Text Adventure
# 06-10-2024
# Brian Morris

# Mode
# Encapsulates a mode of operation
# in which the user interacts with Text Adventure
class Mode():
    # default signatures
    CHANGE_MODE = "change mode to new command structure with signature: "
    QUIT_SIGNATURE = "quit"
    BACK_SIGNATURE = "back"

    ALL_OBJECTS = "all"

    # built in commands
    HELP_COMMAND = "help"
    QUIT_COMMAND = "quit"
    LOOK_COMMAND = "look"
    BACK_COMMAND = "back"
    RESERVE_WORDS = [ HELP_COMMAND, QUIT_COMMAND, LOOK_COMMAND, BACK_COMMAND ]

    # all modes have HELP, LOOK, BACK, and QUIT commands
    def _back_funct(self, targets=None):
        return f"{self.CHANGE_MODE}{self.BACK_SIGNATURE}"
    
    def _quit_funct(self, targets=None):
        return f"{self.CHANGE_MODE}{self.QUIT_SIGNATURE}"
    
    def _look_funct(self, targets=None):
        if targets:
            if targets[0] == self.ALL_OBJECTS and len(self.__objects.keys()) == 1:
                return "There is nothing here..."

            results = {}
            # find references in objects
            for key_string in self.__objects.keys():
                if (key_string in targets or targets[0] == self.ALL_OBJECTS) and key_string != self.ALL_OBJECTS:
                    results[key_string] = self.__objects[key_string]
            
            # any non-matching targets should be None
            for target in targets:
                if target not in results.keys() and targets[0] != self.ALL_OBJECTS:
                    results[target] = None
            
            return results
        else:
            # if no targets were specified, we should return a list of all objects
            results = []
            if len(self.__objects.keys()) == 1: # there will always be a dummy "all" object
                return "There is nothing here..."
            for key_string in self.__objects.keys():
                if key_string != self.ALL_OBJECTS:
                    results.append(key_string)
            return results

    def _help_funct(self, targets=None):
        if targets:
            results = {}
            # find references in objects and commands
            for key_string in self.__objects.keys():
                if (key_string in targets or targets[0] == self.ALL_OBJECTS) and key_string != self.ALL_OBJECTS:
                    hint_text = self.__hints[key_string]
                    if hint_text != None:
                        results[key_string] = hint_text
            for key_string in self.__commands.keys():
                if (key_string in targets or targets[0] == self.ALL_OBJECTS) and key_string != self.ALL_OBJECTS:
                    hint_text = self.__hints[key_string]
                    if hint_text != None:
                        results[key_string] = hint_text
            
            # any non-matching targets should be None
            # as well as any objects which have no hint text
            for target in targets:
                if target not in results.keys() and targets[0] != self.ALL_OBJECTS:
                    results[target] = None
            
            return results
        else:
            # if no targets were specified, we should return a list of all commands
            results = []
            for key_string in self.__commands.keys():
                results.append(key_string)
            return results

    # define mode
    def __init__(self, prompt):
        self.prompt = prompt
        self.__commands = {}
        self.__hints = {}
        self.__objects = {}
        # all modes have HELP, LOOK, BACK, and QUIT
        self.add_command(self.HELP_COMMAND, self._help_funct,
            "List commands, or get a hint on any object or command.")
        self.add_command(self.LOOK_COMMAND, self._look_funct,
            "List objects, or get some details on any object.")
        self.add_command(self.BACK_COMMAND, self._back_funct,
            "Return to previous menu, or close menu.")
        self.add_command(self.QUIT_COMMAND, self._quit_funct,
            "Quit to main menu or desktop.")
        self.add_object(self.ALL_OBJECTS, "Every target that you can possibly command.", "Easy shortcut for targetting everything.")
    
    # Add Object
    # adds a new valid object target
    # mutates object if already exists
    def add_object(self, key_string, description, hint_text=None):
        self.__objects[key_string] = description
        self.__hints[key_string] = hint_text
    
    # Delete Object
    # remove an object from the dictionary
    def delete_object(self, key_string):
        if key_string in self.__objects.keys():
            del self.__objects[key_string]
    
    # Clear Objects
    # remove all objects from the dictionary
    def clear_objects(self):
        self.__objects = {}
    
    # Add Function
    # adds a new function to mode's command dictionary
    # mutates function if it already exists
    def add_command(self, key_string, funct, hint_text=None):
        self.__commands[key_string] = funct
        self.__hints[key_string] = hint_text

    def is_command(self, verb):
        return verb in self.__commands.keys()

    def is_valid(self, noun):
        return noun in self.__objects.keys()
    
    # Run Command
    # runs a command stored in command_dict if it can
    # returns None if command could not be ran, otherwise returns result
    def run_command(self, verb, noun_list=None):
        # look for a matching command
        if verb not in self.__commands.keys():
            return None
        
        # if using reserved command, return function result called on self
        if verb in self.RESERVE_WORDS:
            return self.__commands[verb](noun_list)
        
        # pass control to a custom command
        return self.__commands[verb](self.__objects, noun_list)
        