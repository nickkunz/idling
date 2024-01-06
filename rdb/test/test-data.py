## libraries
import os
import unittest
import pandas as pd

## test data
class TestData(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestData, self).__init__(*args, **kwargs)

        ## load data
        cwd = os.getcwd()
        self.data = pd.read_csv(filepath_or_buffer = cwd + '/rdb/test/test-data.csv')

    ## test rows
    def test_length(self):
        print('Number of observations: ' + str(len(self.data)))

    ## test columns
    def test_columns(self):
        true_columns = (
            'iata_id', 'agency', 'city', 'country', 'region', 'continent', 
            'vehicle_id', 'trip_id', 'route_id', 'latitude', 'longitude', 
            'datetime', 'duration'
        )
        data_columns = tuple(self.data.columns)
        
        self.assertEqual(
            first = data_columns, 
            second = true_columns, 
            msg = "Not all columns found"
        )
    
    ## test iata ids
    def test_iata_ids(self):
        true_iata_ids = (
            'NYC', 'PHL', 'DCA', 'BOS', 'PIT',
            'LAX', 'SFO', 'SAN', 'SEA', 'SMF', 'PDX',
            'ATL', 'MIA', 'TPA', 'SDF', 'BNA',
            'MSP', 'STL', 'MSN', 'CMH', 'DSM',
            'DEN', 'PHX', 'SAT', 'BIL', 'AUS',
            'YUL', 'YYZ', 'YHM', 'YHZ', 'YQT',
            'YVR', 'YYC', 'YEG', 'YXE',
            'AMS', 'ARN', 'HEL', 'DUB', 'FCO',
            'WAW', 'KRK', 'GDN', 'PRG',
            'SYD', 'BNE', 'ADL', 'AKL', 'CHC',
            'DEL'
        )
        data_iata_ids = set(self.data['iata_id'].unique())
        
        self.assertEqual(
            first = data_iata_ids, 
            second = set(true_iata_ids), 
            msg = "Not all values found in 'iata_id' column"
        )

    ## test vehicle ids
    def test_vehicle_ids(self):
        self.assertFalse(
            expr = self.data['vehicle_id'].isnull().any(), 
            msg = "There are missing values in the 'vehicle_id' column"
        )

    ## test route ids and trip ids
    def test_route_ids_trip_ids(self):
        both_null = self.data[self.data['route_id'].isnull() & self.data['trip_id'].isnull()]
        
        self.assertTrue(
            expr = both_null.empty, 
            msg = "Observations are missing both 'route_id' and 'trip_id'."
        )

    ## test geocoords
    def test_geocoords(self):
        lat_null = self.data['latitude'].isnull()
        lon_null = self.data['longitude'].isnull()

        lat_not_float = self.data['latitude'].map(lambda x: not isinstance(x, float))
        lon_not_float = self.data['longitude'].map(lambda x: not isinstance(x, float))

        self.assertFalse(
            expr = lat_null.any(), 
            msg = "Missing observations in 'latitude' column."
        )
        self.assertFalse(
            expr = lon_null.any(), 
            msg = "Missing observations in 'longitude' column."
        )
        self.assertFalse(
            expr = lat_not_float.any(), 
            msg = "Non-float values found in 'latitude' column."
        )
        self.assertFalse(
            expr = lon_not_float.any(), 
            msg = "Non-float values found in 'longitude' column."
        )

    ## test datetime
    def test_datetime(self):
        self.data.sort_values(by = 'datetime', inplace = True)
        time_null = self.data['datetime'].isnull()
        time_diff = self.data['datetime'].diff().fillna(0)
        max_gap = 60 * 5  ## 5min max gap between observations
        time_gaps = time_diff > max_gap
        
        self.assertFalse(
            expr = time_null.any(), 
            msg = "There are missing values in the 'datetime' column"
        )
        self.assertFalse(
            expr = time_gaps.any(), 
            msg = "Time contiguity violated."
        )

    ## test duration
    def test_duration(self):
        dura_null = self.data['duration'].isnull()
        neg_int = self.data['duration'] <= 0
        not_int = self.data['duration'].map(lambda x: not float(x).is_integer())

        self.assertFalse(
            expr = dura_null.any(), 
            msg = "Missing observations in 'duration' column."
        )
        self.assertFalse(
            expr = neg_int.any(), 
            msg = "Negative values found in 'duration' column."
        )
        self.assertFalse(
            expr = not_int.any(), 
            msg = "Non-integer values found in 'duration' column."
        )

## run tests
if __name__ == '__main__':
    unittest.main()