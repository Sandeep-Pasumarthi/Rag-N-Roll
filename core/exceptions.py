import sys
import traceback


class CustomException(Exception):
    def __init__(self, error_message:str, error_details:sys):
        _, _, exc_tb = error_details.exc_info()
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_number = exc_tb.tb_lineno
        self.error_message = error_message
        self.traceback_str = "".join(traceback.format_exception(*error_details.exc_info()))

    def __str__(self):
        return f"""
    Error in [{self.file_name}] at line [{self.line_number}]
    Message:
    {self.error_message}
    Traceback:
    {self.traceback_str}
    """
