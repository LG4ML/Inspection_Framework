import DataLoader as Loader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Union, Optional


class DataInspection(ABC):
    """
    **Summary:**
    Base class for all types of data inspection. This class is abstract and cannot be instantiated.
    """

    @abstractmethod
    @property
    def data(self):
        pass

    @abstractmethod
    def create_report(self):
        pass


class DataFrameInspection(DataInspection):

    def __init__(self, data: pd.DataFrame = None, path: Union[str, Path] = None, encoding: str = 'utf-8',
                 sep: str = ',', decimal: str = '.', index_col: Union[int, List[int]] = None,
                 feature_names: List[str] = None, target_name: str = None, update_dtypes: bool = True):
        # Load data from file if path is provided
        if data is None and path is None:
            raise ValueError('Either data or path must be provided.')
        elif data is not None and path is not None:
            raise ValueError('Only one of data or path must be provided.')
        elif data is not None:
            self.__data = data
        else:
            self.__data = Loader.load_file(path, encoding, sep, decimal, index_col)

        # Set feature names, target name and target type
        self.__feature_names = feature_names
        self.__target_name = target_name
        if target_name is None:
            self.__target_type = None
        elif self.__data[target_name].dtype in ['int64', 'float64']:
            self.__target_type = 'numerical'
        elif self.__data[target_name].dtype in ['object', 'category']:
            self.__target_type = 'categorical'
        else:
            self.__target_type = 'unknown'

        # Update dtypes if requested
        if update_dtypes:
            self.update_dtypes()

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    @property
    def feature_names(self) -> Optional[List[str]]:
        return self.__feature_names

    @property
    def target_name(self) -> Optional[str]:
        return self.__target_name

    @property
    def target_type(self) -> Optional[str]:
        return self.__target_type

    @property
    def shape(self) -> Tuple[int, int]:
        return self.__data.shape

    def update_dtypes(self):
        # Try to automatically update dtypes
        for col in self.__data.columns:
            if self.__data[col].dtype == 'object':
                try:
                    self.__data[col] = pd.to_numeric(self.__data[col])
                except ValueError:
                    pass
            elif self.__data[col].dtype == 'int64':
                self.__data[col] = self.__data[col].astype('float64')

    def create_report(self):
        pass
