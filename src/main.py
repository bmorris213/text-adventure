# Text Adventure
# 05-27-24
# Brian Morris

from gamemanager import GameManager

# Main
# program begins execution here
# execution is passed to game manager
def main():
    # initialize new game environment
    new_session = GameManager()

    # pass execution to game manager
    new_session.run()

if __name__ == '__main__':
    main()