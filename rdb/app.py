## libraries
import os
import sys
from flask import Flask, Response, request, abort, jsonify

## source
sys.path.insert(0, './')
from .src.read import ReadClient, InvalidParameterError

## const
DB_NAME = str(os.getenv(key = 'DB_NAME', default = 'idle'))
DB_USER = str(os.getenv(key = 'DB_USER', default = 'user'))
DB_PASS = str(os.getenv(key = 'DB_PASS', default = 'pass'))
DB_HOST = str(os.getenv(key = 'DB_HOST', default = 'database'))
DB_PORT = int(os.getenv(key = 'DB_PORT', default = 5432))
LOG_LEVEL = str(os.getenv(key = 'LOG_LEVEL', default = 'INFO'))

## app
app = Flask(import_name = __name__)

## logging
app.logger.propagate = False
app.logger.setLevel(level = LOG_LEVEL)
app.debug = True if LOG_LEVEL == 'DEBUG' else False

## error handlers
@app.errorhandler(InvalidParameterError)
def parameter_error(error):
    return jsonify({'error': str(error)}), 422

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'error': 'Invalid URL or parameters'}), 400

@app.errorhandler(Exception)
def handle_exception(error):
    return jsonify({'error': 'Unexpected error'}), 500

## client instance
client = ReadClient(
    db_name = DB_NAME,
    db_user = DB_USER,
    db_pswd = DB_PASS,
    db_host = DB_HOST,
    db_port = DB_PORT
)

## test app
@app.route(rule = '/', methods = ['GET'])
def test():
    if request.args:
        abort(code = 400, text = 'Application test does not accept parameters.')
    app.logger.info(msg = 'Application layer tested sucessfully.')
    return Response(response = None, status = 200)

## query agency table
@app.route('/agency', methods = ['GET'])
def agency():
    params = request.args.to_dict()
    format = params.pop('format', 'geojson')  ## default 'json' response
    app.logger.info(msg = 'Application layer sucessfully queried agency table.')
    return client(table = 'agency', params = params, format = format)

## query events table
@app.route('/events', methods = ['GET'])
def events():
    params = request.args.to_dict()
    format = params.pop('format', 'geojson')  ## default 'geojson' response
    app.logger.info(msg = 'Application layer sucessfully queried events table.')
    return client(table = 'events', params = params, format = format)

## query table join of events and agency
@app.route('/idle', methods = ['GET'])
def idle():
    params = request.args.to_dict()
    format = params.pop('format', 'geojson')  ## default 'geojson' response
    app.logger.info(msg = 'Application layer sucessfully queried idle table.')
    return client(table = 'idle', params = params, format = format)

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run()

## end application