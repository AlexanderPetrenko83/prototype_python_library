import pytest
import os
import sys
import pandas as pd

python_path = os.path.join(os.getcwd())
sys.path.append(python_path)
os.environ["PYTHONPATH"] = python_path

from prototype_python_library.calculations.logistic_model import LogisticModel


@pytest.fixture
def init_logistic_cost():
    return LogisticModel()


df_field_to_region = pd.read_csv('tests/data/field_to_region.csv').drop('Unnamed: 0', axis=1)
df_logistic_cost = pd.read_csv('tests/data/logistic_cost.csv').drop('Unnamed: 0', axis=1)
df_logistic_rates = pd.read_csv('tests/data/logistic_rates.csv').drop('Unnamed: 0', axis=1)
df_logistic_rates_prepared = pd.read_csv('tests/data/logistic_rates_prepared.csv').drop('Unnamed: 0', axis=1)
df_matrix_distance = pd.read_csv('tests/data/matrix_distance.csv').drop('Unnamed: 0', axis=1)


def test_type_logistic_cost(init_logistic_cost):
    logistic = init_logistic_cost
    assert logistic.__class__.__name__ == 'LogisticModel'


def test_attributes_logistic_cost(init_logistic_cost):
    logistic = init_logistic_cost
    attributes = [
        'log_to_console',
        'log_to_file',
        'log_from_custom',
        'log_path',
        'log_file',
        'logger'
    ]

    assert sorted(list(logistic.__dict__.keys())) == sorted(attributes)


def test_methods_logistic_cost(init_logistic_cost):
    logistic = init_logistic_cost

    methods = [method_name for method_name in dir(logistic) if callable(getattr(logistic, method_name))]

    assert 'tariffs' in methods
    assert 'logistic_cost' in methods


def test_tariffs(init_logistic_cost):
    logistic = init_logistic_cost
    df = logistic.tariffs(df_logistic_rates)

    assert sorted(df.columns.tolist()) == sorted(df_logistic_rates_prepared.columns.tolist())
    assert df.dtypes.apply(lambda x: x.name).to_dict() == \
           df_logistic_rates_prepared.dtypes.apply(lambda x: x.name).to_dict()
    assert df.shape[0] == df_logistic_rates_prepared.shape[0]
    assert df['region'].values.tolist() == df_logistic_rates_prepared['region'].values.tolist()
    assert df['logistic_rate'].values.tolist() == df_logistic_rates_prepared['logistic_rate'].values.tolist()
    assert df['lower_limit_rate_km'].values.tolist() == df_logistic_rates_prepared[
        'lower_limit_rate_km'].values.tolist()
    assert df['upper_limit_rate_km'].values.tolist() == df_logistic_rates_prepared[
        'upper_limit_rate_km'].values.tolist()
    assert df['unit'].values.tolist() == df_logistic_rates_prepared['unit'].values.tolist()


def test_logistic_cost(init_logistic_cost):
    logistic = init_logistic_cost
    df = logistic.logistic_cost(df_matrix_distance,
                                df_logistic_rates_prepared,
                                df_field_to_region)

    assert sorted(df.columns.tolist()) == sorted(df_logistic_cost.columns.tolist())
    assert df.dtypes.apply(lambda x: x.name).to_dict() == \
           df_logistic_cost.dtypes.apply(lambda x: x.name).to_dict()
    assert df.shape[0] == df_logistic_cost.shape[0]
    assert df['from'].values.tolist() == df_logistic_cost['from'].values.tolist()
    assert df['to'].values.tolist() == df_logistic_cost['to'].values.tolist()
    assert df['distance'].values.tolist() == df_logistic_cost['distance'].values.tolist()
    assert df['region'].values.tolist() == df_logistic_cost['region'].values.tolist()
    assert df['logistic_rate'].values.tolist() == df_logistic_cost['logistic_rate'].values.tolist()
    assert list(map(int, df['logistic_tariff_by_tn'].values.tolist())) == \
           list(map(int, df_logistic_cost['logistic_tariff_by_tn'].values.tolist()))
