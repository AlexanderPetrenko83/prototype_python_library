import logging

from pathlib import Path
from time import gmtime, strftime


class Logger:
    def __init__(self,
                 log_to_console: bool = True,
                 log_to_file: bool = False,
                 log_from_custom: bool = False,
                 log_name: str = None,
                 log_path: str = None,
                 log_file: str = None):

        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.log_from_custom = log_from_custom

        if log_to_console or log_to_file or log_from_custom:
            if log_name is None:
                self.log_name = 'logger'
            else:
                self.log_name = log_name
        else:
            self.log_name = log_name

        if self.log_to_file:
            if log_path is None:
                self.log_path = 'logs/'
            else:
                self.log_path = log_path
        else:
            self.log_path = log_path
        self.log_file = log_file

        self.logging = None

    def __repr__(self):

        return (
            f'{self.__class__.__name__}('
            f'log_to_console={self.log_to_console}, '
            f'log_to_file={self.log_to_file}, '
            f'log_from_custom={self.log_from_custom}, '
            f'log_name={self.log_name}, '
            f'log_path={self.log_path}, '
            f'log_file={self.log_file})'
        )

    def create_logger(self):

        time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        HANDLERS = [logging.StreamHandler()]

        if self.log_to_file:
            Path(self.log_path).mkdir(parents=True, exist_ok=True)
            HANDLERS.append(logging.FileHandler(f'{self.log_path}{self.log_file}_{time_now}'))

        logging.basicConfig(
            format='%(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO,
            handlers=HANDLERS)
        self.logging = logging

        self.logging.info('Logger created')

    def info(self, some_text):
        self.logging.info(some_text)
