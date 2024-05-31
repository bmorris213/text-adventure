# Text Adventure
# 05-30-24
# Brian Morris

import unittest
from displaymanager import MainMenu

# Test DisplayManager
# unit tests for display manager
class TestDisplayManager(unittest.TestCase):
    def test_window(self):
        win = MainMenu()
        win.wait_for_close()

if __name__ == '__main__':
    unittest.main()