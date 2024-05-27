# Text Adventure
# 05-27-24
# Brian Morris

import time
import sys

ALPHABET = {
    'A' : 'a', 'B' : 'b', 'C' : 'c', 'D' : 'd', 'E' : 'e',
    'F' : 'f', 'G' : 'g', 'H' : 'h', 'I' : 'i', 'J' : 'j',
    'K' : 'k', 'L' : 'l', 'M' : 'm', 'N' : 'n', 'O' : 'o',
    'P' : 'p', 'Q' : 'q', 'R' : 'r', 'S' : 's', 'T' : 't',
    'U' : 'u', 'V' : 'v', 'W' : 'w', 'X' : 'x', 'Y' : 'y', 'Z' : 'z' }

TERMINAL_TAG = "  *"
PLAYER_TAG = " > "

MAX_DELAY = .5
SLOW_TEXT = .3
NORMAL_TEXT = .15
QUICK_TEXT = .05

# Text Manager
# Performs operations on strings
# Handles console i/o

# Display Text
# used to communicate information to the user in a common format
# animated with text_speed
def display_text(text, text_speed=0):
    # break up display by newline characters
    text_lines = text.split('\n')

    # print start of new terminal line
    if text_speed != 0:
        print(TERMINAL_TAG, end='')
    
    if text_speed > MAX_DELAY:
        text_speed = MAX_DELAY

    for line in text_lines:
        # print instantaneously with speed == 0
        if text_speed == 0:
            print(f"{TERMINAL_TAG}{line}")
        else:
            # delay between print operations
            for letter in line:
                time.sleep(text_speed / 5)
                print(letter, end='', flush=True)
            # end line
            time.sleep(text_speed * 5)
            print('', end='\n', flush=True)
            if line != text_lines[len(text_lines) - 1]:
                print(TERMINAL_TAG, end='', flush=True)

# Get Input
# ensures user input is of valid type: words with characters a-z seperated by spaces
# returns None if invalid values are used
def get_input():
    # get arg_string from user
    arg_string = input(f"\n{PLAYER_TAG}", file=sys.stdin)

    result = ""
    # skip multiple spaces in a row
    space_found = False

    for character in arg_string:
        # skip all multiple spaces in a row
        if space_found == True:
            if character == ' ':
                continue
            else:
                space_found = False
            
        if character >= 'a' and character <= 'z':
            # a-z are valid input
            result += character
        elif character >= 'A' and character <= 'Z':
            # A-Z need to become a-z
            result += to_lower(character)
        elif character == ' ':
            # first of potentially many spaces
            result += ' '
            space_found = True
        else:
            # invalid character returned
            return None
        
    # strip ends of spaces
    if len(result) != 0:
        result = result.lstrip(' ')
    if len(result) != 0:
        result = result.rstrip(' ')
        
    # test for missing result
    if len(result) == 0:
        return None
        
    # whatever is left is a clean user input string
    return result

# To Lower
# Safely reduces A-Z to lower case
# returns unmodified if not A-Z
def to_lower(arg_string):
    # perform recursive operation on objects of size > 1
    if len(arg_string) != 1:
        new_lower_input = ""
        for character in arg_string:
            new_lower_input += to_lower(character)
        return new_lower_input
        
    # perform whichever operation is needed
    for capital, lower_case in ALPHABET.items():
        if arg_string == capital:
            return lower_case
    
    # return unmodified value if no valid result was found
    return arg_string