## libraries
import os
import re
import unittest

## params
data = './ext/test/data/test_data.txt'

## test data
class TestData(unittest.TestCase):
    def __init__(self, data, *args, **kwargs):
        super(TestData, self).__init__(*args, **kwargs)
        self.data = data

## test missingness
class TestMissingness(TestData):
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
        ))

        ## regex to match labels: <iata_id>
        label_pattern = re.compile(r'label:\s*"([A-Z]+)"')

        ## extract iata ids from test data
        data_iata_ids = set()
        for line in self.data:
            match = label_pattern.search(line)
            if match:
                data_iata_ids.add(match.group(1))

        ## test missing iata ids
        missing_iata_ids = true_iata_ids - data_iata_ids
        self.assertTrue(
            not missing_iata_ids,
            msg = f"Missing IATA IDs in 'label' field: {missing_iata_ids}"
        )

## run tests
if __name__ == '__main__':
    
    ## load test data
    cwd = os.getcwd()
    file_path = os.path.join(cwd, data)
    with open(file_path, 'r') as f:
        text_data = f.readlines()

    ## define test suite
    suite = unittest.TestSuite()
    suite.addTest(TestMissingness(text_data, 'test_null_iata_data'))

    ## conduct tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
