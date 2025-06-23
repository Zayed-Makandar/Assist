import logging

def log_error(self, error):
    logging.basicConfig(filename="assist_errors.log", level=logging.ERROR)
    logging.error(str(error))
    self.show_error(str(error))