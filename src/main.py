# Text Adventure
# 05-27-24
# Brian Morris

# Main
# program begins execution here
# execution is passed to game manager

from gamemanager import GameManager

def main():
    # initialize new game environment
    new_session = GameManager()

    # pass execution to game manager
    new_session.run()

if __name__ == '__main__':
    main()