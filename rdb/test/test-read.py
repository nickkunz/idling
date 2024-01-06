import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, './')
from rdb.src.read import ReadClient

class TestReadClient(unittest.TestCase):

    def setUp(self):
        self.client = ReadClient(
            db_name='test_db',
            db_user='test_user',
            db_pswd='test_pass',
            db_host='test_host',
            db_port='test_port'
        )

    def test_db_conn(self):
        with patch('psycopg2.connect') as mock_connect:
            self.client.db_conn()
            mock_connect.assert_called_once_with(
                database='test_db',
                user='test_user',
                password='test_pass',
                host='test_host',
                port='test_port'
            )

    def test_to_geojson(self):
        data = [
            [
                "TransLink (British Columbia)",
                "Vancouver",
                "North America",
                "Canada",
                1703810633,
                300,
                "YVR",
                "Canada West",
                "6705",
                "13589077",
                "7482",
                -122.87535095214844,
                49.20391845703125
            ],
            [
                "Delhi Transport Corporation (DTC)",
                "Delhi",
                "Asia",
                "India",
                1703810700,
                300,
                "DEL",
                "Asia",
                "10107",
                "10107_21_6",
                "DL1PD3067",
                77.33116149902344,
                28.684406280517578
            ]
        ]
        feat = {
            'type': 'Feature',
            'properties': {
                'agency': 0,
                'city': 1,
                'continent': 2,
                'country': 3,
                'datetime': 4,
                'duration': 5,
                'iata_id': 6,
                'region': 7,
                'route_id': 8,
                'trip_id': 9,
                'vehicle_id': 10
            },
            'geometry': {'type': 'Point', 'coordinates': [None, None]}
        }
        result = self.client.to_geojson(data, feat)
        self.assertEqual(result['type'], 'FeatureCollection')
        self.assertEqual(len(result['features']), 2)

if __name__ == '__main__':
    unittest.main()