## libraries
import os
import sys
import threading
from flask import Flask, Response
from flask_socketio import SocketIO

## modules
sys.path.insert(0, './')
from .src.subset import find_idle

## params
URL_DATA = str(os.getenv('URL_DATA'))
R_PARAM = int(os.getenv('R_PARAM'))
H_PARAM = int(os.getenv('H_PARAM'))
M_PARAM = int(os.getenv('M_PARAM'))

## app and websocket
app = Flask(__name__)
sio = SocketIO(
    app = app,
    cors_allowed_origins = '*'
)

## test route
@app.route(rule = '/', methods = ['GET'])
def test():
    return Response(
        response = None,
        status = 200
    )

## buffer and subset
def subset(sio = sio):
    for i in find_idle(  ## iter thro generator
        url = URL_DATA,
        time_r = R_PARAM,
        time_h = H_PARAM,
        move_m = M_PARAM,
        ):

        # emit data to client thro websocket
        sio.emit(
            event = 'idle',  ## listen for events titled "idle"
            data = i,
        )

## process thread
threading.Thread(target = lambda: subset(sio = sio)).start()

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run(
#         debug = LocalEnv.DEBUG,
#         host = LocalEnv.URL,
#         port = 8000
#     )