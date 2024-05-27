# Text Adventure
# 05-27-2024
# Brian Morris

import sys
import inspect
from datetime import datetime

# Error Manager
# stores and logs error reports
# gracefully handles any crashes
class ErrorManager():
    # instances of error manager store logged errors
    def __init__(self):
        self.log = []
    
    # store a thrown exception to be reported later
    # takes an exception-type report
    def log_error(self, exception_reported):
        # ensure argument is an exception
        if isinstance(exception_reported, Exception) == False:
            exception_reported = Exception("log-error requires an exception as input")
        
        # get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # get source of the error
        caller_frame = inspect.currentframe().f_back

        filename = caller_frame.f_code.co_filename
        caller_class = caller_frame.f_locals.get('self', None).__class__.__name__
        function_name = caller_frame.f_code.co_filename
        line_number = caller_frame.f_lineno

        source = f"{filename}/{caller_class}: {function_name} line {line_number}"

        # get the type of exception
        error_type = type(exception_reported).__name__

        # create log
        error_report = f"ERROR\nfrom source {source} at time {current_time}."
        error_report += f"\nReported as {error_type}: {str(exception_reported)}.\n"

        # store error
        self.log += error_report
    
    # gracefully handle a fatal error and exit the program
    def close_program(self):
        # log a fatal error
        self.log_error(Exception("fatal error encountered"))

        # report all errors
        self.inspect_errors()
        
        # gracefully exit program
        sys.exit(1)

    # view all current errors with stderr
    def inspect_errors(self):
        # send all errors in log to sderr
        for error_report in self.log:
            print(error_report, file=sys.stderr)
