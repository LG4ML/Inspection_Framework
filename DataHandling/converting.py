import copy
import datetime as dt
import itertools
from typing import Union, List, Tuple
import numpy as np
import pandas as pd


def __cast_input_values(values: Union[pd.Series, np.ndarray, List[str]]) \
        -> Tuple[pd.Series, str]:
    """
    Casts the input values to a pandas Series and returns them.

    :param values: Values to cast.
    :return: Values as a pandas Series and the input format.
    """
    # Cast the values to a pandas Series if necessary
    if isinstance(values, pd.Series):
        return values, 'series'
    elif isinstance(values, np.ndarray):
        return pd.Series(values), 'array'
    elif isinstance(values, list):
        return pd.Series(values), 'list'
    elif isinstance(values, (str, int, float)):
        return pd.Series([values]), 'single'
    else:
        raise TypeError('Invalid type of values.')


def __return_values(original_values: Union[pd.Series, np.ndarray, List[str], str, int, float],
                    transformed_values: Union[pd.Series, np.ndarray, List[str], str, int, float],
                    result: str,
                    input_format: str) \
        -> Union[pd.Series, np.ndarray, List[str], str, int, float]:
    """
    Transforms the transformed values to the desired format and returns them. If the transformation fails, the original
    values are returned. The result parameter specifies the format of the returned values. If result is 'series', a
    pandas Series is returned. If result is 'array', a numpy array is returned. If result is 'list', a list is returned.
    If result is 'same', the values are returned in the same format as the input.

    :param original_values: Values to return if the transformation failed.
    :param transformed_values: Values to return if the transformation succeeded.
    :param result: Format of the returned values. Has to be one of 'series', 'array', 'list' or 'same'.
    :param input_format: Format of the input values. Has to be one of 'series', 'array', 'list' or 'single'.
    :return: Values in the desired format or the original values if the transformation failed.
    """
    # If the conversion was successful, transform the values to the desired format
    if transformed_values is not None:
        if result == 'series' or (result == 'same' and input_format == 'series'):
            return transformed_values
        elif result == 'array' or (result == 'same' and input_format == 'array'):
            return transformed_values.values
        elif result == 'list' or (result == 'same' and input_format == 'list'):
            return transformed_values.tolist()
        elif result == 'same' and input_format == 'single':
            return transformed_values[0]
    else:
        return original_values


def convert_to_datetime(values: Union[pd.Series, np.ndarray, List[str]],
                        fmt: str = None,
                        result: str = 'same') \
        -> Union[pd.Series, np.ndarray, List[dt.datetime]]:
    """
    Converts the values to datetime format and returns them in the same format as the input. If the conversion fails,
    the original values are returned. The format of the datetime string is specified by the fmt parameter. If fmt is
    None, the function tries to infer the format automatically. The result parameter specifies the format of the
    returned values. If result is 'series', a pandas Series is returned. If result is 'array', a numpy array is
    returned. If result is 'list', a list is returned. If result is 'same', the values are returned in the same format
    as the input.

    :param values: Values to convert to datetime format.
    :param fmt: Optional format of the datetime string. If None, the format is inferred automatically.
    :param result: Format of the returned values. Has to be one of 'series', 'array', 'list' or 'same'.
    :return: Values in datetime format or the original values if the conversion fails.
    """
    # Check if the result parameter is valid
    assert result in ['series', 'array', 'list', 'same'], 'Invalid result parameter.'

    # Get the input format and transform the values to a pandas Series if necessary
    original_values = copy.deepcopy(values)
    values, input_format = __cast_input_values(values)

    # Create an empty variable to store the converted values
    transformed_values = None

    # Try to convert the values to datetime format using the Pandas to_datetime function with different settings
    settings = itertools.product([None, fmt], [True, False])
    for fmt, infer_datetime_format in settings:
        try:
            transformed_values = pd.to_datetime(values, format=fmt, infer_datetime_format=infer_datetime_format)
            break
        except pd.errors.ParserError:
            pass
        except ValueError:
            pass
    try:
        transformed_values = pd.to_datetime(values)
    except pd.errors.ParserError:
        pass
    except ValueError:
        pass

    # Return the values in the desired format
    return __return_values(original_values, transformed_values, result, input_format)


def __replace_multiple_decimal_separators(value: str) \
        -> str:
    """
    Replaces multiple decimal separators with a single decimal separator and returns the result.

    :param value: Value to replace the decimal separators.
    :return: Transformed value.
    """
    # Split the value at the decimal separator and join the parts again with a single decimal separator
    if value.count('.') > 1:
        splits = value.split('.')
        value = ''.join(splits[:-1]) + '.' + splits[-1]

    # Return the transformed value
    return value


def convert_to_numerical(values: Union[pd.Series, np.ndarray, List[str]],
                         result: str = 'same') \
        -> Union[pd.Series, np.ndarray, List[float]]:
    """
    Converts the values to numerical format and returns them in the same format as the input. If the conversion fails,
    the original values are returned. The result parameter specifies the format of the returned values. If result is
    'series', a pandas Series is returned. If result is 'array', a numpy array is returned. If result is 'list', a
    list is returned. If result is 'same', the values are returned in the same format as the input.

    :param values: Values to convert to numerical format.
    :param result: Format of the returned values. Has to be one of 'series', 'array', 'list' or 'same'.
    :return: Values in numerical format or the original values if the conversion fails.
    """
    # Check if the result parameter is valid
    assert result in ['series', 'array', 'list', 'same'], 'Invalid result parameter.'

    # Get the input format and transform the values to a pandas Series if necessary
    original_values = copy.deepcopy(values)
    values, input_format = __cast_input_values(values)

    # Replace any commas with a dot and replace O with 0
    values = values.str.replace(',', '.').str.replace('O', '0')

    # Create an empty variable to store the converted values
    transformed_values = None

    # Try to convert the values to numerical format using the Pandas to_numeric function
    try:
        transformed_values = pd.to_numeric(values)
    except ValueError:
        pass

    # Try to remove multiple commas or dots and convert the values to numerical format
    if transformed_values is None:
        try:
            transformed_values = pd.to_numeric(values.apply(__replace_multiple_decimal_separators))
        except ValueError:
            pass

    # Return the values in the desired format
    return __return_values(original_values, transformed_values, result, input_format)


def convert_to_boolean(values: Union[pd.Series, np.ndarray, List[str]],
                       result: str = 'same') \
        -> Union[pd.Series, np.ndarray, List[float]]:
    # Check if the result parameter is valid
    assert result in ['series', 'array', 'list', 'same'], 'Invalid result parameter.'

    # Get the input format and transform the values to a pandas Series if necessary
    original_values = copy.deepcopy(values)
    values, input_format = __cast_input_values(values)

    # Create an empty variable to store the converted values
    transformed_values = None

    # Try to convert the values to boolean format using the Pandas to_numeric function
    try:
        transformed_values = pd.to_numeric(values).astype(bool)
    except ValueError:
        pass

    # Try to map the values to boolean format
    if transformed_values is None:
        try:
            transformed_values = values.apply(lambda x: bool(x))
        except ValueError:
            pass

    # Return the values in the desired format
    return __return_values(original_values, transformed_values, result, input_format)
