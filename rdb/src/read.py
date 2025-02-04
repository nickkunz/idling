## libraries
import os
import time
import copy
import logging
import psycopg2
import flask

## params
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## logging
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdlr = logging.StreamHandler()
hdlr.setFormatter(fmt = fmt)
logging.basicConfig(level = LOG_LEVEL, handlers = [hdlr])
logger = logging.getLogger(name = __name__)
logger.propagate = True

## error handling
class DatabaseConnectionError(Exception):
    pass

class InvalidParameterError(Exception):
    pass

## client to database
class ReadClient():
    def __init__(self,
                 db_name, db_user, db_pswd, db_host, db_port,
                 recon_tries = 3, recon_delay = 1, recon_timeo = 60):

        self.db_name = db_name
        self.db_user = db_user
        self.db_pswd = db_pswd
        self.db_host = db_host
        self.db_port = db_port
        self.recon_tries = recon_tries
        self.recon_delay = recon_delay
        self.recon_timeo = recon_timeo

    ## connect to database
    def db_conn(self):
        if hasattr(self, 'connect') and self.connect.closed == 0:
            logger.info(msg = 'Database connection already exists.')
            return
        i = 0
        while i < self.recon_tries:
            try:
                self.connect = psycopg2.connect(
                    database = self.db_name,
                    user = self.db_user,
                    password = self.db_pswd,
                    host = self.db_host,
                    port = self.db_port,
                    connect_timeout = self.recon_timeo
                )
                self.connect.set_session(readonly = True)  ## enforce read-only mode
                logger.info(msg = 'Client successfully connected to database in read only mode.')
                break
            except psycopg2.OperationalError as e:
                logger.error(msg = 'Client failed to connect to database. Reconnection attempt {x} of {y}: {z}.'.format(
                        x = i + 1,
                        y = self.recon_tries,
                        z = e
                    )
                )
                if i == self.recon_tries - 1:
                    raise
                else:
                    time.sleep(self.recon_delay)
                    i += 1
        if i == self.recon_tries:
            logger.error(msg = 'Client failed to connect to database. Max number of reconnection attempts reached.')
            raise DatabaseConnectionError('Client failed to connect to database. Max number of reconnection attempts reached.')

    ## geojson encoder
    def to_geojson(self, data, feat):
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        for i in data:
            feat_copy = copy.deepcopy(feat)
            feat_copy['properties'] = {k: i[v] for k, v in feat_copy['properties'].items()}
            feat_copy['geometry']['coordinates'] = [i[-3], i[-4]]  ## lon, lat
            geojson["features"].append(feat_copy)
        return geojson

    ## csv encoder
    def to_csv(self, data, headers):
        if not data:
            return None
        
        ## build csv data
        if headers:
            csv_data = [headers] + [list(i) for i in data]
        else:
            csv_data = [list(i) for i in data]
        csv = '\n'.join([','.join(map(str, i)) for i in csv_data])

        ## build http response
        response = flask.Response(response = csv, mimetype = 'text/csv')
        response.headers.set('Content-Disposition', 'attachment', filename = 'idle.csv')
        return response

    ## query database
    def __call__(self, table, params, format):

        ## validate table
        table_valid = ['agency', 'events', 'idle']
        if table not in table_valid:
            raise ValueError('Invalid table: {x}.'.format(x = table))

        ## validate format
        format_valid = ['geojson', 'csv']
        if format not in format_valid:
            raise InvalidParameterError('Invalid parameter value: {x}'.format(x = format))

        ## connect database
        self.db_conn()

        ## return geojson
        if format == 'geojson':
            try:
                if table == 'agency':
                    query, values = self.agency_query(params)
                    data = self.db_read(query = query, values = values)
                    return flask.jsonify(data or {'message': 'No data found.'})

                elif table == 'events':
                    query, values = self.events_query(params)
                    data = self.db_read(query = query, values = values)
                    if isinstance(data, flask.Response):
                        return data
                    feat = {
                        'type': 'Feature',
                        'properties': {
                            'iata_id': 0,
                            'vehicle_id': 1,
                            'trip_id': 2,
                            'route_id': 3,
                            'datetime': -2,
                            'duration': -1
                        },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [None, None]  ## replaced in to_geojson()
                        }
                    }
                    data = self.to_geojson(data = data, feat = feat)
                    return flask.jsonify(data or {'message': 'No data found.'})

                elif table == 'idle':
                    query, values = self.idle_query(params)
                    data = self.db_read(query = query, values = values)
                    if isinstance(data, flask.Response):
                        return data
                    feat = {
                        'type': 'Feature',
                        'properties': {
                            'iata_id': 0,
                            'agency': 1,
                            'city': 2,
                            'country': 3,
                            'region': 4,
                            'continent': 5,
                            'vehicle_id': 6,
                            'trip_id': 7,
                            'route_id': 8,
                            'datetime': -2,
                            'duration': -1
                        },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [None, None]  ## replaced in to_geojson()
                        }
                    }
                    data = self.to_geojson(data = data, feat = feat)
                    return flask.jsonify(data or {'message': 'No data found.'})

            ## handle errors
            except Exception as e:
                logger.exception(
                    'Client encountered an error while building query: {x}.'.format(x = e)
                )
                raise

            ## close database connection
            finally:
                self.db_close()

        ## return csv
        if format == 'csv':
            try:
                if table == 'agency':
                    query, values = self.agency_query(params)
                    data = self.db_read(query = query, values = values)

                    ## *strict* order of headers
                    headers = [
                        'iata_id',
                        'agency',
                        'city',
                        'country',
                        'region',
                        'continent'
                    ]
                    return self.to_csv(data = data, headers = headers)

                elif table == 'events':
                    query, values = self.events_query(params)
                    data = self.db_read(query = query, values = values)
                    if isinstance(data, flask.Response):
                        return data

                    ## *strict* order of headers
                    headers = [
                        'iata_id',
                        'vehicle_id',
                        'trip_id',
                        'route_id',
                        'latitude',
                        'longitude',
                        'datetime',
                        'duration'
                    ]
                    return self.to_csv(data = data, headers = headers)

                elif table == 'idle':
                    query, values = self.idle_query(params)
                    data = self.db_read(query = query, values = values)
                    if isinstance(data, flask.Response):
                        return data

                    ## *strict* order of headers
                    headers = [
                        'iata_id',
                        'agency',
                        'city',
                        'country',
                        'region',
                        'continent',
                        'vehicle_id',
                        'trip_id',
                        'route_id',
                        'latitude',
                        'longitude',
                        'datetime',
                        'duration'
                    ]
                    return self.to_csv(data = data, headers = headers)

            ## handle errors
            except Exception as e:
                logger.exception(
                    'Client encountered an error while building query: {x}.'.format(x = e)
                )
                raise

            ## close database connection
            finally:
                self.db_close()

    ## execute query
    def db_read(self, query, values):
        with self.connect.cursor() as cur:
            try:
                cur.execute("SET statement_timeout = 300000") ## statement timeout to 5 mins
                cur.execute(query, values)
                data = cur.fetchall()

                ## return csv data when accept header received
                if flask.request.headers.get('Accept') == 'text/csv':
                    return self.to_csv(data = data, headers = None)
                else:
                    return data  ## no accept header received
            except Exception as e:
                logger.error(msg = 'Client failed to execute query: {0}'.format(e))
                # self.connect.rollback()  ## not needed for read-only
                raise

    ## build 'agency' table query
    def agency_query(self, params):
        params_valid = [
            'iata_id',
            'agency',
            'city',
            'country',
            'region',
            'continent'
        ]
        
        ## base query
        query = "SELECT * FROM agency"
        
        ## build query
        values = list()
        if params:
            clauses = list()
            for key, val in params.items():
                if key in params_valid:

                    ## validate params
                    check_query = "SELECT EXISTS(SELECT 1 FROM agency WHERE {x} = %s)".format(x = key)
                    with self.connect.cursor() as cur:
                        cur.execute(check_query, (val,))
                        exists = cur.fetchone()[0]
                    if not exists:
                        raise InvalidParameterError('Invalid parameter value: {x}'.format(x = val))
                    clauses.append("{x} = %s".format(x = key))
                    values.append(val)
                else:
                    raise InvalidParameterError('Invalid parameter: {x}'.format(x = key))
            query += " WHERE " + " AND ".join(clauses)
        return query, values

    ## build 'events' table query
    def events_query(self, params):
        params_valid = [
            'iata_id',
            'vehicle_id',
            'trip_id',
            'route_id',
            'datetime',
            'start_datetime',
            'end_datetime',
            'duration',
            'min_duration',
            'max_duration'
        ]

        ## base query
        query = "SELECT * FROM events"

        ## build query
        values = list()
        if params:
            clauses = list()
            for key, val in params.items():

                ## validate params
                if key in params_valid:
                    if key.endswith('_id'):
                        check_query = "SELECT EXISTS(SELECT 1 FROM events WHERE {x} = %s)".format(x = key)
                        with self.connect.cursor() as cur:
                            cur.execute(check_query, (val,))
                            exists = cur.fetchone()[0]
                        if not exists:
                            raise InvalidParameterError('Invalid parameter value: {x}'.format(x = val))
                    if key == 'start_datetime':
                        clauses.append("datetime >= %s")
                        values.append(val)
                    elif key == 'end_datetime':
                        clauses.append("datetime <= %s")
                        values.append(val)
                    elif key == 'min_duration':
                        clauses.append("duration >= %s")
                        values.append(val)
                    elif key == 'max_duration':
                        clauses.append("duration <= %s")
                        values.append(val)
                    else:
                        clauses.append("{x} = %s".format(x = key))
                        values.append(val)
                else:
                    raise InvalidParameterError('Invalid parameter: {x}'.format(x = key))
            query += " WHERE " + " AND ".join(clauses)
        return query, values

    ## build 'idle' table query
    def idle_query(self, params):
        params_valid = {
            'iata_id': 'events',
            'vehicle_id': 'events',
            'trip_id': 'events',
            'route_id': 'events',
            'datetime': 'events',
            'start_datetime': 'events',
            'end_datetime': 'events',
            'duration': 'events',
            'min_duration': 'events',
            'max_duration': 'events',
            'agency': 'agency',
            'city': 'agency',
            'country': 'agency',
            'region': 'agency',
            'continent': 'agency'
        }

        ## base query
        query = """
            SELECT agency.*, events.vehicle_id, events.trip_id, events.route_id, 
                   events.latitude, events.longitude, events.datetime, events.duration 
            FROM agency LEFT JOIN events ON agency.iata_id = events.iata_id
            """

        ## build query
        values = list()
        if params:
            clauses = list()
            for key, val in params.items():

                ## validate params
                if key in params_valid:
                    if key.endswith('_id') or key in ['agency', 'city', 'country', 'region', 'continent']:
                        check_query = "SELECT EXISTS(SELECT 1 FROM events WHERE {x} = %s)".format(x = key)
                        with self.connect.cursor() as cur:
                            cur.execute(check_query, (val,))
                            exists = cur.fetchone()[0]
                        if not exists:
                            raise InvalidParameterError('Invalid parameter value: {x}'.format(x = val))
                    if key == 'start_datetime':
                        clauses.append("events.datetime >= %s")
                        values.append(val)
                    elif key == 'end_datetime':
                        clauses.append("events.datetime <= %s")
                        values.append(val)
                    elif key == 'min_duration':
                        clauses.append("events.duration >= %s")
                        values.append(val)
                    elif key == 'max_duration':
                        clauses.append("events.duration <= %s")
                        values.append(val)
                    else:
                        clauses.append("{x}.{y} = %s".format(x = params_valid[key], y = key))
                        values.append(val)
                else:
                    raise InvalidParameterError('Invalid parameter: {x}'.format(x = key))
            query += " WHERE " + " AND ".join(clauses)
        return query, values

    ## close database connection
    def db_close(self):
        if hasattr(self, 'connect'):
            try:
                if self.connect.closed == 0:
                    self.connect.close()
                    logger.info(msg = 'Client successfully closed database connection.')
            except Exception as e:
                logger.error(
                    msg = 'Client error closing database connection: {x}'.format(
                        x = e
                    )
                )

## end program