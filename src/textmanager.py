# Text Adventure
# 06-10-2024
# Brian Morris

import sys

ALPHABET = {
    'A' : 'a', 'B' : 'b', 'C' : 'c', 'D' : 'd', 'E' : 'e',
    'F' : 'f', 'G' : 'g', 'H' : 'h', 'I' : 'i', 'J' : 'j',
    'K' : 'k', 'L' : 'l', 'M' : 'm', 'N' : 'n', 'O' : 'o',
    'P' : 'p', 'Q' : 'q', 'R' : 'r', 'S' : 's', 'T' : 't',
    'U' : 'u', 'V' : 'v', 'W' : 'w', 'X' : 'x', 'Y' : 'y', 'Z' : 'z' }

TERMINAL_TAG = "      // "
PLAYER_TAG = " > "
END_MARKER = "-------------------"

DEFAULT_LINE_WIDTH = 9

MAX_NAME_LENGTH = 15

# Text Manager
# Performs operations on strings
# Handles console i/o

# Ask Yes or No
# designed to prompt user with a yes or no question
# and only accept 'yes' or 'no' answers
# returning None if 'yes', 'no' if 'no', and 'quit' if 'quit' or 'back' or 'stop' are used
def ask_yes_or_no(question, input_handler=None):
    display_text(question)
    display_text("(Type \"quit\", \"back\", or \"stop\" to stop)")

    while(True):
        user_input = None
        if input_handler == None:
            user_input = input(f"{PLAYER_TAG}")
        else:
            user_input = input_handler.get_input()

        user_input = to_lower(user_input)

        if user_input == "yes" or user_input == "y":
            return None
        elif user_input == "no" or user_input == "n":
            return "no"
        elif user_input == "back" or user_input == "quit" or user_input == "stop":
            return "quit"
        else:
            display_text("Only \"yes\" or \"no\" answers accepted.")

# Display Text
# used to communicate information to the user in a common format
# animated with a delay
def display_text(text, strip_tags=False, line_width=DEFAULT_LINE_WIDTH):
    text_lines = None
    if isinstance(text, list):
        text_lines = []
        new_length = len(text)
        current_index = 0

        # just simply use anything less than line width
        if new_length < line_width:
            new_line = ""
            for i in range(new_length):
                new_line += f"{text[i]}, "
            text_lines.append(new_line[:-2])
        else:
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

    result = ""
    if strip_tags == False:
        for line in text_lines:
            result += f"{TERMINAL_TAG}{line}\n"
    else:
        for line in text_lines:
            result += f"{line}\n"

    print(result, file=sys.stdout, flush=True, end="")

# Get Input
# ensures user input is of valid type: words with characters a-z seperated by spaces
# returns None, None if invalid values are used, or verb, noun if they are valid
def get_input(input_handler=None, validate_chars=True):
    # get arg_string from user
    if input_handler==None:
        arg_string = input(f"{PLAYER_TAG}")
    else:
        arg_string = input_handler.get_input()

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
        
        if validate_chars == False:
            result += character
            if character == ' ':
                space_found = True
            continue

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

# Clean Name
# safely limits name length and invalid character use
# returns None if name contains invalid characters
def clean_name(name_string):
    result = ""
    if name_string == None or len(name_string) == 0:
        return None
    
    name_string = name_string.rstrip(' ')
    name_string = name_string.lstrip(' ')

    if name_string == None or len(name_string) == 0:
        return None

    # skip multiple spaces in a row
    space_found = False

    for character in name_string:
        # skip all multiple spaces in a row
        if space_found == True:
            if character == ' ':
                continue
            else:
                space_found = False
            
        if character >= 'a' and character <= 'z':
            result += character
        elif character >= 'A' and character <= 'Z':
            result += to_lower(character)
        elif character == ' ':
            if result == "":
                continue # skip all spaces at beginning

            # first of potentially many spaces: files use ' '
            result += ' '
            space_found = True
        else:
            # invalid character returned
            return None
    
        if len(result) >= MAX_NAME_LENGTH:
            break
    
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