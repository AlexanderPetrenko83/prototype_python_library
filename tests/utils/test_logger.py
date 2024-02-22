import pytest
import os
import sys
import shutil

python_path = os.path.join(os.getcwd())
sys.path.append(python_path)
os.environ["PYTHONPATH"] = python_path

from prototype_python_library.utils.logger import Logger


@pytest.fixture
def init_logger():
    return Logger()


def test_type_logger(init_logger):
    logger = init_logger
    assert logger.__class__.__name__ == 'Logger'


def test_default_attributes_logger(init_logger):
    logger = init_logger

    attributes = {
        'log_to_console': True,
        'log_to_file': False,
        'log_from_custom': False,
        'log_name': 'logger',
        'log_path': None,
        'log_file': None,
        'logging': None
        }

    assert logger.__dict__ == attributes


def test_methods_logger(init_logger):
    logger = init_logger

    methods = [method_name for method_name in dir(logger) if callable(getattr(logger, method_name))]

    assert 'create_logger' in methods
    assert 'info' in methods


def test_create_folder_for_logger():
    logger = Logger('test_logger', log_to_file=True, log_path=None)
    logger.create_logger()

    directories = [name for name in os.listdir(".") if os.path.isdir(name)]

    assert 'logs' in directories

    shutil.rmtree('logs')

