import logging

from pathlib import Path
from time import gmtime, strftime


class Logger:
    """
    Logger class


    """
    def __init__(self,
                 log_to_console: bool = True,
                 log_to_file: bool = False,
                 log_from_custom: bool = False,
                 log_name: str = None,
                 log_path: str = None,
                 log_file: str = None):

        bool_variables = {'log_to_console': log_to_console,
                          'log_to_file': log_to_file,
                          'log_from_custom': log_from_custom}

        string_variables = {'log_name': log_name,
                            'log_path': log_path,
                            'log_file': log_file}

        for key, value in bool_variables.items():
            self.verify_flag(value, key)

        for key, value in string_variables.items():
            self.verify_str_or_none(value, key)

        self.__log_to_console = log_to_console
        self.__log_to_file = log_to_file
        self.__log_from_custom = log_from_custom

        if log_to_console or log_to_file or log_from_custom:
            if log_name is None:
                self.__log_name = 'MathOptLogger'
            else:
                self.__log_name = log_name
        else:
            self.__log_name = log_name

        if self.log_to_file:
            if log_path is None:
                self.__log_path = 'logs/'
            else:
                self.__log_path = log_path

            if log_file is None:
                self.__log_file = self.__log_name
            else:
                self.__log_file = log_file
        else:
            self.__log_path = log_path
            self.__log_file = log_file

        self.__logging = None
        self.create_logger()

    def __repr__(self):

        return (
            f'{self.__class__.__name__}('
            f'log_to_console={self.__log_to_console}, '
            f'log_to_file={self.__log_to_file}, '
            f'log_from_custom={self.__log_from_custom}, '
            f'log_name={self.__log_name}, '
            f'log_path={self.__log_path}, '
            f'log_file={self.__log_file})'
        )

    @property
    def log_to_console(self):
        return self.__log_to_console

    @property
    def log_to_file(self):
        return self.__log_to_file

    @property
    def log_from_custom(self):
        return self.__log_from_custom

    @property
    def log_name(self):
        return self.__log_name

    @property
    def log_path(self):
        return self.__log_path

    @property
    def log_file(self):
        return self.__log_file

    @property
    def logging(self):
        return self.__logging

    @logging.setter
    def logging(self, new_logging):
        self.__logging = new_logging

    @classmethod
    def verify_flag(cls, flag_value, flag_name):
        if type(flag_value) != bool:
            raise TypeError(f'{flag_name} must be bool, not {type(flag_name)}')

    @classmethod
    def verify_str(cls, string_value, string_name):
        if type(string_value) != str:
            raise TypeError(f'{string_name} must be string, not {type(string_value)}')

    @classmethod
    def verify_str_or_none(cls, string_value, string_name):
        if type(string_value) != str and string_value is not None:
            raise TypeError(f'{string_name} must be string or None, not {type(string_value)}')

    def create_logger(self,
                      show_output: bool = False):

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
