# Text Adventure
# 05-27-24
# Brian Morris

import unittest

from mode import Mode

# Test Mode
# unit tests for mode
class TestMode(unittest.TestCase):
    def setUp(self):
        def add(objects, targets=None):
            sum = 0
            for key, value in objects.items():
                if targets == None:
                    sum += value
                elif key in targets:
                    sum += value
            return sum
        def test(objects, targets=None):
            return "testing..."
        
        self.mode = Mode("Test")

        self.mode.add_command("test", test)
        self.mode.add_command("add", add, "Adds any amount of items")
        self.mode.add_object("one", 1)
        self.mode.add_object("two", 2)
        
    def test_run_command(self):
        test_suite = [ "help", "help help", "look", "look one",
            "look two", "help look back quit", "back", "quit",
            "add", "help add", "test", "add two", "lok",
            "look monkey", "help monkey" ]
        expected_results = [
            ["help", "look", "back", "quit", "test", "add"],
            { "help" : "List commands, or get a hint on any object or command." },
            ["one", "two"], { "one" : 1 }, { "two" : 2 },
            { "look" : "List objects, or get some details on any object.",
            "back" : "Return to previous menu, or close menu.",
            "quit" : "Quit to main menu or desktop." },
            f"{Mode.CHANGE_MODE}{Mode.BACK_SIGNITURE}",
            f"{Mode.CHANGE_MODE}{Mode.QUIT_SIGNITURE}", 3,
            { "add" : "Adds any amount of items" },
            "testing...", 2, None,
            { "monkey" : None },
            { "monkey" : None } ]
        
        for i in range(len(test_suite)):
            words = test_suite[i].split(' ')
            verb = words[0]
            noun_list = []
            if len(words) > 1:
                noun_list = words[1:]
            else:
                noun_list = None
            
            result = self.mode.run_command(verb, noun_list)

            self.assertEqual(result, expected_results[i])
if __name__ == '__main__':
    unittest.main()