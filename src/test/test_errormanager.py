# Text Adventure
# 05-27-24
# Brian Morris

import unittest
import sys
import os
from io import StringIO

from errormanager import ErrorManager

# Test ErrorManager
# unit tests for error manager
class TestErrorManager(unittest.TestCase):
    # initialize dummy environment
    def setUp(self):
        # redirect stderr
        self.saved_stderr = sys.stderr
        self.stderr = StringIO()
        sys.stderr = self.stderr
    
    # return to default environment
    def tearDown(self):
        sys.stderr = self.saved_stderr

    # ensure program gracefully exits
    def test_close_program(self):
        error_log = ErrorManager()

        # ensure program attempted close
        with self.assertRaises(SystemExit) as cm:
            error_log.close_program()

            self.assertEqual(cm.exception.code, 1)

        # ensure a fatal error was reported
        self.stderr.seek(0)
        error_output = self.stderr.read()
        self.assertTrue("Exception: fatal error encountered" in error_output)
    
    # ensure logs are reported successfully
    def test_report_errors(self):
        error_log = ErrorManager()

        test_values = [ Exception("test1"), ValueError("test2"),
            AssertionError("test3"), IndexError("test4") ]
        
        # log test errors
        for test_value in test_values:
            try:
                raise test_value
            except type(test_value) as e:
                error_log.log_error(e)

        error_log.inspect_errors()
        
        # ensure test errors were reported
        for test_value in test_values:
            self.stderr.seek(0)
            error_output = self.stderr.read()
            self.assertTrue(f"Reported as {type(test_value).__name__}: {str(test_value)}." in error_output)

        # ensure log_error raises correct exception
        try:
            error_log.log_error("invalid input")
        except Exception as e:
            self.assertEqual(str(e), "log-error requires an exception as input")

if __name__ == '__main__':
    unittest.main()