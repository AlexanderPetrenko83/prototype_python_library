import pandas as pd
import inspect
from typing import Optional

from prototype_python_library.utils.logger import Logger


class LogisticModel:
    """

    The class contains typical calculations related to the logistics of RusAgro products:
        1) Automatic collection of the following data from various systems:
            - distance matrix,
            - tariffs (car, train),
            - point-region.
        2) Data processing.
        3) Calculation of product delivery costs.

    """

    def __init__(self) -> None:

        self.logger = None
        self.log_to_stream = False
        self.log_to_file = False
        self.log_from_custom = False
        self.log_path = None
        self.log_file = None

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @classmethod
    def verify_str(cls, string):
        if type(string) is not str:
            raise TypeError(f'Variable must be string, not {type(string)}')

    @classmethod
    def verify_flag(cls, flag):
        if type(flag) is not bool:
            raise TypeError(f'Variable must be bool, not {type(flag)}')

    @classmethod
    def verify_dataframe(cls, dataframe, dataframe_name):
        if type(dataframe) != pd.DataFrame:
            raise TypeError(f'{dataframe_name} must be pandas DataFrame object, not {type(dataframe)}')

    @classmethod
    def verify_tariffs_method_1_columns(cls, columns_given):
        columns_expected = ['region',
                            'distance_km',
                            'logistic_rate',
                            'unit']
        if sorted(columns_given) != sorted(columns_expected):
            raise ValueError(f'Expected columns {sorted(columns_expected)}, but columns given {sorted(columns_given)}')

    @classmethod
    def verify_tariffs_columns(cls, columns_given):
        columns_expected = ['region',
                            'logistic_rate',
                            'lower_limit_rate_km',
                            'upper_limit_rate_km',
                            'unit']
        if sorted(columns_given) != sorted(columns_expected):
            raise ValueError(f'Expected columns {sorted(columns_expected)}, but columns given {sorted(columns_given)}')

    @classmethod
    def verify_matrix_of_distance_columns(cls, columns_given):
        columns_expected = ['from',
                            'to',
                            'distance']
        if sorted(columns_given) != sorted(columns_expected):
            raise ValueError(f'Expected columns {sorted(columns_expected)}, but columns given {sorted(columns_given)}')

    @classmethod
    def verify_field_to_region_columns(cls, columns_given):
        columns_expected = ['from',
                            'region']
        if sorted(columns_given) != sorted(columns_expected):
            raise ValueError(f'Expected columns {sorted(columns_expected)}, but columns given {sorted(columns_given)}')

    @classmethod
    def verify_methods_of_preprocessing_tariffs(cls, method_given):
        methods_expected = ['method_1']
        if method_given not in methods_expected:
            raise ValueError(f'Expected methods {methods_expected}, but method given {method_given}')

    def init_logger(self,
                    log_to_stream: bool = True,
                    log_to_file: bool = True,
                    log_from_custom: bool = False,
                    log_path: Optional[str] = None,
                    log_file: Optional[str] = None
                    ) -> None:
        """
        The method initializes the logger

        :param log_to_stream: If True, logs will be output to the console. Defaults to True.
        :param log_to_file: If True, logs will be output to the file. Defaults to True.
        :param log_from_custom: In developing.
        :param log_path: Path to the log file. Defaults to None.
        :param log_file: Name of the log file. Defaults to None.
        :return:
        """

        for i in [log_to_stream, log_to_file, log_from_custom]:
            self.verify_flag(i)

        for i in [log_path, log_file]:
            if i is not None:
                self.verify_str(i)

        self.log_to_stream = log_to_stream
        self.log_to_file = log_to_file
        self.log_from_custom = log_from_custom
        self.log_path = log_path
        self.log_file = log_file

        self.logger = Logger(
            log_to_stream=self.log_to_stream,
            log_to_file=self.log_to_file,
            log_from_custom=self.log_from_custom,
            log_name=f'Logger for {self.__class__.__name__}',
            log_path=self.log_path,
            log_file=self.log_file
        )

        if self.log_to_stream or self.log_to_file:
            self.logger.info(f"Object initialization of class: {self.__class__.__name__}")
            self.logger.info(f'Object created: {self.__repr__()}')

    def tariffs(self,
                df_tariffs: pd.DataFrame,
                tariff_data_method: str = 'method_1') -> pd.DataFrame:
        """
        The method to preprocess data for tariff dataset

        :param df_tariffs: Dataset that will be preprocessed into tariffs.
        :param tariff_data_method: There are methods for preprocessing to tariff dataset.
        :return: Preprocessed tariff dataset.

        """
        if self.log_to_stream or self.log_to_file:
            self.logger.info(f"Run {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")

        self.verify_dataframe(df_tariffs, 'df_tariffs')
        self.verify_methods_of_preprocessing_tariffs(tariff_data_method)
        if tariff_data_method == 'method_1':
            self.verify_tariffs_method_1_columns(df_tariffs.columns.tolist())

        df = df_tariffs.copy()

        df[['lower_limit_rate_km', 'upper_limit_rate_km']] = df['distance_km'].str.split(' ', expand=True)[[2, 4]]

        df = df.dropna()[[
            'region',
            'logistic_rate',
            'lower_limit_rate_km',
            'upper_limit_rate_km',
            'unit']]

        df['logistic_rate'] = (df['logistic_rate']
                               .astype('str')
                               .apply(lambda x: x.replace(',', '.'))
                               .astype('float'))
        df['lower_limit_rate_km'] = (df['lower_limit_rate_km']
                                     .astype('str')
                                     .apply(lambda x: x.replace(',', '.'))
                                     .astype('float'))
        df['upper_limit_rate_km'] = (df['upper_limit_rate_km']
                                     .astype('str')
                                     .apply(lambda x: x.replace(',', '.'))
                                     .astype('float'))

        return df

    def logistic_cost(self,
                      df_matrix_of_distances: pd.DataFrame,
                      df_tariffs: pd.DataFrame,
                      df_field_to_region: pd.DataFrame) -> pd.DataFrame:
        """
        The method to calculate the logistic cost.

        :param df_matrix_of_distances: Dataframe format distance matrix.
        :param df_tariffs: Dataframe format tariff dataset.
        :param df_field_to_region: Dataframe with fields and their belonging to the region.

        :return: Dataframe format logistic cost dataset.

        """
        if self.log_to_stream or self.log_to_file:
            self.logger.info(f"Run {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")

        dfs = {'df_matrix_of_distances': df_matrix_of_distances,
               'df_tariffs': df_tariffs,
               'df_field_to_region': df_field_to_region}

        for key, value in dfs.items():
            self.verify_dataframe(value, key)

        self.verify_matrix_of_distance_columns(df_matrix_of_distances.columns.tolist())
        self.verify_tariffs_columns(df_tariffs.columns.tolist())
        self.verify_field_to_region_columns(df_field_to_region.columns.tolist())

        df = df_matrix_of_distances.merge(df_field_to_region, on=['from'], how='left').dropna().copy()

        df = (df
              .merge(df_tariffs, on=['region'], how='left')
              .assign(distance_true=lambda x: (x.distance >= x.lower_limit_rate_km)
                                              & (x.distance < x.upper_limit_rate_km)))

        df = (df[df['distance_true'] == True]
              .drop(columns=['lower_limit_rate_km', 'upper_limit_rate_km', 'distance_true']))

        df.loc[(df['unit'] == 'тн*км'), 'logistic_tariff_by_tn'] = \
            df.logistic_rate * df.distance
        df.loc[(df['unit'] == 'тн'), 'logistic_tariff_by_tn'] = \
            df.logistic_rate

        df = df.drop(columns=['unit'])

        return df
