## libraries
import os
import unittest
import pandas as pd
from datetime import datetime

## test data
class TestData(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestData, self).__init__(*args, **kwargs)

        ## load data
        cwd = os.getcwd()
        self.data = pd.read_csv(filepath_or_buffer = cwd + '/rdb/test/test-data-1.csv')

    ## test meta data
    def test_meta_data(self):
        print('Number of observations: ' + str(len(self.data)))
        print('Date range of observations: ' + \
            str(datetime.utcfromtimestamp(self.data['datetime'].min()).strftime('%Y-%m-%d %H:%M:%S')) + ' to ' + \
            str(datetime.utcfromtimestamp(self.data['datetime'].max()).strftime('%Y-%m-%d %H:%M:%S'))
        )
    
    ## test duplicates
    def test_dups(self):
        dup_obs = self.data[self.data.duplicated()]
        self.assertFalse(
            expr = dup_obs.empty,
            msg = "Duplicate observations found. \n {x}.".format(
                x = dup_obs
            )
        )

    ## test columns
    def test_feat(self):
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
        true_iata_ids = set((
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
        )
        data_iata_ids = set(self.data['iata_id'].unique())
        self.assertEqual(
            first = data_iata_ids,
            second = true_iata_ids,
            msg = "Not all values found in 'iata_id' column."
        )

    ## test vehicle ids
    def test_vehicle_ids(self):
        self.assertFalse(
            expr = self.data['vehicle_id'].isnull().any(), 
            msg = "There are missing values in the 'vehicle_id' column"
        )

    ## test route ids and trip ids
    def test_route_trip_ids(self):
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
    def test_datetime_null(self):
        time_null = self.data['datetime'].isnull()
        self.assertFalse(
            expr = time_null.any(), 
            msg = "There are missing values in the 'datetime' column"
        )

    def test_datetime(self):
        self.data.sort_values(by = 'datetime', inplace = True)
        time_diff = self.data['datetime'].diff().fillna(0)
        max_gap = 600  ## 10 min max gap between new observations
        time_gaps = time_diff > max_gap
        self.assertFalse(
            expr = time_gaps.any(), 
            msg = "Time contiguity violated."
        )

    ## test duration
    def test_duration_null(self):
        dura_null = self.data['duration'].isnull()
        self.assertFalse(
            expr = dura_null.any(),
            msg = "Missing observations in 'duration' column."
        )

    def test_duration_zero(self):
        zero_vals = self.data['duration'].eq(0)
        self.assertFalse(
            expr = zero_vals.any(),
            msg = "Zero values found in 'duration' column."
        )

    def test_dura_neg(self):
        neg_int = self.data['duration'] < 0
        self.assertFalse(
            expr = neg_int.any(),
            msg = "Negative values found in 'duration' column."
        )

    def test_duration_int(self):
        not_int = self.data['duration'].map(lambda x: not float(x).is_integer())
        self.assertFalse(
            expr = not_int.any(),
            msg = "Non-integer values found in 'duration' column."
        )

    def test_duration_avg(self):
        op_time = self.data.groupby('vehicle_id')['datetime'].agg(['min', 'max'])
        op_time_min = self.data.sort_values('datetime').groupby('vehicle_id').first()
        op_time['min'] = op_time['min'] - op_time_min['duration']
        op_time['id_time'] = self.data.groupby('vehicle_id')['duration'].sum()
        op_time['op_time'] = op_time['max'] - op_time['min']

        id_time_prc = (self.data.groupby('vehicle_id')['duration'].sum() / op_time['op_time']) * 100
        id_time_avg = round(id_time_prc.mean())
        print('Average proportion of idle time: ' + str(id_time_avg) + '%')

        id_time_avg_min = 15  ## -15% of lower bound est 30%
        id_time_avg_max = 60  ## +15% of lower bound est 45%

        self.assertGreaterEqual(
            a = id_time_avg,
            b = id_time_avg_min,
            msg = "Average percentage of idle time is less than {x} %.".format(
                x = id_time_avg_min
            )
        )
        self.assertLessEqual(
            a = id_time_avg,
            b = id_time_avg_max,
            msg = "Average percentage of idle time is greater than {x} %.".format(
                x = id_time_avg_max
            )
        )

## run tests
if __name__ == '__main__':
    unittest.main()
