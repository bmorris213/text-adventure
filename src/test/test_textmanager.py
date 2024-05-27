# Text Adventure
# 05-27-24
# Brian Morris

import unittest

from textmanager import TextManager

# Test TextManager
# unit tests for text manager
class TestTextManager(unittest.TestCase):
    def test_to_lower(self):
        # define tests
        test_suite = [ "test", "TEST", "T", "o", "Te1s1T!", [ '_', " Test ", '_' ] ]
        results = [ "test", "test", "t", "o", "te1s1t!", "_ test _" ]

        for i in range(len(test_suite)):
            self.assertEqual(TextManager.to_lower(test_suite[i]), results[i])

if __name__ == '__main__':
    unittest.main()