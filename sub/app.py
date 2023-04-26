## libraries
import sys
import threading
from flask import Flask, Response
from flask_socketio import SocketIO

## modules
sys.path.insert(0, './')
from .src.subset import find_idle
from conf.environ import LocalEnv

## app and socket
app = Flask(__name__)
sio = SocketIO(
    app = app,
    cors_allowed_origins = '*'
)

## test route
@app.route('/', methods = ['GET'])
def test():
    return Response(status = 200)

## buffer and subset data
@app.route('/subset', methods = ['GET'])
def subset(sio = sio):

    ## iter thro generator
    for i in find_idle(
        url = 'http://extract:6080/extract',
        time_h = 1,
        move_m = 10,
        time_r = 30
        ):

        # emit data thro websocket
        sio.emit(
            event = 'events',  ## listen for messages titled "events"
            data = i,
        )

## process thread
threading.Thread(target = lambda: subset(sio = sio)).start()

## run app (does not run with gunicorn)
# if __name__ == '__main__':
#     app.run(
#         debug = LocalEnv.DEBUG,
#         host = LocalEnv.URL,
#         port = 8000
#     )