import unittest
import pandas as pd
from pathlib import Path
from DataHandling import load_tabular_like_file


class TestLoading(unittest.TestCase):
    def test_load_covid_data(self):
        result = load_tabular_like_file('../data/Covid_Data.csv')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (52429, 21))

    def test_load_cycling_data(self):
        result = load_tabular_like_file('../data/Cycling_Data.csv')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (624, 28))

    def test_load_passenger_data(self):
        result = load_tabular_like_file('../data/Passenger_Stats.csv')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (15007, 17))

    def test_load_song_data(self):
        path = Path('../data/Radio_Songs.csv')
        result = load_tabular_like_file(path)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (2918, 4))

    def test_load_wine_data(self):
        path = Path('../data/Wine_Malformed.csv')
        result = load_tabular_like_file(path, separator=';')
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.shape, (4898, 5))
