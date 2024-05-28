# Text Adventure
# 05-27-24
# Brian Morris

import os
import pickle

# initialize paths
PROJECT_ROOT = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)), os.pardir))
DATA_PATH = "data"
SAVES_PATH = "saves"
SOURCE_PATH = "src" # path is ignored when modifying files, and added to file_dependencies
TEST_PATH = "test"
CACHE = "__pycache__"

# initialize file names
DEFAULT_SAVE = "world.data"
DEFAULT_CONFIG = "default.config"
MAIN_SHELL = "main.sh"
TEST_SHELL = "test.sh"
FILE_DEPENDENCIES = [ DEFAULT_SAVE, DEFAULT_CONFIG, MAIN_SHELL, TEST_SHELL ]
CURRENT_CONFIG = "current.config"
ERROR_LOG = "error.log"

# File Manager
# handles all file i/o operations
# ensures file validity, and no duplicate files exist

# Validate Files
# ensures a list of files mandetory for program function do exist
# returns a 1 if they don't, and a 0 if they do
def validate_files():
    # add file dependencies
    files_to_validate = []
    files_to_validate.append(os.path.join(PROJECT_ROOT, MAIN_SHELL))
    files_to_validate.append(os.path.join(PROJECT_ROOT, TEST_SHELL))
    files_to_validate.append(os.path.join(PROJECT_ROOT, DATA_PATH, DEFAULT_CONFIG))
    files_to_validate.append(os.path.join(PROJECT_ROOT, DATA_PATH, DEFAULT_SAVE))

    # add project source files
    project_files = [ "main.py", "mode.py", "gamemanager.py",
        "errormanager.py", "filemanager.py", "textmanager.py",
        "worldmanager.py", "partymanager.py", "encountermanager.py" ]
    for file in project_files:
        files_to_validate.append(os.path.join(PROJECT_ROOT, SOURCE_PATH, file))

    # validate files exist
    for file in files_to_validate:
        if os.path.exists(file):
            if os.path.isfile(file):
                continue
        return 1
    
    return 0

# Add Log
# used to append a new error log to the report file
# if the error log file does not exist, make it
def add_log(error_report):
    found_path = locate_file(ERROR_LOG)

    if found_path == None:
        found_path = os.path.join(PROJECT_ROOT, SOURCE_PATH, ERROR_LOG)
        # create empty error log file
        with open(found_path, 'wb') as f:
            pass
    
    # append log
    with open(found_path, 'ab') as f:
        pickle.dump(error_report, f)

# Add Save
# adds a new file to the saves folder using world.data
# returns a 1 if that save already exists, and 0 if save creation was successful
def add_save(file_name):
    found_path = locate_file(file_name)

    if found_path != None:
        return 1 # save already exists
    
    # build a new file in the saves folder in data
    found_path = os.path.join(PROJECT_ROOT, DATA_PATH, SAVES_PATH, file_name)
    default_world = read_data(DEFAULT_SAVE)
    
    with open(found_path, 'wb') as file:
        for item in default_world:
            pickle.dump(item, file)

    return 0

# Add Config
# ensures a new current.config file is made in the data folder
# returns 1 if there is already a config file, and 0 if file was added
def add_config():
    found_path = locate_file(CURRENT_CONFIG)

    if found_path != None:
        return 1 # config already exists

    # build a new config using default config
    found_path = os.path.join(PROJECT_ROOT, DATA_PATH, CURRENT_CONFIG)
    default_configuration = read_data(DEFAULT_CONFIG)

    with open(found_path, 'wb') as file:
        for item in default_configuration:
            pickle.dump(item, file)
    
    return 0

# Delete File
# if the given file name refers to a mutatable project file, delete it
# returns 1 if you cannot perform deletion, returns 0 if successful
def delete_file(file_name):
    found_path = locate_file(file_name)

    if found_path == None or not os.path.exists(found_path):
        return 1 # cannot delete file
    
    os.remove(found_path)
    return 0 # successful deletion

# Write Data
# overwrites information if the file exists
# returns 1 if it does not exist, returns 0 if successful
def write_data(file_name, data):
    found_path = locate_file(file_name)
    # if item does not exist, we cannot write to it
    
    if found_path == None or not os.path.exists(found_path):
        return 1 # cannot write to file
    
    # use pickle to serialize Python objects and record into the file
    with open(found_path, 'wb') as file:
        for item in data:
            pickle.dump(item, file)
    
    return 0

# Read Data
# copy out the binary contents of a file into a list of items and return it
# returns None if there was no valid file found
def read_data(file_name):
    found_path = locate_file(file_name)

    if found_path == None or not os.path.exists(found_path):
        return None # cannot read file
    
    # use pickle to deserialize each item into Python objects
    data = []
    with open(found_path, 'rb') as file:
        while True:
            try:
                data.append(pickle.load(file))
            except EOFError:
                break
    
    # test for empty binary file
    if len(data) == 0:
        return None
    
    return data

# Locate File
# searches project files for every match, returning the path to that file
# returns None if there were 0/multiple matches or file is not a file
def locate_file(file_name):
    matches = []

    # error log is found in src, but can still be edited
    if file_name == ERROR_LOG:
        return os.path.join(PROJECT_ROOT, SOURCE_PATH, ERROR_LOG)

    for root, dirs, files in os.walk(PROJECT_ROOT):
        if SOURCE_PATH in dirs:
            dirs.remove(SOURCE_PATH)
        
        if file_name in files and file_name not in FILE_DEPENDENCIES:
            file_path = os.path.join(root, file_name)
            # Ensure the match is a file
            if os.path.isfile(file_path):  
                matches.append(file_path)
    
    if len(matches) != 1:
        return None
    else:
        return matches[0]