## libraries
import sys
import unittest

## modules
sys.path.insert(0, './')
from conf.environ import DevEnv, LocalEnv

## local machine tests
class TestLocalEnv(unittest.TestCase):

    def debug(self):
        self.assertTrue(LocalEnv.DEBUG)

    def logging(self):
        self.assertFalse(LocalEnv.LOGGING)

    def localhost(self):
        self.assertEqual(LocalEnv.URL, 'localhost')

## dev env tests
class TestDevEnv(unittest.TestCase):
    
    def debug(self):
        self.assertTrue(DevEnv.DEBUG)

    def logging(self):
        self.assertFalse(DevEnv.LOGGING)

## run test
if __name__ == '__main__':
    unittest.main()
