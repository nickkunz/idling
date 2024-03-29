## libraries
import os
import unittest
import numpy as np
import pandas as pd
from datetime import datetime
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

    def test_null_route_id(self):
        null = self.data[self.data['route_id'].isnull()]
        null_perc = (len(null) / len(self.data)) * 100
        if null_perc == 0:
            print("No missing values in 'route_id' column.")
        else:
            print("{x}% of missing values in 'route_id' column.".format(
                x = round(number = null_perc, ndigits = 2)
                )
            )
        self.assertLessEqual(
            a = null_perc,
            b = 50,
            msg = "The percentage of missing values in 'route_id' column is greater than 50%."
        )

    def test_null_trip_id(self):
        null = self.data[self.data['trip_id'].isnull()]
        null_perc = (len(null) / len(self.data)) * 100
        if null_perc == 0:
            print("No missing values in 'trip_id' column.")
        else:
            print("{x}% of missing values in 'trip_id' column.".format(
                x = round(number = null_perc, ndigits = 2)
                )
            )
        self.assertLessEqual(
            a = null_perc,
            b = 50,
            msg = "The percentage of missing values in 'trip_id' column is greater than 50%."
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
    def __init__(self, data, iata_id = None, iata_path = None, gtfs_path = None, dist_thres = 25,
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
                    df = pd.read_csv(
                        filepath_or_buffer = os.path.join(subdir, i),
                        low_memory = False,
                        dtype = {
                            'vehicle_id': str,
                            'trip_id': str,
                            'route_id': str
                            }
                        )
                    self.shapes_df = pd.concat([self.shapes_df, df])
                elif i == 'trips.txt':
                    df = pd.read_csv(
                        filepath_or_buffer = os.path.join(subdir, i),
                        low_memory = False,
                        dtype = {
                            'vehicle_id': str,
                            'trip_id': str,
                            'route_id': str
                            }
                        )
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

        ## merge idle data with trips data
        self.merged_df = self.data.merge(
            right = self.trips_df[['route_id', 'trip_id', 'shape_id']],
            how = 'left',
            left_on = 'route_id',
            right_on = 'route_id'
        )

        ## when route_id is not available use trip_id
        self.merged_df = self.merged_df.combine_first(
            self.data.merge(
                right = self.trips_df[['trip_id', 'shape_id']],
                how = 'left',
                left_on = 'trip_id',
                right_on = 'trip_id'
            )
        )

        ## drop rows with missing shape_id and clean up
        if len(self.merged_df['shape_id']) == 0:
            return None
        
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
        accuracy = (within_shape / total_events) * 100 if total_events > 0 else None
        return accuracy, total_events

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
        accuracy, _ = self.comp_perc()
        if accuracy is None:
            print("{x} has no matching shape paths.".format(x = self.iata_id))
        else:
            print("{x} percent of idling events outside {y} meter distance threshold: {z}%".format(
                    x = self.iata_id,
                    y = self.dist_thres,
                    z = round(number = 100 - accuracy, ndigits = 2)
                )
            )
            self.assertGreaterEqual(
                a = round(accuracy),
                b = 50,
                msg = "{x} percent of idling events outside {y} meter distance threshold violated: {z}%".format(
                    x = self.iata_id,
                    y = self.dist_thres,
                    z = round(number = 100 - accuracy, ndigits = 2)
                    )
                )

class TestSpatialPointMean(TestSpatialPoint):
    def __init__(self, data = None, iata_path = None, dist_thres = 25, *args, **kwargs):
        super().__init__(data, iata_path, dist_thres, *args, **kwargs)
        self.data = data
        self.iata_path = iata_path
        self.dist_thres = dist_thres

    def shapes_path_loop(self, data, iata_path, dist_thres):
        results = {}
        for iata_id, gtfs_path in iata_path:
            test = TestSpatialPoint(
                data = data,
                iata_id = iata_id,
                gtfs_path = gtfs_path,
                dist_thres = dist_thres,
                methodName = 'test_shapes_path'
            )
            accuracy, total_events = test.comp_perc()
            if accuracy is not None:
                results[iata_id] = {'accuracy': accuracy, 'observations': total_events}
        return results

    def test_shapes_path_mean_unweight(self):
        results = self.shapes_path_loop(
            data = self.data,
            iata_path = self.iata_path
        )
        n_results = len(results)
        mean_unweight = sum(i['accuracy'] for i in results.values()) / n_results if n_results > 0 else None
        if mean_unweight is None:
            print("No matching shape paths found.")
        else:
            print("Mean unweighted spatial point error: {x}%".format(
                x = round(number = 100 - mean_unweight, ndigits = 2)
                )
            )

        self.assertGreaterEqual(
            a = mean_unweight, 
            b = 85,
            msg = "Mean unweight is less than 85"
        )

    def test_shapes_path_mean_weight(self):
        results = self.shapes_path_loop(
            data = self.data,
            iata_path = self.iata_path
        )
        n_results = sum(i['observations'] for i in results.values())
        mean_weight = sum(i['accuracy'] * i['observations'] / n_results for i in results.values())
        if mean_weight is None:
            print("No matching shape paths found.")
        else:
            print("Mean weighted spatial point error: {x}%".format(
                x = round(number = 100 - mean_weight, ndigits = 2)
                )
            )

        self.assertGreaterEqual(
            a = mean_weight,
            b = 85,
            msg = "Weighted sum is less than 85"
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
        datetime_24h = 86400 - 600  ## 10min error tolerance
        datetime_gap = datetime_max - datetime_min

        print("Datetime range from first to last observation:  {x} sec.".format(
            x = datetime_gap
            )
        )

        self.assertGreater(
            a = datetime_gap,
            b = datetime_24h,
            msg = "Datetime difference is not approximately 24 hours."
        )

    def test_datetime_down(self):
        self.data.sort_values(by = 'datetime', inplace = True)
        time_diff = self.data['datetime'].diff().fillna(0)
        max_gap = 60  ## 1 min datetime gap counted as downtime
        time_down = time_diff[time_diff > max_gap]
        time_down_total = time_down.sum()
        time_total = self.data['datetime'].max() - self.data['datetime'].min()
        time_down_perc = (time_down_total / time_total) * 100 if time_total > 0 else None
        
        if time_down_perc is None:
            print("Error in downtime violation.")
        else:
            print("Datetime contiguity downtime: {x}%".format(
                x = round(number = time_down_perc, ndigits = 2)
                )
            )

        self.assertLessEqual(
            a = time_down_perc,
            b = 5,
            msg = "Datetime contiguity downtime violated beyond 5% tolerance."
        )

    def test_datetime_gap(self):
        self.data.sort_values(by = 'datetime', inplace = True)
        time_diff = self.data['datetime'].diff().fillna(0)
        max_gap = 600  ## 10min max gap between new observations
        time_gap = time_diff > max_gap
        time_gap_max = time_diff.max()

        if time_diff.any():
            print("Datetime contiguity maximum gap: {x} sec.".format(
                x = time_gap_max
                )
            )

        self.assertFalse(
            expr = time_gap.any(), 
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
        op_time = self.data.groupby(['agency', 'vehicle_id'])['datetime'].agg(['min', 'max'])
        op_time_min = self.data.sort_values('datetime').groupby(['agency', 'vehicle_id']).first()
        op_time['min'] = op_time['min'] - op_time_min['duration']
        op_time['op_time'] = op_time['max'] - op_time['min']
        
        ## feature mapping
        feat_map = ['iata_id', 'city', 'country', 'region', 'continent']
        for i in feat_map:
            mp = self.data.sort_values('datetime').groupby(['agency', 'vehicle_id'])[i].first()
            op_time[i] = op_time.index.map(mp)

        ## feature order
        op_time = op_time.reset_index()
        feat_ord = [
            'iata_id', 
            'agency', 
            'city', 
            'country',
            'region',
            'continent',
            'vehicle_id',
            'op_time'
        ]
        op_time = op_time[feat_ord]

        ## mean proportion of idle time
        op_time_idx = op_time.set_index(['agency', 'vehicle_id'])['op_time']
        id_time_idx = self.data.groupby(['agency', 'vehicle_id'])['duration'].sum()
        if not op_time_idx.index.duplicated().any() and not id_time_idx.index.duplicated().any():
            id_time_prc = (id_time_idx / op_time_idx)
            id_time_prc = id_time_prc[id_time_prc <= 1] ## remove errors where idling time is greater than operating time
            id_time_avg = round(id_time_prc.mean() * 100, ndigits = 2)

        print("Average proportion of idle time: {x} %".format(
            x = id_time_avg
            )
        )

        ## est 30% to 44% idle time taken from existing studies
        id_time_avg_min = 50  ## +20% of lower bound est 30%
        id_time_avg_max = 64  ## +20% of upper bound est 44%

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

    ## test idle duration average adjusted for longer than 5 min
    def test_duration_avg_adj(self):
        id_five = self.data[self.data['duration'] > 300]  ## 5 min
        op_time = self.data.groupby('vehicle_id')['datetime'].agg(['min', 'max'])
        op_time_min = id_five.sort_values('datetime').groupby('vehicle_id').first()
        op_time['min'] = op_time['min'] - op_time_min['duration']
        op_time['id_time'] = id_five.groupby('vehicle_id')['duration'].sum()
        op_time['op_time'] = op_time['max'] - op_time['min']

        id_time_prc_adj = (id_five.groupby('vehicle_id')['duration'].sum() / op_time['op_time']) * 100
        id_time_prc_adj = round(number = id_time_prc_adj.mean(), ndigits = 2)
        print('Average proportion of idle time longer than 5 minutes: ' + str(id_time_prc_adj) + '%')

        ## est 30% to 44% idle time taken from existing studies
        id_time_prc_adj_min = 30  ## lower bound est 30% (no adjustment)
        id_time_prc_adj_max = 44  ## upper bound est 44% (no adjustment)

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
    # path = '/rdb/test/data/test-data-a.csv'
    # path = '/rdb/test/data/test-data-b.csv'
    path = '/rdb/test/data/test-data-c.csv'
    # path = '/rdb/test/data/test-data-d.csv'
    # path = '/rdb/test/data/test-data-e.csv'
    # path = '/rdb/test/data/test-data-f.csv'
    # path = '/rdb/test/data/test-data-g.csv'

    data = pd.read_csv(
        filepath_or_buffer = cwd + path,
        low_memory = False,
        dtype = {
            'vehicle_id': str,
            'trip_id': str,
            'route_id': str,
            'latitude': float,
            'longitude': float,
            'datetime': int,
            'duration': int
            }
        )
    
    ## force data types
    data['route_id'] = data['route_id'].astype(str)
    data['trip_id'] = data['trip_id'].astype(str)

    ## test suite
    suite = unittest.TestSuite()

    ## data types
    suite.addTest(TestDataType(data, 'test_data_type'))
    suite.addTest(TestDataType(data, 'test_data_type_iata_id'))
    suite.addTest(TestDataType(data, 'test_data_type_agency'))
    suite.addTest(TestDataType(data, 'test_data_type_city'))
    suite.addTest(TestDataType(data, 'test_data_type_country'))
    suite.addTest(TestDataType(data, 'test_data_type_region'))
    suite.addTest(TestDataType(data, 'test_data_type_continent'))
    suite.addTest(TestDataType(data, 'test_data_type_vehicle_id'))
    suite.addTest(TestDataType(data, 'test_data_type_trip_id'))
    suite.addTest(TestDataType(data, 'test_data_type_route_id'))
    suite.addTest(TestDataType(data, 'test_data_type_lat'))
    suite.addTest(TestDataType(data, 'test_data_type_lon'))
    suite.addTest(TestDataType(data, 'test_data_type_datetime'))
    suite.addTest(TestDataType(data, 'test_data_type_duration'))

    ## duplication & missingness
    suite.addTest(TestDuplication(data, 'test_duplicate_cols'))
    suite.addTest(TestDuplication(data, 'test_duplicate_rows'))

    suite.addTest(TestMissingness(data, 'test_null_cols'))
    suite.addTest(TestMissingness(data, 'test_null_iata_id'))
    suite.addTest(TestMissingness(data, 'test_null_iata_data'))
    suite.addTest(TestMissingness(data, 'test_null_agency'))
    suite.addTest(TestMissingness(data, 'test_null_city'))
    suite.addTest(TestMissingness(data, 'test_null_country'))
    suite.addTest(TestMissingness(data, 'test_null_region'))
    suite.addTest(TestMissingness(data, 'test_null_continent'))
    suite.addTest(TestMissingness(data, 'test_null_vehicle_id'))
    suite.addTest(TestMissingness(data, 'test_null_route_id'))
    suite.addTest(TestMissingness(data, 'test_null_trip_id'))
    suite.addTest(TestMissingness(data, 'test_null_route_trip_id'))
    suite.addTest(TestMissingness(data, 'test_null_lat'))
    suite.addTest(TestMissingness(data, 'test_null_lon'))
    suite.addTest(TestMissingness(data, 'test_null_datetime'))
    suite.addTest(TestMissingness(data, 'test_null_duration'))

    ## spatial point accuracy
    suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lat_zero'))
    suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lon_zero'))
    suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lat_max'))
    suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lat_min'))
    suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lon_max'))
    suite.addTest(TestSpatialPoint(data = data, methodName = 'test_lon_min'))

    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'NYC',
    #     gtfs_path = cwd + '/rdb/test/routes/us-east/nyc/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PHL',
    #     gtfs_path = cwd + '/rdb/test/routes/us-east/phl/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'DCA',
    #     gtfs_path = cwd + '/rdb/test/routes/us-east/dca/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'BOS',
    #     gtfs_path = cwd + '/rdb/test/routes/us-east/bos/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PIT',
    #     gtfs_path = cwd + '/rdb/test/routes/us-east/pit/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'LAX',
    #     gtfs_path = cwd + '/rdb/test/routes/us-west/lax/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SFO',
    #     gtfs_path = cwd + '/rdb/test/routes/us-west/sfo/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SAN',
    #     gtfs_path = cwd + '/rdb/test/routes/us-west/san/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SEA',
    #     gtfs_path = cwd + '/rdb/test/routes/us-west/sea/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SMF',
    #     gtfs_path = cwd + '/rdb/test/routes/us-west/smf/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PDX',
    #     gtfs_path = cwd + '/rdb/test/routes/us-west/pdx/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'ATL',
    #     gtfs_path = cwd + '/rdb/test/routes/us-suth/atl/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'MIA',
    #     gtfs_path = cwd + '/rdb/test/routes/us-suth/mia/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'TPA',
    #     gtfs_path = cwd + '/rdb/test/routes/us-suth/tpa/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SDF',
    #     gtfs_path = cwd + '/rdb/test/routes/us-suth/sdf/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'BNA',
    #     gtfs_path = cwd + '/rdb/test/routes/us-suth/bna/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'MSP',
    #     gtfs_path = cwd + '/rdb/test/routes/us-cent/msp/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'STL',
    #     gtfs_path = cwd + '/rdb/test/routes/us-cent/stl/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'MSN',
    #     gtfs_path = cwd + '/rdb/test/routes/us-cent/msn/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'CMH',
    #     gtfs_path = cwd + '/rdb/test/routes/us-cent/cmh/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'DSM',
    #     gtfs_path = cwd + '/rdb/test/routes/us-cent/dsm/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'DEN',
    #     gtfs_path = cwd + '/rdb/test/routes/us-mntn/den/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PHX',
    #     gtfs_path = cwd + '/rdb/test/routes/us-mntn/phx/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SAT',
    #     gtfs_path = cwd + '/rdb/test/routes/us-mntn/sat/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'AUS',
    #     gtfs_path = cwd + '/rdb/test/routes/us-mntn/aus/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # # suite.addTest(TestSpatialPoint(
    # #     data = data,
    # #     iata_id = 'BIL',
    # #     gtfs_path = cwd + '/rdb/test/routes/us-mntn/bil/',
    # #     methodName = 'test_shapes_path'
    # #     )
    # # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YUL',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-east/yul/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YYZ',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-east/yyz/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YHM',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-east/yhm/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YHZ',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-east/yhz/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YQT',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-east/yqt/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YVR',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-west/yvr/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YYC',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-west/yyc/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YEG',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-west/yeg/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'YXE',
    #     gtfs_path = cwd + '/rdb/test/routes/ca-west/yxe/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'AMS',
    #     gtfs_path = cwd + '/rdb/test/routes/eu-west/ams/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'DUB',
    #     gtfs_path = cwd + '/rdb/test/routes/eu-west/dub/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # # ## incomplete test data (invalid mapping route_ids / trip_ids to shape_ids)
    # # suite.addTest(TestSpatialPoint(
    # #     data = data,
    # #     iata_id = 'ARN',
    # #     gtfs_path = cwd + '/rdb/test/routes/eu-west/arn/',
    # #     methodName = 'test_shapes_path'
    # #     )
    # # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'HEL',
    #     gtfs_path = cwd + '/rdb/test/routes/eu-west/hel/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'FCO',
    #     gtfs_path = cwd + '/rdb/test/routes/eu-west/fco/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # # ## incomplete test data (invalid mapping route_ids / trip_ids to shape_ids)
    # # suite.addTest(TestSpatialPoint(
    # #     data = data,
    # #     iata_id = 'WAW',
    # #     gtfs_path = cwd + '/rdb/test/routes/eu-cent/waw/',
    # #     methodName = 'test_shapes_path'
    # #     )
    # # )
    # # ## incomplete test data (invalid mapping route_ids / trip_ids to shape_ids)
    # # suite.addTest(TestSpatialPoint(
    # #     data = data,
    # #     iata_id = 'KRK',
    # #     gtfs_path = cwd + '/rdb/test/routes/eu-cent/krk/',
    # #     methodName = 'test_shapes_path'
    # #     )
    # # )
    # # ## incomplete test data (invalid mapping route_ids / trip_ids to shape_ids)
    # # suite.addTest(TestSpatialPoint(
    # #     data = data,
    # #     iata_id = 'GDN',
    # #     gtfs_path = cwd + '/rdb/test/routes/eu-cent/gdn/',
    # #     methodName = 'test_shapes_path'
    # #     )
    # # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'PRG',
    #     gtfs_path = cwd + '/rdb/test/routes/eu-cent/prg/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'SYD',
    #     gtfs_path = cwd + '/rdb/test/routes/oc-full/syd/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'BNE',
    #     gtfs_path = cwd + '/rdb/test/routes/oc-full/bne/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'ADL',
    #     gtfs_path = cwd + '/rdb/test/routes/oc-full/adl/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'AKL',
    #     gtfs_path = cwd + '/rdb/test/routes/oc-full/akl/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # suite.addTest(TestSpatialPoint(
    #     data = data,
    #     iata_id = 'CHC',
    #     gtfs_path = cwd + '/rdb/test/routes/oc-full/chc/',
    #     methodName = 'test_shapes_path'
    #     )
    # )
    # # ## incomplete test data (no shapes.txt file)
    # # suite.addTest(TestSpatialPoint(
    # #     data = data,
    # #     iata_id = 'DEL',
    # #     gtfs_path = cwd + '/rdb/test/routes/as-full/del/',
    # #     methodName = 'test_shapes_path'
    # #     )
    # # )

    # ## iata id to path mapping
    # iata_path_us_east = (
    #     ('NYC', cwd + '/rdb/test/routes/us-east/nyc/'),
    #     ('PHL', cwd + '/rdb/test/routes/us-east/phl/'),
    #     ('DCA', cwd + '/rdb/test/routes/us-east/dca/'),
    #     ('BOS', cwd + '/rdb/test/routes/us-east/bos/'),
    #     ('PIT', cwd + '/rdb/test/routes/us-east/pit/')
    # )

    # iata_path_us_west = (
    #     ('LAX', cwd + '/rdb/test/routes/us-west/lax/'),
    #     ('SFO', cwd + '/rdb/test/routes/us-west/sfo/'),
    #     ('SAN', cwd + '/rdb/test/routes/us-west/san/'),
    #     ('SEA', cwd + '/rdb/test/routes/us-west/sea/'),
    #     ('SMF', cwd + '/rdb/test/routes/us-west/smf/'),
    #     ('PDX', cwd + '/rdb/test/routes/us-west/pdx/')
    # )

    # iata_path_us_suth = (
    #     ('ATL', cwd + '/rdb/test/routes/us-suth/atl/'),
    #     ('MIA', cwd + '/rdb/test/routes/us-suth/mia/'),
    #     ('TPA', cwd + '/rdb/test/routes/us-suth/tpa/'),
    #     ('SDF', cwd + '/rdb/test/routes/us-suth/sdf/'),
    #     ('BNA', cwd + '/rdb/test/routes/us-suth/bna/')
    # )

    # iata_path_us_cent = (
    #     ('MSP', cwd + '/rdb/test/routes/us-cent/msp/'),
    #     ('STL', cwd + '/rdb/test/routes/us-cent/stl/'),
    #     ('MSN', cwd + '/rdb/test/routes/us-cent/msn/'),
    #     ('CMH', cwd + '/rdb/test/routes/us-cent/cmh/'),
    #     ('DSM', cwd + '/rdb/test/routes/us-cent/dsm/')
    # )

    # iata_path_us_mntn = (
    #     ('DEN', cwd + '/rdb/test/routes/us-mntn/den/'),
    #     ('PHX', cwd + '/rdb/test/routes/us-mntn/phx/'),
    #     ('SAT', cwd + '/rdb/test/routes/us-mntn/sat/'),
    #     ('AUS', cwd + '/rdb/test/routes/us-mntn/aus/')
    #     # ('BIL', cwd + '/rdb/test/routes/us-mntn/bil/')
    # )

    # iata_path_ca_east = (
    #     ('YUL', cwd + '/rdb/test/routes/ca-east/yul/'),
    #     ('YYZ', cwd + '/rdb/test/routes/ca-east/yyz/'),
    #     ('YHM', cwd + '/rdb/test/routes/ca-east/yhm/'),
    #     ('YHZ', cwd + '/rdb/test/routes/ca-east/yhz/'),
    #     ('YQT', cwd + '/rdb/test/routes/ca-east/yqt/')
    # )

    # iata_path_ca_west = (
    #     ('YVR', cwd + '/rdb/test/routes/ca-west/yvr/'),
    #     ('YYC', cwd + '/rdb/test/routes/ca-west/yyc/'),
    #     ('YEG', cwd + '/rdb/test/routes/ca-west/yeg/'),
    #     ('YXE', cwd + '/rdb/test/routes/ca-west/yxe/')
    # )

    # iata_path_eu_west = (
    #     ('AMS', cwd + '/rdb/test/routes/eu-west/ams/'),
    #     # ('ARN', cwd + '/rdb/test/routes/eu-west/arn/'),
    #     ('HEL', cwd + '/rdb/test/routes/eu-west/hel/'),
    #     ('DUB', cwd + '/rdb/test/routes/eu-west/dub/'),
    #     ('FCO', cwd + '/rdb/test/routes/eu-west/fco/')
    # )

    # iata_path_eu_cent = (
    #     # ('WAW', cwd + '/rdb/test/routes/eu-cent/waw/'),
    #     # ('KRK', cwd + '/rdb/test/routes/eu-cent/krk/'),
    #     # ('GDN', cwd + '/rdb/test/routes/eu-cent/gdn/'),
    #     ('PRG', cwd + '/rdb/test/routes/eu-cent/prg/')
    # )

    # iata_path_oceania = (
    #     ('SYD', cwd + '/rdb/test/routes/oc-full/syd/'),
    #     ('BNE', cwd + '/rdb/test/routes/oc-full/bne/'),
    #     ('ADL', cwd + '/rdb/test/routes/oc-full/adl/'),
    #     ('AKL', cwd + '/rdb/test/routes/oc-full/akl/'), 
    #     ('CHC', cwd + '/rdb/test/routes/oc-full/chc/')
    # )

    # # iata_path_asia = (
    # #    ('DEL', cwd + '/rdb/test/routes/as-full/del/')
    # # )

    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_east,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_east,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_west,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_west,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_suth,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_suth,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_cent,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_cent,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_mntn,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_us_mntn,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_ca_east,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_ca_east,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_ca_west,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_ca_west,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_eu_west,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_eu_west,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_eu_cent,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_eu_cent,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_oceania,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path_oceania,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )

    # iata_path = (
    #     ('NYC', cwd + '/rdb/test/routes/us-east/nyc/'),
    #     ('PHL', cwd + '/rdb/test/routes/us-east/phl/'),
    #     ('DCA', cwd + '/rdb/test/routes/us-east/dca/'),
    #     ('BOS', cwd + '/rdb/test/routes/us-east/bos/'),
    #     ('PIT', cwd + '/rdb/test/routes/us-east/pit/'),
    #     ('LAX', cwd + '/rdb/test/routes/us-west/lax/'),
    #     ('SFO', cwd + '/rdb/test/routes/us-west/sfo/'),
    #     ('SAN', cwd + '/rdb/test/routes/us-west/san/'),
    #     ('SEA', cwd + '/rdb/test/routes/us-west/sea/'),
    #     ('SMF', cwd + '/rdb/test/routes/us-west/smf/'),
    #     ('PDX', cwd + '/rdb/test/routes/us-west/pdx/'),
    #     ('ATL', cwd + '/rdb/test/routes/us-suth/atl/'),
    #     ('MIA', cwd + '/rdb/test/routes/us-suth/mia/'),
    #     ('TPA', cwd + '/rdb/test/routes/us-suth/tpa/'),
    #     ('SDF', cwd + '/rdb/test/routes/us-suth/sdf/'),
    #     ('BNA', cwd + '/rdb/test/routes/us-suth/bna/'),
    #     ('MSP', cwd + '/rdb/test/routes/us-cent/msp/'),
    #     ('STL', cwd + '/rdb/test/routes/us-cent/stl/'),
    #     ('MSN', cwd + '/rdb/test/routes/us-cent/msn/'),
    #     ('CMH', cwd + '/rdb/test/routes/us-cent/cmh/'),
    #     ('DSM', cwd + '/rdb/test/routes/us-cent/dsm/'),
    #     ('DEN', cwd + '/rdb/test/routes/us-mntn/den/'),
    #     ('PHX', cwd + '/rdb/test/routes/us-mntn/phx/'),
    #     ('SAT', cwd + '/rdb/test/routes/us-mntn/sat/'),
    #     ('AUS', cwd + '/rdb/test/routes/us-mntn/aus/'),
    #     # ('BIL', cwd + '/rdb/test/routes/us-mntn/bil/'),
    #     ('YUL', cwd + '/rdb/test/routes/ca-east/yul/'),
    #     ('YYZ', cwd + '/rdb/test/routes/ca-east/yyz/'),
    #     ('YHM', cwd + '/rdb/test/routes/ca-east/yhm/'),
    #     ('YHZ', cwd + '/rdb/test/routes/ca-east/yhz/'),
    #     ('YQT', cwd + '/rdb/test/routes/ca-east/yqt/'),
    #     ('YVR', cwd + '/rdb/test/routes/ca-west/yvr/'),
    #     ('YYC', cwd + '/rdb/test/routes/ca-west/yyc/'),
    #     ('YEG', cwd + '/rdb/test/routes/ca-west/yeg/'),
    #     ('YXE', cwd + '/rdb/test/routes/ca-west/yxe/'),
    #     ('AMS', cwd + '/rdb/test/routes/eu-west/ams/'),
    #     # ('ARN', cwd + '/rdb/test/routes/eu-west/arn/'),
    #     ('HEL', cwd + '/rdb/test/routes/eu-west/hel/'),
    #     ('DUB', cwd + '/rdb/test/routes/eu-west/dub/'),
    #     ('FCO', cwd + '/rdb/test/routes/eu-west/fco/'),
    #     # ('WAW', cwd + '/rdb/test/routes/eu-cent/waw/'),
    #     # ('KRK', cwd + '/rdb/test/routes/eu-cent/krk/'),
    #     # ('GDN', cwd + '/rdb/test/routes/eu-cent/gdn/'),
    #     ('PRG', cwd + '/rdb/test/routes/eu-cent/prg/'),
    #     ('SYD', cwd + '/rdb/test/routes/oc-full/syd/'),
    #     ('BNE', cwd + '/rdb/test/routes/oc-full/bne/'),
    #     ('ADL', cwd + '/rdb/test/routes/oc-full/adl/'),
    #     ('AKL', cwd + '/rdb/test/routes/oc-full/akl/'),
    #     ('CHC', cwd + '/rdb/test/routes/oc-full/chc/')
    #     # ('DEL', cwd + '/rdb/test/routes/as-full/del/')
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path,
    #     methodName = 'test_shapes_path_mean_unweight'
    #     )
    # )
    # suite.addTest(TestSpatialPointMean(
    #     data = data,
    #     iata_path = iata_path,
    #     methodName = 'test_shapes_path_mean_weight'
    #     )
    # )

    ## temporal contiguity
    suite.addTest(TestDateTime(data, 'test_datetime_zero'))
    suite.addTest(TestDateTime(data, 'test_datetime_neg'))
    suite.addTest(TestDateTime(data, 'test_datetime_24h'))
    suite.addTest(TestDateTime(data, 'test_datetime_down'))
    suite.addTest(TestDateTime(data, 'test_datetime_gap'))

    ## duration expectation
    suite.addTest(TestDuration(data, 'test_duration_zero'))
    suite.addTest(TestDuration(data, 'test_duration_neg'))
    suite.addTest(TestDuration(data, 'test_duration_avg'))
    suite.addTest(TestDuration(data, 'test_duration_avg_adj'))

    ## conduct tests
    runner = unittest.TextTestRunner()
    runner.run(suite)

    ## other info
    print('Number of observations: ' + str(len(data)))
    print('Percentage of missing observations: ' + str(round((data.isnull().sum().sum() / data.size * 100), 2)) + '%')
    print('Date range of observations: ' + \
        str(datetime.utcfromtimestamp(data['datetime'].min()).strftime('%Y-%m-%d %H:%M:%S')) + ' to ' + \
        str(datetime.utcfromtimestamp(data['datetime'].max()).strftime('%Y-%m-%d %H:%M:%S'))
    )