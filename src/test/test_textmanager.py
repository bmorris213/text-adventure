# Text Adventure
# 05-30-24
# Brian Morris

import unittest
import sys
from unittest.mock import patch, call
from io import StringIO

import textmanager

# Test TextManager
# unit tests for text manager
class TestTextManager(unittest.TestCase):
    # ensure prompting user works as intended)
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_text(self, mock_stdout):
        test_string = "Testing1...\nTesting2...\nTesting3..."

        textmanager.display_text(test_string)
        
        # ensure correct breaking up of prints in print with 0 delay
        expected_output = mock_stdout.getvalue()
        self.assertTrue(f"{textmanager.TERMINAL_TAG}Testing1..." in expected_output)
        self.assertTrue(f"{textmanager.TERMINAL_TAG}Testing2..." in expected_output)
        self.assertTrue(f"{textmanager.TERMINAL_TAG}Testing3..." in expected_output)

        # test display works with given input of list
        test_string = []
        # ensure list is 3 x LINE_WIDTH
        for i in range(3):
            for j in range(textmanager.DEFAULT_LINE_WIDTH):
                test_string.append(f"line width {i}")
        test_string.extend(["test", "values"])

        expected_output = []
        current_length = 0
        line = ""
        # result should have 2 x LINE_WIDTH
        for i in range(2):
            line = ""
            for j in range(textmanager.DEFAULT_LINE_WIDTH):
                line += f"line width {i}, "
                current_length += 1
            expected_output.append(line)
        # add the first half(+1?) of the remainder
        line = ""
        new_width = (len(test_string) - current_length) // 2
        if new_width % 2 != 0:
            new_width += 1
        for i in range(new_width + 1):
            line += f"line width 2, "
            current_length += 1
        expected_output.append(line)

        # then add remaining amount
        current_length += 2 # don't add the last two
        line = ""
        for i in range(len(test_string) - current_length):
            line += f"line width 2, "
        line += f"test, values"
        expected_output.append(line)

        # call function, and ensure expected output is present
        textmanager.display_text(test_string)
        result = mock_stdout.getvalue()
        print(result, file=sys.stdout)

        for line in expected_output:
            self.assertTrue(f"{textmanager.TERMINAL_TAG}{line}" in result)

    # ensure user input retrieval is handled successfully
    def test_get_input(self):
        test_suite = [ "test", " words with spaces ", "CAPS    WORDS", "something_invalid", "     " ]
        results = [ ("test", None) , ("words", ["with", "spaces"]), ("caps", ["words"]), (None, None), (None, None) ]

        with patch('builtins.input', side_effect=test_suite) as mock_input:
            for i in range(len(test_suite)):
                self.assertEqual(textmanager.get_input(), results[i])

    # ensure character cases are lowered safely
    def test_to_lower(self):
        test_suite = [ "test", "TEST", "T", "o", "Te1s1T!", [ "_", " Test ", "_" ] ]
        results = [ "test", "test", "t", "o", "te1s1t!", "_ test _" ]

        for i in range(len(test_suite)):
            self.assertEqual(textmanager.to_lower(test_suite[i]), results[i])

if __name__ == '__main__':
    unittest.main()