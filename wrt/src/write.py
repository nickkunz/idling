## libraries
import os
import sys
import json
import socketio
import psycopg2

## modules
sys.path.insert(0, './')
 
## data source (websocket)
src = 'ws://localhost:4080/'

## data destination (database)
hst = 'localhost'
hst_prt = 5432
sql_pth_evt = './wrt/conf/events.sql'
sql_pth_agc = './wrt/conf/agency.sql'

## read sql file
def read_sql(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return f.read()  ## query contents
    else:
        return ''  ## empty string if file does not exist

## websocket
sio = socketio.Client(
    reconnection = True,
    reconnection_attempts = 3,
    reconnection_delay = 1,
    reconnection_delay_max = 5,
    randomization_factor = 0.5
)

## client interact
@sio.event
def connect():
    print('Client connected to {x}'.format(x = src))

@sio.event
def connect_error():
    print('Client connection error to {x}'.format(x = src))

@sio.event
def disconnect():
    print('Client disconnected from {x}'.format(x = src))

## listen for events
@sio.on('events')
def on_message(json_data):

    ## parse json response
    try:
        data = json.loads(json_data)
        if len(data) == 0:
            print('Client received empty JSON response.')
            return

    except:
        print('Client failed to parse JSON response.')
        

    ## insert idle data into table
    try:
        for i in data:
            query = read_sql(
                path = sql_pth_evt  ## events query file path
            )

            cur.execute(
                query = query,
                vars = (
                    str(i['iata_id']),
                    str(i['vehicle_id']),
                    str(i['trip_id']),
                    str(i['route_id']),
                    float(i['latitude']),
                    float(i['longitude']),
                    str(i['iata_id']),
                    str(i['vehicle_id']),
                    str(i['trip_id']),
                    str(i['route_id']),
                    float(i['latitude']),
                    float(i['longitude']),
                    int(i['datetime']),
                    int(i['duration']),
                    int(i['duration'])
                )
            )

        ## save insert changes
        cnn.commit()
        print('Client wrote to http://{x}:{y}.'.format(
            x = hst,
            y = hst_prt
            )
        )

    ## undo insert attempt
    except:
        cnn.rollback()
        print('Client failed to write to http://{x}:{y}.'.format(
            x = hst,
            y = hst_prt
            )
        )

## connect to database
n_try_db = 3
i = 0
while i < n_try_db:
    try:
        cnn = psycopg2.connect(
            dbname = 'idle',
            user = 'user',
            password = 'pass',
            host = 'localhost',
            port = 5432,
        )
        cur = cnn.cursor()
        print('Client connected to http://{x}:{y}.'.format(
            x = hst,
            y = hst_prt
            )
        )
        break

    except:
        print(
            'Client failed to connect to database. Reconnection attempt {x} of {y}.'.format(
                x = i + 1,
                y = n_try_db
            )
        )
    i += 1

## end reconnect attempts
if i == n_try_db:
    print('Client failed to connect to database. Max retries reached.')
    sys.exit(1)

## create transit agency table
query = read_sql(path = sql_pth_agc) ## transit agency query file path
cur.execute(query = query)
cnn.commit()

## connect to websocket
n_try_ws = 3
i = 0
while i < n_try_ws:
    try:
        sio.connect(
            url = src,
            transports = 'websocket',
            wait_timeout = 120,
            wait = True
        )
        break

    except:
        print('Client failed to connect to {z}. Reconnection attempt {x} of {y}.'.format(
            x = i + 1,
            y = n_try_ws,
            z = src
            )
        )
    i += 1

## end reconnect attempts
if i == n_try_ws:
    print('Client failed to connect to {z}. Max retries reached.'.format(z = src))
    sys.exit(1)

## end of program