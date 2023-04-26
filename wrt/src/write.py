## libraries 
import sys
import json
import socketio
import psycopg2

## end point
src = 'ws://localhost:4080/'
hst = 'localhost'
hst_prt = 5432

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

    except:
        print('Client failed to parse JSON response.')

    ## insert data into the table
    try:
        for i in data:
            cur.execute(
                query = """
                WITH j AS (
                    SELECT * FROM idle
                    WHERE vehicle_id = %s
                    AND trip_id = %s
                    AND route_id = %s
                    AND latitude = %s
                    AND longitude = %s
                    ORDER BY duration DESC
                    LIMIT 1
                )
                INSERT INTO idle (
                    vehicle_id,
                    trip_id,
                    route_id,
                    latitude,
                    longitude,
                    datetime,
                    duration
                )
                SELECT %s, %s, %s, %s, %s, %s, %s
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM j
                )
                OR %s > COALESCE((SELECT duration FROM j), 0)
                ON CONFLICT (
                    vehicle_id,
                    trip_id,
                    route_id,
                    latitude,
                    longitude
                )
                DO UPDATE SET duration = EXCLUDED.duration
                WHERE idle.duration < EXCLUDED.duration;
                """,

                vars = (
                    str(i['vehicle_id']),
                    str(i['trip_id']),
                    str(i['route_id']),
                    float(i['latitude']),
                    float(i['longitude']),
                    str(i['vehicle_id']),
                    str(i['trip_id']),
                    str(i['route_id']),
                    float(i['latitude']),
                    float(i['longitude']),
                    int(i['datetime']),
                    int(i['duration']),
                    int(i['duration']),
                )
            )

        ## save insert changes
        cnn.commit()
        print('Client wrote to database.')

    ## undo insert attempt
    except:
        cnn.rollback()
        print("Client failed to write to database.")

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
        print("Client connected to database.")
        break

    except:
        print(
            'Client failed to connect to database. Attempt {x} of {y}.'.format(
                x = i + 1,
                y = n_try_db
            )
        )
    i += 1

## end reconnect attempts
if i == n_try_db:
    print('Client failed to connect to database. Max retries reached.')
    sys.exit(1)

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
        print('Client failed to connect to {z}. Attempt {x} of {y}.'.format(
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