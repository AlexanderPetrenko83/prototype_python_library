import pandas as pd
import inspect

from prototype_python_library.utils.logger import Logger


class LogisticModel:
    """
    Class representing

    """

    def __init__(self,
                 log_to_console: bool = True,
                 log_to_file: bool = False,
                 log_from_custom: bool = False,
                 log_path: str = None,
                 log_file: str = None) -> None:

        bool_variables = {'log_to_console': log_to_console,
                          'log_to_file': log_to_file,
                          'log_from_custom': log_from_custom}

        string_variables = {'log_path': log_path,
                            'log_file': log_file}

        for key, value in bool_variables.items():
            self.verify_flag(value, key)

        for key, value in string_variables.items():
            self.verify_str_or_none(value, key)

        self.__log_to_console = log_to_console
        self.__log_to_file = log_to_file
        self.__log_from_custom = log_from_custom

        self.__log_path = log_path
        if self.log_to_file:
            if log_file is None:
                self.__log_file = self.__class__.__name__
            else:
                self.__log_file = log_file
        else:
            self.__log_file = log_file

        self.logger = Logger(
            log_to_console=self.log_to_console,
            log_to_file=self.log_to_file,
            log_from_custom=self.log_from_custom,
            log_name=f'Logger for {self.__class__.__name__}',
            log_path=self.log_path,
            log_file=self.log_file
        )

        if self.log_to_console:
            self.logger.info(f"Object initialization of class: {self.__class__.__name__}")
            self.logger.info(f'Object created: {self.__repr__()}')

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
    def log_path(self):
        return self.__log_path

    @property
    def log_file(self):
        return self.__log_file

    @classmethod
    def verify_flag(cls, flag_value, flag_name):
        if type(flag_value) != bool:
            raise TypeError(f'{flag_name} must be bool, not {type(flag_name)}')

    @classmethod
    def verify_str_or_none(cls, string_value, string_name):
        if type(string_value) != str and string_value is not None:
            raise TypeError(f'{string_name} must be string or None, not {type(string_value)}')

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


    def __repr__(self):

        return (
            f'{self.__class__.__name__}('
            f'log_to_console={self.log_to_console}, '
            f'log_to_file={self.log_to_file}, '
            f'log_from_custom={self.log_from_custom}, '
            f'log_path={self.log_path}, '
            f'log_file={self.log_file})'
        )

    def tariffs(self,
                df_tariffs: pd.DataFrame,
                tariff_data_source: str = 'method_1') -> pd.DataFrame:
        """

        :param tariff_data_source: User has options choosing source of tariffs:
                                                                            'custom'
        :param df_tariffs: The dataset must correspond to the selected data source format.
        :return: Prepared tariff dataset.
                 Dataframe columns:
                                lower_limit_rate_km: int
                                upper_limit_rate_km: int
        """
        if self.log_to_console:
            self.logger.info(f"Run {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")

        self.verify_dataframe(df_tariffs, 'df_tariffs')

        if tariff_data_source == 'method_1':
            self.verify_tariffs_method_1_columns(df_tariffs.columns.tolist())

        df_tariffs[['lower_limit_rate_km', 'upper_limit_rate_km']] = \
            df_tariffs['distance_km'].str.split(' ', expand=True)[[2, 4]]

        df_tariffs = df_tariffs.dropna()[[
            'region',
            'logistic_rate',
            'lower_limit_rate_km',
            'upper_limit_rate_km',
            'unit']]

        df_tariffs['logistic_rate'] = (df_tariffs['logistic_rate']
                                       .astype('str')
                                       .apply(lambda x: x.replace(',', '.'))
                                       .astype('float'))
        df_tariffs['lower_limit_rate_km'] = (df_tariffs['lower_limit_rate_km']
                                             .astype('str')
                                             .apply(lambda x: x.replace(',', '.'))
                                             .astype('float'))
        df_tariffs['upper_limit_rate_km'] = (df_tariffs['upper_limit_rate_km']
                                             .astype('str')
                                             .apply(lambda x: x.replace(',', '.'))
                                             .astype('float'))

        return df_tariffs

    def logistic_cost(self,
                      df_matrix_of_distances: pd.DataFrame,
                      df_tariffs: pd.DataFrame,
                      df_field_to_region: pd.DataFrame) -> pd.DataFrame:
        """

        :param df_field_to_region: Dataframe
        :param df_matrix_of_distances: Dataframe format distance matrix.
                                       Dataframe columns:
                                                    from: str,
                                                    to: str,
                                                    distance: float

        :param df_tariffs: Dataframe format tariff dataset.
                           Dataframe columns:
                                        lower_limit_rate_km: int
                                        upper_limit_rate_km: int

        :return: Dataframe format logistic cost dataset.
                 Dataframe columns:
                                from: str,
                                to: str,
                                distance: float
                                logistic_tariff_by_tn: float


        """
        if self.log_to_console:
            self.logger.info(f"Run {self.__class__.__name__}.{inspect.currentframe().f_code.co_name}")

        dfs = {'df_matrix_of_distances': df_matrix_of_distances,
               'df_tariffs': df_tariffs,
               'df_field_to_region': df_field_to_region}

        for key, value in dfs.items():
            self.verify_dataframe(value, key)

        self.verify_matrix_of_distance_columns(df_matrix_of_distances.columns.tolist())
        self.verify_tariffs_columns(df_tariffs.columns.tolist())
        self.verify_field_to_region_columns(df_field_to_region.columns.tolist())

        df = df_matrix_of_distances.merge(df_field_to_region, on=['from'], how='left').dropna()

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
