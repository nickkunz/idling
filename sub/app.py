## libraries
import os
import sys
import threading
from flask import Flask, Response, request, abort
from flask_socketio import SocketIO

## source
sys.path.insert(0, './')
from .src.subset import find_idle

## params
PB_DATA = str(os.getenv(key = 'PB_DATA', default = 'http://extract:8080/extract'))
R_PARAM = int(os.getenv(key = 'R_PARAM', default = 30))  ## request rate (seconds)
H_PARAM = int(os.getenv(key = 'H_PARAM', default = 1))  ## time-horizon (interval)
M_PARAM = int(os.getenv(key = 'M_PARAM', default = 10))  ## append limit (constant)
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## app
app = Flask(import_name = __name__)

## logging
app.logger.propagate = False
app.logger.setLevel(level = LOG_LEVEL)
app.debug = True if LOG_LEVEL == 'DEBUG' else False

## websocket
sio = SocketIO(
    app = app,
    cors_allowed_origins = '*'
)

## test app
@app.route(rule = '/', methods = ['GET'])
def test():
    if request.args:
        abort(code = 400, text = 'Application does not accept parameters.')
    app.logger.info(msg = 'Application layer tested sucessfully.')
    return Response(response = None, status = 200)

## buffer and subset
def subset(sio = sio):
    app.logger.info(msg = 'Application layer started sucessful.')
    for i in find_idle(  ## iter thro gen obj
        url = PB_DATA,
        time_r = R_PARAM,
        time_h = H_PARAM,
        move_m = M_PARAM
        ):

        ## client data stream
        sio.emit(
            event = 'events',  ## listen for event titled "events"
            data = i  ## send data
        )

## process thread
thread = threading.Thread(target = lambda: subset(sio = sio))
thread.start()

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run()

## end application