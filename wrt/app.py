## libraries
import os
import sys
import threading
from flask import Flask, Response, request, abort

## source
sys.path.insert(0, './')
from .src.write import WriteClient

## params
WS_HOST = str(os.getenv(key = 'WS_HOST', default = 'http://subset:7080'))
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
app.logger.propagate = False
app.logger.setLevel(level = LOG_LEVEL)
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

## background thread flag
service_running = threading.Event()

## test app
@app.route(rule = '/', methods = ['GET'])
def test():
    if request.args:
        abort(code = 400, text = 'Application test does not accept parameters.')
    app.logger.info(msg = 'Application tested sucessfully.')
    return Response(response = None, status = 200)

## write websocket data to database
@app.route(rule = '/write', methods = ['GET'])
def write():
    if request.args:
        abort(code = 400, text = 'Application does not accept parameters.')
    if service_running.is_set():
        app.logger.warning('Application is already running.')
        return Response(
            response = 'Application is already running.',
            status = 200
        )

    def start_service():
        app.logger.info('Application starting as a background thread.')
        client.run()

    service_thread = threading.Thread(target = start_service, daemon = True)
    service_thread.start()
    service_running.set()

    app.logger.info(msg = 'Application started sucessfully.')
    return Response(
        response = 'Application started sucessfully. Writing to database...',
        status = 200
    )

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run()

## end application