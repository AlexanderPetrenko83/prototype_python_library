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
        'log_to_stream': True,
        'log_to_file': False,
        'log_from_custom': False,
        'log_name': 'MathOptLogger',
        'log_path': None,
        'log_file': None
        }

    logger_attributes = logger.__dict__.copy()
    logger_attributes.pop('logging')

    assert logger_attributes == attributes


def test_methods_logger(init_logger):
    logger = init_logger

    methods = [method_name for method_name in dir(logger) if callable(getattr(logger, method_name))]

    assert 'info' in methods
    assert 'info_run_module' in methods
    assert 'info_complete_module' in methods
    assert 'info_download_parameters' in methods
    assert 'info_checking_the_directory' in methods


def test_create_folder_for_logger():
    _ = Logger(log_name='test_logger', log_to_file=True, log_path=None)

    directories = [name for name in os.listdir(".") if os.path.isdir(name)]

    assert 'logs' in directories

    shutil.rmtree('logs')

