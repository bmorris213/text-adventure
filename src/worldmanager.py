# Text Adventure
# 06-10-2024
# Brian Morris

from mode import Mode

# World Manager
# handles interactions with an instance of world
# delegates to party manager and encounter manager as needed
class WorldManager():
    # mode returns that translate to gamemanager actions
    GAME_COMMAND = "use command:"
    SAVE_SIGNATURE = "save world data"
    OPTION_SIGNATURE = "return to the options submenu" # recycle gamemanager options

    # WORLD class data struct stores all information about the world
    class World():
        def __init__(self):
            # create the default world and fill it with the default objects
            self.cow_push_count = 0
            self.box_secret = "A magical potato!"
            self.enemy_reaction = "Ow..."
            self.enemy_hp = 4

            self.containers = ["box"]
            self.pushables = ["cow"]
            self.enemies = ["troll"]
            self.location = "A New Journey"
    
    def _save_funct(self, objects, targets=None):
        return f"{Mode.GAME_COMMAND}{SAVE_SIGNATURE}"

    def _option_funct(self, objects, targets=None):
        return f"{Mode.GAME_COMMAND}{OPTION_SIGNATURE}"
    
    def _do_stuff_funct(self, objects, targets=None):
        if targets:
            if Mode.ALL_OBJECTS in self.targets:
                return f"You go and \"use\" absolutely everything in your sight. Good job?"

            resulting_action = ""

            for key_string in objects.keys():
                if key_string in targets and key_string != Mode.ALL_OBJECTS:
                    resulting_action += f"Nice work, {self.user_name}, you really used that \"{key_string}\"...\n"
            
            if resulting_action == "":
                resulting_action = f"What use is that ol \"{targets[0]}\" anyway?\n"
            
            return f"{resulting_action}Maybe try something else?"
        else:
            return f"Nice work, {self.user_name}, you do stuff real good."
    
    def _open_funct(self, objects, targets=None):
        if targets:
            if len(targets) > 1 or Mode.ALL_OBJECTS in targets:
                return f"You can only open 1 thing at a time!"

            if target[0] not in objects.keys():
                return f"There is no \"{target[0]}\" here to open..."

            if target[0] not in self.world.containers:
                return f"You can't open \"{target[0]}\", but nice try..."

            return f"Inside of \"{target[0]}\" there is..... {self.world.box_secret}"
        else:
            return "You need to specify what you're trying to open..."
    
    def _attack_funct(self, objects, targets=None):
        if targets:
            for target in targets:
                if target not in objects.keys():
                    return f"There is no \"{target}\" here to attack..."
            
            if Mode.ALL_OBJECTS in targets:
                return f"You fight the whole world and lose.\nEventually you get up and can try again."

            result = ""
            for target in targets:
                if target not in self.world.enemies:
                    result += f"You hit \"{target}\" with all your might...\n"
                else:
                    self.world.enemy_hp -= 1
                    if self.world.enemy_hp < 0:
                        result += f"\"{target}\" is already dead... Your cruelty knows no bounds.\n"
                    elif self.world.enemy_hp == 0:
                        result += f"\"{target}\" succumbs to your incredible violence. Congradulations, you win!\nYou can \"quit\" now, proud of your accomplishments.\n"
                    else:
                        result += f"\"{target}\" cries out in pain...\n\"{self.enemy_reaction}\", they say.\n"

            return f"{result}With combat accomplished, what will you do next?"
        else:
            return "You need to specify what you're trying to attack..."
    
    def _push_funct(self, objects, targets=None):
        if targets:
            if len(targets) > 1 or Mode.ALL_OBJECTS in targets:
                return "You can only \"push\" one thing at a time..."
            
            if targets[0] not in objects.keys():
                return f"There is no \"{targets[0]}\" here to push..."
            
            if targets[0] not in self.world.pushables:
                return f"You shove \"{targets[0]}\" with all your might, but to no avail..."
            
            if targets[0] == "cow":
                self.world.cow_push_count += 1
                if self.world.cow_push_count >= 5:
                    return f"You've already rolled over the cow.\nWhat more are you trying to accomplish???"
                elif self.world.cow_push_count == 5:
                    return f"You push the cow again and again until eventually... it rolls over! Achievement unlocked!"
                elif self.world.cow_push_count == 1:
                    return f"You... push the cow. Congradulations."
                else:
                    return f"Again you push the cow. You seem to be... making some progress?"
        else:
            return "You need to specify what you're trying to push..."

    def _init_only_mode(self):
        result = Mode("Welcome to the WORLD!! Look at all this awesome game that's definitely everywhere!")
        result.add_command("save", self._save_funct, "Save the data you manipulated.")
        result.add_command("options", self._option_funct, "Pause and mess with settings.")
        result.add_command("use", self._do_stuff_funct, "Do fun game things with the stuff that's here. This is a game. I swear.")
        result.add_command("open", self._open_funct, "Opens a container, if it is... a container...")
        result.add_command("attack", self._attack_funct, "Hit a thing by flailing your fists!")
        result.add_command("push", self._push_funct, "Does something... or DOES IT?!!!")

        result.add_object("cow", "It's a... cow!", "Rolls over if you push it enough.")
        result.add_object("box", "An unassuming box.", "Contains a mystery! OR DOES IT?!!")
        result.add_object("troll", "Enemy spotted!", "Attack it, dummy!")

        return result

    # initializes world state with default world variables
    def __init__(self):
        # initialize modes
        self.modes = {}
        self.user_name = None
        self.world = self.World()
        
        # initialize modes
        self.modes = {}
        self.modes["only"] = self._init_only_mode()
    
    # name the player
    def name(self, user_name):
        self.user_name = user_name
    
    # load in world data
    def load(self, data):
        self.world = data

    # load in a string representing the location of the player
    def get_location_title(self):
        return self.world.location
    
    # get the mode in which the player is currently playing on gameplay startup
    def get_initial_mode(self):
        return self.modes["only"]
    
    # get a small readable summary blip about save file status
    def get_summary(self):
        return f"Player {self.user_name} is... doing things..."
    
    # return all data relavant for save/load operations
    def get_world_data(self):
        return self.world