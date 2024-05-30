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

DEFAULT_LINE_WIDTH = 15

# Text Manager
# Performs operations on strings
# Handles console i/o

# Display Text
# used to communicate information to the user in a common format
# animated with a delay
def display_text(text, text_delay=0, line_width=DEFAULT_LINE_WIDTH):
    text_lines = None
    if isinstance(text, list):
        text_lines = []
        new_length = len(text)
        current_index = 0

        # take out all line_width lines
        while new_length - line_width > line_width:
            line = ""
            for i in range(line_width):
                line += f"{text[current_index + i]}, "
            text_lines.append(line)
            current_index += line_width
            new_length -= line_width
        
        # cut the rest in half
        if new_length % line_width != 0:
            new_length = new_length // 2
            if new_length % 2 != 0:
                new_length += 1
            # take that amount out
            line = ""
            for i in range(new_length + 1):
                line += f"{text[current_index + i]}, "
            text_lines.append(line)
            current_index += new_length + 1
        
        # add the rest
        line = ""
        for i in range(len(text) - current_index):
            line += f"{text[current_index + i]}, "
        text_lines.append(line[:-2])
    elif isinstance(text, dict):
        # break up display by key : value
        text_lines = []
        for key, line in text.items():
            text_lines.append(f"{key}: {line}")
    elif isinstance(text, str):
        # break up display by newline characters
        text_lines = text.split('\n')
    else:
        # text is not string, list, or dict
        text_lines = [text]

    # print start of new terminal line
    if text_delay != 0:
        print(TERMINAL_TAG, end='', file=sys.stdout)
    
    if text_delay > MAX_DELAY:
        text_delay = MAX_DELAY

    for line in text_lines:
        # print instantaneously with delay == 0
        if text_delay == 0:
            print(f"{TERMINAL_TAG}{line}", file=sys.stdout)
        else:
            # delay between print operations
            for letter in line:
                time.sleep(text_delay / 5)
                print(letter, end='', flush=True, file=sys.stdout)
            # end line
            time.sleep(text_delay * 5)
            print('', end='\n', flush=True, file=sys.stdout)
            if line != text_lines[len(text_lines) - 1]:
                print(TERMINAL_TAG, end='', flush=True, file=sys.stdout)

# Get Input
# ensures user input is of valid type: words with characters a-z seperated by spaces
# returns None, None if invalid values are used, or verb, noun if they are valid
def get_input():
    # get arg_string from user
    arg_string = input(f"{PLAYER_TAG}")

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
            return None, None
    
    # strip ends of spaces
    if len(result) != 0:
        result = result.lstrip(' ')
    if len(result) != 0:
        result = result.rstrip(' ')
        
    # test for missing result
    if len(result) == 0:
        return None, None
        
    # whatever is left is a clean user input string
    # split based on spaces
    words = result.split(' ')
    if len(words) == 0:
        return None, None
    
    # verb is first word, nouns are the other words
    nouns = None
    verb = words[0]
    if len(words) > 1:
        nouns = words[1:]

    return verb, nouns

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