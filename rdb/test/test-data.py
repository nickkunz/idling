## libraries
import os
import unittest
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
import concurrent.futures

## test data
class TestData(unittest.TestCase):
    def __init__(self, data, *args, **kwargs):
        super(TestData, self).__init__(*args, **kwargs)
        self.data = data

## test data types
class TestDataType(TestData):
    def test_data_type(self):
        self.assertTrue(
            expr = isinstance(self.data, pd.DataFrame),
            msg = "Data was not correctly imported as a DataFrame."
        )

    def test_data_type_iata_id(self):
        self.assertTrue(
            expr = self.data['iata_id'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'iata_id' column are of string data type."
        )

    def test_data_type_agency(self):
        self.assertTrue(
            expr = self.data['agency'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'agency' column are of string data type."
        )

    def test_data_type_city(self):
        self.assertTrue(
            expr = self.data['city'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'city' column are of string data type."
        )

    def test_data_type_country(self):
        self.assertTrue(
            expr = self.data['country'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'country' column are of string data type."
        )

    def test_data_type_region(self):
        self.assertTrue(
            expr = self.data['region'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'region' column are of string data type."
        )

    def test_data_type_continent(self):
        self.assertTrue(
            expr = self.data['continent'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'continent' column are of string data type."
        )

    def test_data_type_vehicle_id(self):
        self.assertTrue(
            expr = self.data['vehicle_id'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'vehicle_id' column are of string data type."
        )

    def test_data_type_route_id(self):
        self.assertTrue(
            expr = self.data['route_id'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'route_id' column are of string data type."
        )

    def test_data_type_trip_id(self):
        self.assertTrue(
            expr = self.data['trip_id'].apply(lambda x: isinstance(x, str)).all(),
            msg = "Not all values in 'trip_id' column are of string data type."
        )

    def test_data_type_lat(self):
        self.assertTrue(
            expr = self.data['latitude'].apply(lambda x: isinstance(x, float)).all(),
            msg = "Not all values in 'latitude' column are of float data type."
        )

    def test_data_type_lon(self):
        self.assertTrue(
            expr = self.data['longitude'].apply(lambda x: isinstance(x, float)).all(),
            msg = "Not all values in 'longitude' column are of float data type."
        )

    def test_data_type_datetime(self):
        self.assertTrue(
            expr = self.data['datetime'].apply(lambda x: isinstance(x, int)).all(),
            msg = "Not all values in 'datetime' column are of integer data type."
        )
    
    def test_data_type_duration(self):
        self.assertTrue(
            expr = self.data['duration'].apply(lambda x: isinstance(x, int)).all(),
            msg = "Not all values in 'duration' column are of integer data type."
        )

## test duplication
class TestDuplication(TestData):
    def test_duplicate_cols(self):
        data_columns = self.data.columns
        self.assertEqual(
            first = len(data_columns),
            second = len(set(data_columns)),
            msg = "Not all fields / features (columns) are unique."
        )

    def test_duplicate_rows(self):
        dup_obs = self.data[self.data.duplicated()]
        self.assertTrue(
            expr = dup_obs.empty,
            msg = "Not all observations (rows) are unique: {x}.".format(
                x = dup_obs
            )
        )

## test missingnesss
class TestMissingness(TestData):
    def test_null_cols(self):
        true_columns = (
            'iata_id', 'agency', 'city', 'country', 'region', 'continent', 
            'vehicle_id', 'trip_id', 'route_id', 'latitude', 'longitude', 
            'datetime', 'duration'
        )

        data_columns = tuple(self.data.columns)
        self.assertEqual(
            first = data_columns,
            second = true_columns,
            msg = "Found missing fields / features (columns)."
        )

    def test_null_iata_id(self):
        self.assertFalse(
            expr = self.data['iata_id'].isnull().any(), 
            msg = "Found missing values in 'iata_id' column."
        )

    def test_null_iata_data(self):
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
            msg = "Not all data sources were found in 'iata_id' column."
        )

    def test_null_agency(self):
        self.assertFalse(
            expr = self.data['agency'].isnull().any(),
            msg = "Found missing values in 'agency' column."
        )

    def test_null_city(self):
        self.assertFalse(
            expr = self.data['city'].isnull().any(),
            msg = "Found missing values in 'city' column."
        )

    def test_null_country(self):
        self.assertFalse(
            expr = self.data['country'].isnull().any(),
            msg = "Found missing values in 'country' column."
        )

    def test_null_region(self):
        self.assertFalse(
            expr = self.data['region'].isnull().any(),
            msg = "Found missing values in 'region' column."
        )

    def test_null_continent(self):
        self.assertFalse(
            expr = self.data['continent'].isnull().any(),
            msg = "Found missing values in 'continent' column."
        )

    def test_null_vehicle_id(self):
        self.assertFalse(
            expr = self.data['vehicle_id'].isnull().any(),
            msg = "There are missing values in the 'vehicle_id' column."
        )

    def test_null_route_trip_id(self):
        both_null = self.data[self.data['route_id'].isnull() & self.data['trip_id'].isnull()]
        self.assertTrue(
            expr = both_null.empty, 
            msg = "There are missing values in both 'route_id' and 'trip_id'."
        )

    def test_null_lat(self):
        lat_null = self.data['latitude'].isnull()
        self.assertFalse(
            expr = lat_null.any(),
            msg = "Missing observations in 'latitude' column."
        )

    def test_null_lon(self):
        lon_null = self.data['longitude'].isnull()
        self.assertFalse(
            expr = lon_null.any(),
            msg = "Missing observations in 'longitude' column."
        )

    def test_null_datetime(self):
        time_null = self.data['datetime'].isnull()
        self.assertFalse(
            expr = time_null.any(),
            msg = "Missing values in the 'datetime' column"
        )

    def test_null_duration(self):
        time_null = self.data['duration'].isnull()
        self.assertFalse(
            expr = time_null.any(),
            msg = "Found missing values in 'duration' column."
        )

## test spatial point accuracy
class TestSpatialPoint(TestData):
    def __init__(self, data, iata_id = None, gtfs_path = None, dist_thres = 30,
        methodName = 'runTest'):
        super(TestSpatialPoint, self).__init__(data, methodName)
        self.iata_id = iata_id
        self.gtfs_path = gtfs_path
        self.dist_thres = dist_thres
        self.shapes_df = pd.DataFrame()
        self.trips_df = pd.DataFrame()

        ## load gtfs data only if path is provided
        if gtfs_path:  
            self.load_gtfs()
            self.prep_data()
            self.grow_tree()

    @staticmethod
    def deg_per_meter(lat_radians):
        return 1 / (111.32 * 1000 * np.cos(lat_radians))  # 111.32 km is 1 deg of lat

    def load_gtfs(self):
        for subdir, dirs, files in os.walk(self.gtfs_path):
            for i in files:
                if i == 'shapes.txt':
                    df = pd.read_csv(os.path.join(subdir, i))
                    self.shapes_df = pd.concat([self.shapes_df, df])
                elif i == 'trips.txt':
                    df = pd.read_csv(os.path.join(subdir, i))
                    self.trips_df = pd.concat([self.trips_df, df])

        ## omit duplicates
        self.shapes_df.drop_duplicates(inplace = True)
        self.trips_df.drop_duplicates(inplace = True)

    ## merge idle data with trips data
    def prep_data(self):

        ## filter by iata_id, *strictly* required 
        ## (avoids mismatching route_ids across transit agencies)
        if self.iata_id:
            if isinstance(self.iata_id, str):
                self.data = self.data[self.data['iata_id'] == self.iata_id]
            elif isinstance(self.iata_id, list):
                self.data = self.data[self.data['iata_id'].isin(self.iata_id)]

        ## force string data types on route and trip ids
        self.data.loc[:, 'route_id'] = self.data['route_id'].astype(str)
        self.data.loc[:, 'trip_id'] = self.data['trip_id'].astype(str)
        self.trips_df.loc[:, 'route_id'] = self.trips_df['route_id'].astype(str)
        self.trips_df.loc[:, 'trip_id'] = self.trips_df['trip_id'].astype(str)

        ## merge idle data with trips data
        self.merged_df = self.data.merge(
            right=self.trips_df[['route_id', 'trip_id', 'shape_id']],
            how='left',
            left_on='route_id',
            right_on='route_id'
        )

        # In cases where route_id is not available, use trip_id
        self.merged_df = self.merged_df.combine_first(
            self.data.merge(
                right=self.trips_df[['trip_id', 'shape_id']],
                how='left',
                left_on='trip_id',
                right_on='trip_id'
            )
        )

        self.merged_df.dropna(subset = ['shape_id'], inplace = True)

        ## use float32 to save memory, optimize speed
        self.shapes_df[['shape_pt_lat', 'shape_pt_lon']] = self.shapes_df[ 
            ['shape_pt_lat', 'shape_pt_lon']
        ].astype(np.float32)

        self.merged_df[['latitude', 'longitude']] = self.merged_df[
            ['latitude', 'longitude']
        ].astype(np.float32)

        ## calculate distance threshold in degrees
        avg_lat = np.radians(self.merged_df['latitude'].mean())
        deg_per_met_lat = self.deg_per_meter(avg_lat)
        self.dist_thres_deg = self.dist_thres * deg_per_met_lat

    ## build kdtree for each shape path
    def grow_tree(self):
        self.shapes_df['shape_pt_lat'], self.shapes_df['shape_pt_lon'] = map(
            np.radians, [self.shapes_df['shape_pt_lat'], self.shapes_df['shape_pt_lon']]
        )
        self.shape_kdtrees = {
            shape_id: KDTree(shape_pt[['shape_pt_lat', 'shape_pt_lon']].to_numpy()) 
                for shape_id, shape_pt in self.shapes_df.groupby('shape_id')
        }

    ## prepare data for parallel processing
    def prep_para(self, shape_id, idle_pt):
        tree = self.shape_kdtrees[shape_id]
        idle_pt_coord = idle_pt[['latitude', 'longitude']].apply(np.radians).to_numpy()
        counts = tree.query_radius(idle_pt_coord, r = self.dist_thres_deg, count_only = True)
        return len(idle_pt), np.sum(counts > 0)

    ## compute spatial point accuracy
    def comp_perc(self):
        total_events = 0
        within_shape = 0

        ## percentage of idle events within distance threshold
        with concurrent.futures.ThreadPoolExecutor() as thread:
            results = thread.map(lambda x: self.prep_para(*x), self.merged_df.groupby('shape_id'))
        for total, within_dist_thres in results:
            total_events += total
            within_shape += within_dist_thres
        return (within_shape / total_events) * 100 if total_events > 0 else 0

    ## test spatial points
    def test_lat_zero(self):
        lat_zero = self.data['latitude'].eq(0)
        self.assertFalse(
            expr = lat_zero.any(),
            msg = "There are zero values in the 'latitude' column"
        )

    def test_lon_zero(self):
        lon_zero = self.data['longitude'].eq(0)
        self.assertFalse(
            expr = lon_zero.any(),
            msg = "There are zero values in the 'longitude' column"
        )

    def test_lat_max(self):
        lat_max = self.data['latitude'].gt(90)
        self.assertFalse(
            expr = lat_max.any(),
            msg = "There are latitude values greater than 90 degrees."
        )
    
    def test_lat_min(self):
        lat_min = self.data['latitude'].lt(-90)
        self.assertFalse(
            expr = lat_min.any(),
            msg = "There are latitude values less than -90 degrees."
        )
    
    def test_lon_max(self):
        lon_max = self.data['longitude'].gt(180)
        self.assertFalse(
            expr = lon_max.any(),
            msg = "There are longitude values greater than 180 degrees."
        )

    def test_lon_min(self):
        lon_min = self.data['longitude'].lt(-180)
        self.assertFalse(
            expr = lon_min.any(),
            msg = "There are longitude values less than -180 degrees."
        )

    def test_shapes_path(self):
        within_shape_perc = round(self.comp_perc())
        print("{x} percent of idling events within {y} meter threshold: {z}%".format(
                x = self.iata_id,
                y = self.dist_thres,
                z = round(within_shape_perc)
            )
        )
        self.assertGreaterEqual(
            a = within_shape_perc,
            b = 85,
            msg = "{x} percent of idling events within {y} meter threshold violated: {z}%".format(
                x = self.iata_id,
                y = self.dist_thres,
                z = round(within_shape_perc)
            )
        )

## test temporal contiguity
class TestDateTime(TestData):
    def test_datetime_zero(self):
        time_zero = self.data['datetime'].eq(0)
        self.assertFalse(
            expr = time_zero.any(),
            msg = "There are zero values in the 'datetime' column"
        )

    def test_datetime_neg(self):
        time_neg = self.data['datetime'] < 0
        self.assertFalse(
            expr = time_neg.any(),
            msg = "Negative values found in 'datetime' column."
        )

    def test_datetime_24h(self):
        datetime_min = self.data['datetime'].min()
        datetime_max = self.data['datetime'].max()
        datetime_24h = 86400 - 600  ## 24hrs, 10min error tolerance
        datetime_gap = datetime_max - datetime_min

        self.assertGreater(
            a = datetime_gap,
            b = datetime_24h,
            msg = "Datetime difference is not approximately 24 hours."
        )

    def test_datetime_gap(self):
        self.data.sort_values(by = 'datetime', inplace = True)
        time_diff = self.data['datetime'].diff().fillna(0)
        max_gap = 600  ## 10min max gap between new observations
        time_gaps = time_diff > max_gap

        self.assertFalse(
            expr = time_gaps.any(), 
            msg = "Datetime time contiguity violated beyond 10 minutes."
        )

## test duration expectation
class TestDuration(TestData):
    def test_duration_zero(self):
        time_zero = self.data['duration'].eq(0)
        self.assertFalse(
            expr = time_zero.any(),
            msg = "Found zero values in 'duration' column."
        )

    def test_duration_neg(self):
        time_neg = self.data['duration'] < 0
        self.assertFalse(
            expr = time_neg.any(),
            msg = "Found negative values in 'duration' column."
        )

    ## test idle duration average
    def test_duration_avg(self):
        op_time = self.data.groupby('vehicle_id')['datetime'].agg(['min', 'max'])
        op_time_min = self.data.sort_values('datetime').groupby('vehicle_id').first()
        op_time['min'] = op_time['min'] - op_time_min['duration']
        op_time['id_time'] = self.data.groupby('vehicle_id')['duration'].sum()
        op_time['op_time'] = op_time['max'] - op_time['min']

        id_time_prc = (self.data.groupby('vehicle_id')['duration'].sum() / op_time['op_time']) * 100
        id_time_avg = round(id_time_prc.mean())
        print('Average proportion of idle time: ' + str(id_time_avg) + '%')

        ## est 30% to 45% idle time taken from existing studies
        id_time_avg_min = 15  ## -15% of lower bound est 30%
        id_time_avg_max = 60  ## +15% of upper bound est 45%

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

    ## test idle duration average adjusted for 5 min or longer
    def test_duration_avg_adj(self):
        id_five = self.data[self.data['duration'] >= 300]  ## 5 min
        op_time = self.data.groupby('vehicle_id')['datetime'].agg(['min', 'max'])
        op_time_min = id_five.sort_values('datetime').groupby('vehicle_id').first()
        op_time['min'] = op_time['min'] - op_time_min['duration']
        op_time['id_time'] = id_five.groupby('vehicle_id')['duration'].sum()
        op_time['op_time'] = op_time['max'] - op_time['min']

        id_time_prc_adj = (id_five.groupby('vehicle_id')['duration'].sum() / op_time['op_time']) * 100
        id_time_prc_adj = round(id_time_prc_adj.mean())
        print('Average proportion of idle time 5 minutes or longer: ' + str(id_time_prc_adj) + '%')

        ## est 30% to 45% idle time taken from existing studies
        id_time_prc_adj_min = 30  ## lower bound est 30% (no adjustment)
        id_time_prc_adj_max = 45  ## upper bound est 45% (no adjustment)

        self.assertGreaterEqual(
            a = id_time_prc_adj,
            b = id_time_prc_adj_min,
            msg = "Average percentage of idle time is less than {x} %.".format(
                x = id_time_prc_adj_min
            )
        )
        self.assertLessEqual(
            a = id_time_prc_adj,
            b = id_time_prc_adj_max,
            msg = "Average percentage of idle time is greater than {x} %.".format(
                x = id_time_prc_adj_max
            )
        )

## run tests
if __name__ == '__main__':

    ## load test data
    cwd = os.getcwd()
    data = pd.read_csv(filepath_or_buffer = cwd + '/rdb/test/data/test-data-c.csv')

    ## pre-process data
    data['trip_id'] = data['trip_id'].astype(str)
    data['route_id'] = data['route_id'].astype(str)

    ## test suite
    suite = unittest.TestSuite()

    ## data types
    # suite.addTest(TestDataType(data, 'test_data_type'))
    # suite.addTest(TestDataType(data, 'test_data_type_iata_id'))
    # suite.addTest(TestDataType(data, 'test_data_type_agency'))
    # suite.addTest(TestDataType(data, 'test_data_type_city'))
    # suite.addTest(TestDataType(data, 'test_data_type_country'))
    # suite.addTest(TestDataType(data, 'test_data_type_region'))
    # suite.addTest(TestDataType(data, 'test_data_type_continent'))
    # suite.addTest(TestDataType(data, 'test_data_type_vehicle_id'))
    # suite.addTest(TestDataType(data, 'test_data_type_trip_id'))
    # suite.addTest(TestDataType(data, 'test_data_type_route_id'))
    # suite.addTest(TestDataType(data, 'test_data_type_lat'))
    # suite.addTest(TestDataType(data, 'test_data_type_lon'))
    # suite.addTest(TestDataType(data, 'test_data_type_datetime'))
    # suite.addTest(TestDataType(data, 'test_data_type_duration'))

    # ## duplication & missingness
    # suite.addTest(TestDuplication(data, 'test_duplicate_cols'))
    # suite.addTest(TestDuplication(data, 'test_duplicate_rows'))

    # suite.addTest(test=  TestMissingness(data, 'test_null_cols'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_agency'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_city'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_country'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_region'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_continent'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_vehicle_id'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_route_trip_id'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_lat'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_lon'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_datetime'))
    # suite.addTest(test=  TestMissingness(data, 'test_null_duration'))

    # ## spatial point accuracy
    # suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lat_zero'))
    # suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lon_zero'))
    # suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lat_max'))
    # suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lat_min'))
    # suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lon_max'))
    # suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lon_min'))
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'NYC',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-east/nyc/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PHL',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-east/phl/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'DCA',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-east/dca/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'BOS',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-east/bos/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PIT',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-east/pit/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'LAX',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-west/lax/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SFO',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-west/sfo/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SAN',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-west/san/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SEA',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-west/sea/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SMF',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-west/smf/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PDX',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-west/pdx/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'ATL',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-suth/atl/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'MIA',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-suth/mia/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'TPA',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-suth/tpa/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SDF',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-suth/sdf/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'BNA',
    #     gtfs_path = cwd + '/rdb/test/shapes/us-suth/bna/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    suite.addTest(TestSpatialPoint(
        data = data,
        iata_id = 'MSP',
        gtfs_path = cwd + '/rdb/test/shapes/us-cent/msp/',
        methodName = 'test_shapes_path'
        )
    )
    suite.addTest(TestSpatialPoint(
        data = data,
        iata_id = 'STL',
        gtfs_path = cwd + '/rdb/test/shapes/us-cent/stl/',
        methodName = 'test_shapes_path'
        )
    )
    ## temporal contiguity
    # suite.addTest(TestDateTime(data, 'test_datetime_zero'))
    # suite.addTest(TestDateTime(data, 'test_datetime_neg'))
    # suite.addTest(TestDateTime(data, 'test_datetime_24h'))
    # suite.addTest(TestDateTime(data, 'test_datetime_gap'))

    # ## duration expectation
    # suite.addTest(TestDuration(data, 'test_duration_zero'))
    # suite.addTest(TestDuration(data, 'test_duration_neg'))
    # suite.addTest(TestDuration(data, 'test_duration_avg'))
    # suite.addTest(TestDuration(data, 'test_duration_avg_adj'))

    ## conduct tests
    runner = unittest.TextTestRunner()
    runner.run(suite)

    print('Number of observations: ' + str(len(data)))
    # print('Percentage of missing data: ' + str(round((data.isnull().sum().sum() / data.size * 100), 2)) + '%')
    # print('Date range of observations: ' + \
    #     str(datetime.utcfromtimestamp(data['datetime'].min()).strftime('%Y-%m-%d %H:%M:%S')) + ' to ' + \
    #     str(datetime.utcfromtimestamp(data['datetime'].max()).strftime('%Y-%m-%d %H:%M:%S'))
    # )