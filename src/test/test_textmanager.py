# Text Adventure
# 05-27-24
# Brian Morris

import unittest
from unittest.mock import patch, call

import textmanager

# Test TextManager
# unit tests for text manager
class TestTextManager(unittest.TestCase):
    # ensure prompting user works as intended
    @patch('builtins.print')
    @patch('textmanager.time.sleep', return_value=None)
    def test_display_text(self, mock_sleep, mock_print):
        test_string = "Testing1...\nTesting2...\nTesting3..."
        test_values = [ 0, textmanager.QUICK_TEXT, textmanager.NORMAL_TEXT, textmanager.SLOW_TEXT, 500 ]

        for i in range(len(test_values)):
            textmanager.display_text(test_string, test_values[i])
        
        # ensure correct breaking up of prints in print with 0 delay
        mock_print.assert_any_call(f"{textmanager.TERMINAL_TAG}Testing1...")
        mock_print.assert_any_call(f"{textmanager.TERMINAL_TAG}Testing2...")
        mock_print.assert_any_call(f"{textmanager.TERMINAL_TAG}Testing3...")

        # ensure delays have been called with the correct values
        expected_calls = []
        for i in range(len(test_values)):
            if i != 0:
                adjusted_time_delay = min(test_values[i], textmanager.MAX_DELAY)
                char_delay = adjusted_time_delay / 5
                line_delay = adjusted_time_delay * 5

                for line in test_string.split('\n'):
                    expected_calls.extend([call(char_delay) for _ in line])
                    expected_calls.append(call(line_delay))

        self.assertEqual(mock_sleep.call_count, len(expected_calls))
        mock_sleep.assert_has_calls(expected_calls, any_order=True)


    # ensure user input retrieval is handled successfully
    def test_get_input(self):
        test_suite = [ "test", " words with spaces ", "CAPS    WORDS", "something_invalid", "     " ]
        results = [ "test", "words with spaces", "caps words", None, None ]

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