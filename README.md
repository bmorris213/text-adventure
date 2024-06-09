# text-adventure
## A glorious text-adventure style rpg engine

This package is a text adventure rpg game engine. It isn't really a game, although it contains the shell of a game inside of it for demonstration purposes.
To run the basic shell game, just double click main.bat for windows, or main.sh for linux/mac os.
To make your own options menu, change the definition of the Configuration class within the src/main.py to set up your own options menu!
To make your own game, change the definition of the World class within the src/worldmanager.py to define what makes up the world of your game, and then change the definition of the self.modes section of the code

### What is a mode?

A 'Mode' in the context of this text adventure game is a mode of operation within the game. In each mode we define a list of commands based on 1: the word players need to type to use that command and 2: the internal function that command performs on the world. Each mode also stores the list of targets that those commands can be used on. Notice this list is seperate from the ingame state of World class, so managing both is important.

When you define a new 'Mode' of operation for your game, you define the rules for how the player can interact with your World. I've written a few modes to show you about how they should work, but to create your own game, check out src/mode.py to see how they internally work, and src/gamemanager.py has a function "run_mode" which loops infinitely, accepting input and handling taking action based on the current mode.

The 'filemanager.py' handles internal files, the 'errormanager.py' handles when exceptions are thrown, and the 'textmanager.py' handles parsing user input and displaying resulting text. The 'displaymanager.py' file handles the display window that pops up.

To change the 'look' and 'feel' of the game, change the self.game_themes section of the 'displaymanager.py'. The code defines a basic window class, and a GameWindow class that inherets specific behavior from it.

## So what now?

If you've had fun playing my little dummy game, take this code and extend it to your own purposes! Maybe you can write a really fun text adventure game using the framework I've set up!