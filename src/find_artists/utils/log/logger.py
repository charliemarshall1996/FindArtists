import logging


class Logger:
    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = logging.getLogger('findartist_logger')
        self.logger.setLevel(logging.DEBUG)
        self._configure_logger()

    def _configure_logger(self):
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(self.file_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message, *args):
        self.logger.debug(message, args)

    def info(self, message, *args):
        self.logger.info(message, args)

    def warning(self, message, *args):
        self.logger.warning(message, args)

    def error(self, message, *args):
        self.logger.error(message, args)

    def critical(self, message, *args):
        self.logger.critical(message, args)
