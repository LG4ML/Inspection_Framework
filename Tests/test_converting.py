import unittest
from DataHandling import convert_to_numerical, convert_to_datetime, convert_to_boolean
import numpy as np
import pandas as pd
import datetime as dt


class TestConverting(unittest.TestCase):
    def test_numerical_series(self):
        # Test with a pandas Series
        series = pd.Series(['1', '2', '3'])
        result = convert_to_numerical(series)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.tolist(), [1, 2, 3])

    def test_numerical_array(self):
        # Test with a numpy array
        array = np.array(['1', '2', '3'])
        result = convert_to_numerical(array)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.tolist(), [1, 2, 3])

    def test_numerical_list(self):
        # Test with a list
        list_ = ['1', '2', '3']
        result = convert_to_numerical(list_)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1, 2, 3])

    def test_numerical_single(self):
        # Test with a string that cannot be converted
        single = 'a'
        result = convert_to_numerical(single)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'a')

        # Test with a string that can be converted
        single = '1'
        result = convert_to_numerical(single, result='list')
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1])

    def test_numerical_malformed(self):
        # Test with a malformed string
        values = ['1,05', '1.000,02', '1O']
        result = convert_to_numerical(values, result='same')
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1.05, 1000.02, 10])

    def test_datetime_series(self):
        # Test with a pandas Series
        series = pd.Series(['2018-01-01', '2018-01-02', '2018-01-03'])
        result = convert_to_datetime(series)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.tolist(), [dt.datetime(2018, 1, 1), dt.datetime(2018, 1, 2), dt.datetime(2018, 1, 3)])

    def test_boolean_series(self):
        # Test with a pandas Series
        series = pd.Series(['True', 'False', 'True'])
        result = convert_to_boolean(series)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.tolist(), [True, False, True])

    def test_boolean_numbers(self):
        # Test with a pandas Series
        series = pd.Series(['1', '0', '1'])
        result = convert_to_boolean(series)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.tolist(), [True, False, True])

    def test_boolean_not_bool(self):
        # Test with a pandas Series
        series = pd.Series(['1', '2', '3'])
        result = convert_to_boolean(series)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.tolist(), [True, True, True])


if __name__ == '__main__':
    unittest.main()
