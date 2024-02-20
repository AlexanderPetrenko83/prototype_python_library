import pandas as pd
import inspect

from prototype_python_library.utils.logger import Logger


class LogisticCost:
    """
    Class representing a calculating of logistic cost

    """

    def __init__(self,
                 log_to_console: bool = True,
                 log_to_file: bool = False,
                 log_from_custom: bool = False,
                 log_path: str = None,
                 log_file: str = None) -> None:

        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.log_from_custom = log_from_custom
        self.log_path = log_path
        if self.log_to_file:
            if log_file is None:
                self.log_file = self.__class__.__name__
            else:
                self.log_file = log_file
        else:
            self.log_file = log_file

        self.logger = Logger(name_log=f'Logger for {self.__class__.__name__}',
                             log_to_console=self.log_to_console,
                             log_to_file=self.log_to_file,
                             log_from_custom=self.log_from_custom,
                             log_path=self.log_path,
                             log_file=self.log_file)
        self.logger.create_logger()

        if self.log_to_console:
            self.logger.info(f"Initialize {self.__class__.__name__}")
            self.logger.info(self.__repr__())

    def __repr__(self):

        return (
            f'{self.__class__.__name__}('
            f'log_to_console={self.log_to_console}, '
            f'log_to_file={self.log_to_file}, '
            f'log_from_custom={self.log_from_custom}, '
            f'log_path={self.log_path}, '
            f'log_file={self.log_file})'
        )

    @property
    def fullname(self):
        return (f'{self.log_to_console} '
                f'{self.log_to_file} '
                f'{self.log_from_custom} '
                f'{self.log_path} '
                f'{self.log_file}')

    def prepare_tariffs(self,
                        df_tariffs: pd.DataFrame,
                        tariff_data_source: str = 'custom') -> pd.DataFrame:
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

    def get_logistic_cost(self,
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
