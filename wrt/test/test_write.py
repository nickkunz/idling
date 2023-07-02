## libraries
import sys

## modules
sys.path.insert(0, './')
from wrt.src.write import read_sql

## test case 1: valid sql file
sql_pth = './wrt/conf/insert.sql'
assert isinstance(read_sql(path = sql_pth), str) == True

## test case 2: file does not exist
sql_pth = './wrt/conf/demo.sql'
assert read_sql(path = sql_pth) == ''

## test case passed
print("All tests passed!")
