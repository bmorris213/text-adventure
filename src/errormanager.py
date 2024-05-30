# Text Adventure
# 05-30-2024
# Brian Morris

import sys
import inspect
from datetime import datetime

import filemanager

# Error Manager
# stores and logs error reports
# gracefully handles any crashes

# Log Error
# store a thrown exception to be reported later
# takes an exception-type report
def log_error(exception_reported):
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
    error_report = f"ERROR\nfrom source {source} at time {current_time}.\n"
    error_report += f"Reported as {error_type}: {str(exception_reported)}.\n"

    # store error
    filemanager.add_log(error_report)

# Close Program
# gracefully handle a fatal error and exit the program
def close_program():
    # log a fatal error
    log_error(Exception("fatal error encountered"))
        
    # gracefully exit program
    sys.exit(1)

# view all current errors with stderr
def inspect_errors():
    # get the log from file
    logs = filemanager.read_data(filemanager.ERROR_LOG)

    # if there were no logs, or file is missing, return
    if logs == None:
        return

    # send all errors in log to sderr
    for error_report in logs:
        print(error_report, file=sys.stderr)
