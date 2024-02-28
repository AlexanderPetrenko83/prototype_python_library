import logging

from pathlib import Path
from time import gmtime, strftime
from typing import Optional


class Logger:
    """

    The class creates a logger. The class pre-provides logger settings, which simplifies the use of the logger.

    :param log_to_stream: If True, logs will be output to the console. Defaults to True.
    :param log_to_file: If True, logs will be output to the file. Defaults to False.
    :param log_from_custom: In developing.
    :param log_name: Name to the logger. Defaults to 'MathOptLogger'.
    :param log_path: Path to the log file. Defaults to None.
    :param log_file: Name of the log file. Defaults to None.


    """
    def __init__(self,
                 log_to_stream: bool = True,
                 log_to_file: bool = False,
                 log_from_custom: bool = False,
                 log_name: Optional[str] = 'MathOptLogger',
                 log_path: Optional[str] = None,
                 log_file: Optional[str] = None) -> None:

        bool_variables = {'log_to_stream': log_to_stream,
                          'log_to_file': log_to_file,
                          'log_from_custom': log_from_custom}

        string_variables = {'log_name': log_name,
                            'log_path': log_path,
                            'log_file': log_file}

        for key, value in bool_variables.items():
            self.verify_flag(value, key)

        for key, value in string_variables.items():
            if value is not None:
                self.verify_str(value, key)

        self.log_to_stream = log_to_stream
        self.log_to_file = log_to_file
        self.log_from_custom = log_from_custom

        self.log_name = log_name

        if self.log_to_file:
            if log_path is None:
                self.log_path = 'logs/'
            else:
                self.log_path = log_path

            if log_file is None:
                self.log_file = self.log_name
            else:
                self.log_file = log_file
        else:
            self.log_path = log_path
            self.log_file = log_file

        self.logging = None
        self.create_logger()

    def __repr__(self):

        return (
            f'{self.__class__.__name__}('
            f'log_to_stream={self.log_to_stream}, '
            f'log_to_file={self.log_to_file}, '
            f'log_from_custom={self.log_from_custom}, '
            f'log_name={self.log_name}, '
            f'log_path={self.log_path}, '
            f'log_file={self.log_file})'
        )

    @classmethod
    def verify_flag(cls, flag_value, flag_name):
        if type(flag_value) is not bool:
            raise TypeError(f'{flag_name} must be bool, not {type(flag_name)}')

    @classmethod
    def verify_str(cls, string_value, string_name):
        if type(string_value) is not str:
            raise TypeError(f'{string_name} must be string, not {type(string_value)}')

    def create_logger(self,
                      show_output: bool = False) -> None:
        """
        The method creates a logger.
        :param show_output: If it is True, the logger will print to console a message "Logger created". Default is False.
        :return: None
        """

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

        if show_output:
            self.logging.info('Logger created')

    def info(self,
             some_text: str = 'put some text here'):
        self.logging.info(some_text)

    def info_run_module(self, name_of_function: str = 'put some text here'):
        self.logging.info(f"------- Module '{name_of_function}' is running -------")

    def info_complete_module(self, name_of_function: str = 'put some text here'):
        self.logging.info(f"------- Module '{name_of_function}' completed -------\n")

    def info_download_parameters(self):
        self.logging.info(f"Parameters is downloading")

    def info_checking_the_directory(self):
        self.logging.info(f"Checking & creating the directory")
