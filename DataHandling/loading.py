import itertools
from pathlib import Path
from typing import Union, Optional
import pandas as pd

ENCODINGS = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'ascii']
SEPARATORS = [',', ';', '\t', '|']
DECIMALS = [',', '.']


def load_tabular_like_file(path: Union[str, Path], encoding: str = None, separator: str = None,
                           decimal: str = None, index_col: Union[str, int] = None) -> pd.DataFrame:
    """
    Loads the data from the given path into a Pandas DataFrame.

    The function automatically detects the file format and loads the data accordingly. If the file format is not
    supported, the function will raise a ValueError. Furthermore, corrupted files will be solved as far as possible.

    :param path: Path to the data file as string or Path object.
    :param encoding: Encoding of the data file. If None, the function will try to detect the encoding.
    :param separator: Separator of the data file. If None, the function will try to detect the separator.
    :param decimal: Decimal separator of the data file. If None, the function will try to detect the decimal separator.
    :param index_col: Column to use as index for the DataFrame. If None, no column will be used as index.
    :raise: ValueError if the file format is not supported.
    :raise: FileNotFoundError if the file does not exist.
    :return: Pandas DataFrame with the loaded data.
    """
    # Check if the given path is a string or a Path object
    if not isinstance(path, Path):
        path = Path(path)

    # Check if the given path exists
    if not path.exists():
        raise FileNotFoundError(f'The given path {path} does not exist.')

    # Check if the given path is a file
    if not path.is_file():
        raise ValueError(f'The given path {path} is not a file.')

    # Check if the given path is a csv file
    if path.suffix.lower() in ['.csv', '.txt']:
        data = load_csv_like_file(path=path, encoding=encoding, separator=separator,
                                  decimal=decimal, index_col=index_col)
        if data is None:
            raise ValueError(f'The given file {path} is not a valid csv or txt file.')
        return data

    # Check if the given path is an Excel file
    elif path.suffix.lower() in ['.xlsx', '.xls', '.xlsm']:
        data = load_excel_file(path=path, index_col=index_col)
        if data is None:
            raise ValueError(f'The given file {path} is not a valid excel file.')
        return data

    # Raise an error if the file format is not supported
    else:
        raise ValueError(f'The given file format {path.suffix} is currently not supported.')


def load_csv_like_file(path: Path, encoding: str = None, separator: str = None,
                       decimal: str = None, index_col: Union[str, int] = None) -> Optional[pd.DataFrame]:
    """
    Loads a csv or txt file into a Pandas DataFrame.

    The function automatically detects the encoding, separator and decimal separator of the file. If the file could not
    be loaded, the function will return None.

    :param path: Path to the data file as string or Path object.
    :param encoding: Encoding of the data file. If None, the function will try to detect the encoding.
    :param separator: Separator of the data file. If None, the function will try to detect the separator.
    :param decimal: Decimal separator of the data file. If None, the function will try to detect the decimal separator.
    :param index_col: Column to use as index for the DataFrame. If None, no column will be used as index.
    :return: Pandas DataFrame with the loaded data or None if the file could not be loaded.
    """
    # Initialize an empty DataFrame
    data = None

    # Use the given parameters to load the data
    try:
        data = pd.read_csv(path, encoding=encoding, sep=separator,
                           decimal=decimal if decimal is not None else '.',
                           index_col=index_col)
        return data
    except Exception:
        pass

    # If the loading fails, try to detect the encoding, separator and decimal separator
    for enc, sep, dec in itertools.product(ENCODINGS, SEPARATORS, DECIMALS):
        try:
            data = pd.read_csv(path, encoding=enc, sep=sep, decimal=dec)
            return data
        except Exception:
            pass

    return data


def load_excel_file(path: Path, index_col: Union[str, int] = None) -> Optional[pd.DataFrame]:
    """
    Loads an Excel file into a Pandas DataFrame.

    :param path: Path to the data file as string or Path object.
    :param index_col: Column to use as index for the DataFrame. If None, no column will be used as index.
    :return: Pandas DataFrame with the loaded data or None if the file could not be loaded.
    """
    # Initialize an empty DataFrame
    data = None

    # Use the given parameters to load the data
    try:
        data = pd.read_excel(path, index_col=index_col)
    except Exception:
        pass

    return data
