import sys
from src.logger import logging

def get_error_detail(error,error_detail:sys):
    '''
    This function generates error message that includes file name,line number and the original error message
    '''
    _, _, exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    line_number=exc_tb.tb_lineno
    error_message=f'errror  occured in script:[{file_name}],line[{line_number}],message[{str(error)}]'
    return error_message

class CustomException(Exception):
    def __init__(self, error,error_detail:sys):
        '''
        Iniatialize the custom excption with the error message
        '''
        error_message=get_error_detail(error,error_detail)
        
        super().__init__(error_message)
        self.error_message=error_message
        
    def __str__(self):
        return  self.error_message     