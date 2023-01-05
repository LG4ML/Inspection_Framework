import pandas as pd
import numpy as np
import datetime as dt
from typing import Union, Optional, List, Tuple, Dict


def convert_to_datetime(values: Union[pd.Series, np.ndarray, List[str]], fmt: str = None,
                        result: str = 'series') -> Union[pd.Series, np.ndarray, List[dt.datetime]]:
    pass


def convert_to_numerical(values: Union[pd.Series, np.ndarray, List[str]],
                         result: str = 'series') -> Union[pd.Series, np.ndarray, List[float]]:
    pass


def convert_to_categorical(values: Union[pd.Series, np.ndarray, List[str]],
                           result: str = 'series') -> Union[pd.Series, np.ndarray, List[str]]:
    pass


def convert_to_boolean(values: Union[pd.Series, np.ndarray, List[str]]) -> pd.Series:
    pass
