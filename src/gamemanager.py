# Text Adventure
# 05-27-24
# Brian Morris

import os
import sys
import time

import errormanager
import filemanager
import textmanager
from mode import Mode

# Game Manager
# Stores and Mutates all game states
# Handles all program delegation
class GameManager():
    # initialize game environment
    def __init__(self):
        # initialize configuration options
        self.text_delay = 0
    
    
    # run a session of game
    def run(self):
        text_list = [ "item 1", "item 2" ]
        for i in range(textmanager.DEFAULT_LINE_WIDTH * 3):
            text_list.append(f"item {i + 3}")
        textmanager.display_text(text_list)