## libraries
import os
import sys
import logging
from flask import Flask, Response

## source
sys.path.insert(0, './')
from .src.write import WriteClient

## params
WS_HOST = str(os.getenv(key = 'WS_HOST'))
if WS_HOST is None:
    raise ValueError('Missing environment variable: WS_HOST.')

DB_NAME = str(os.getenv(key = 'DB_NAME', default = 'idle'))
DB_USER = str(os.getenv(key = 'DB_USER', default = 'user'))
DB_PASS = str(os.getenv(key = 'DB_PASS', default = 'pass'))
DB_HOST = str(os.getenv(key = 'DB_HOST', default = 'database'))
DB_PORT = int(os.getenv(key = 'DB_PORT', default = 5432))
SQL_INIT = str(os.getenv(key = 'SQL_INIT', default = './wrt/conf/sql/init.sql'))
SQL_AGENCY = str(os.getenv(key = 'SQL_AGENCY', default = './wrt/conf/sql/agency.sql'))
SQL_EVENTS = str(os.getenv(key = 'SQL_EVENTS', default = './wrt/conf/sql/events.sql'))
LOG_LEVEL = str(os.getenv(key = 'LOG_LEVEL', default = 'INFO'))

## app
app = Flask(import_name = __name__)

## logging
app.logger.setLevel(level = LOG_LEVEL)
app.logger.propagate = False
app.debug = True if LOG_LEVEL == 'DEBUG' else False

##client instance
client = WriteClient(
    ws_host = WS_HOST,
    db_name = DB_NAME,
    db_user = DB_USER,
    db_pswd = DB_PASS,
    db_host = DB_HOST,
    db_port = DB_PORT,
    sql_init = SQL_INIT,
    sql_agency = SQL_AGENCY,
    sql_events = SQL_EVENTS
)

## test app
@app.route(rule = '/', methods = ['GET'])
def test():
    app.logger.info(msg = 'Client application layer tested sucessfully.')
    return Response(
        response = None,
        status = 200
    )

## write websocket data to database
@app.route(rule = '/write', methods = ['GET'])
def write():
    client.run()
    app.logger.info(msg = 'Client application layer started sucessfully.')
    return Response(
        response = 'Write application started. Beginning to write to database.',
        status = 200
    )

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run()

## end application