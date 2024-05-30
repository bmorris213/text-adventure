# Text Adventure
# 05-30-24
# Brian Morris

import os
import sys
import time

import errormanager
import filemanager
import textmanager
import displaymanager
import partymanager
import worldmanager
import encountermanager
from mode import Mode

# Game Manager
# Stores and Mutates all game states
# Handles all program delegation
class GameManager():
    # initialize game environment
    def __init__(self):
        # initialize configuration options
        self.text_delay = 0
        print("not implemented")
    
    # run a session of game
    def run(self):
        print("not implemented")