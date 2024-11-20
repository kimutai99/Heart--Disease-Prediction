import sys
from src.logger import logging

def get_error_message(error, error_detail: sys):
    '''
    This function generates an error message that includes the file name, line number, and the original error message.
    '''
    try:
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in script: [{file_name}], line: [{line_number}], message: [{str(error)}]"
    except Exception as e:
        error_message = f"Error in error handling: {str(e)}"
    
    return error_message

class CustomException(Exception):
    def __init__(self, error, error_detail: sys):
        '''
        Initialize the custom exception with the error message.
        '''
        # Get the detailed error message using the get_error_message function
        error_message = get_error_message(error, error_detail)
        
        # Log the error message to a logging system
        logging.error(f"CustomException: {error_message}")
        
        # Pass the error message to the parent Exception class
        super().__init__(error_message)
        self.error_message = error_message
        
    def __str__(self):
        return self.error_message
