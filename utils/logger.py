import logging
class Logger(object):
    def __init__(self):
        
        self.logger = logging.getLogger(__name__)
        handler1 = logging.StreamHandler()
        handler2 = logging.FileHandler(filename="run_test.log")
        self.logger.setLevel(logging.DEBUG)
        handler1.setLevel(logging.WARNING)
        handler2.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s  %(levelname)-4s [%(name)s] %(module)s:%(funcName)s:%(lineno)d#    %(message)s")
        handler1.setFormatter(formatter)
        handler2.setFormatter(formatter)

        self.logger.addHandler(handler1)
        self.logger.addHandler(handler2)

    def get_logger(self):
        return self.logger

logger = Logger().get_logger()