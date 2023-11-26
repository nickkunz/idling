## libraries
import os
import sys
import threading
from flask import Flask, Response
from flask_socketio import SocketIO

## source
sys.path.insert(0, './')
from .src.interface import ## placeholder

## params
WS_CONN = str(os.getenv(key = 'WS_CONN'))  ## protobuf data from extract service
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## app
app = Flask(import_name = __name__)

## logging
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
    app.logger.info(msg = 'Client application layer tested sucessfully.')
    return Response(
        response = None,
        status = 200
    )

## buffer and subset
def subset(sio = sio):
    app.logger.info(msg = 'Client application layer started sucessfully.')
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
threading.Thread(target = lambda: subset(sio = sio)).start()

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run()

## end application