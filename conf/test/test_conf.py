## libraries
import sys
import configparser
import unittest

## modules
sys.path.insert(0, './')
from conf.conf import ini_key, ini_var, env_var


## test ini configs
class TestIniCon(unittest.TestCase):
    def test_ini_key(self):

        ## case args
        file_test = './conf/test/test_conf.ini'
        sect_test = 'test_urls'

        ## case .ini file and case data
        config = configparser.ConfigParser()
        config[sect_test] = {
            'test_url_aaa': 'http://testa',
            'test_url_bbb': 'http://testb',
            'test_url_ccc': 'http://testc'
            }

        with open(file_test, 'w') as configfile:
            config.write(configfile)

        ## test return
        result = ini_key(
            file = file_test, 
            sect = sect_test
        )

        self.assertIsInstance(result, dict)
        self.assertDictEqual(result, {
            'test_url_aaa': 'http://testa',
            'test_url_bbb': 'http://testb',
            'test_url_ccc': 'http://testc'
            }
        )


## test ini variables
class TestIniVar(unittest.TestCase):
    def test_ini_var(self):

        ## case args
        file_test = './conf/test/test_conf.ini'
        sect_test = 'test_urls'

        ## test return
        result = ini_var(
            file = file_test,
            sect = sect_test
        )

        self.assertIsInstance(result, list)
        self.assertEqual([i for i in result], ['aaa', 'bbb', 'ccc'])


## test environ variables
class TestEnvVar(unittest.TestCase):
    def test_env_var(self):

        ## case args
        file_test = './conf/test/test_example.env'

        ## test return
        vars = env_var(
            file = file_test
        )
        
        self.assertIsInstance(vars, dict)
        self.assertEqual(vars['API_KEY_A'], '1')
        self.assertEqual(vars['API_KEY_B'], '2')
        self.assertEqual(vars['API_KEY_C'], '3')


## run test
if __name__ == '__main__':
    unittest.main()
