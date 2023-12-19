## libraries
import os
import time
import json
import logging
import threading
import socket
import socketio
import psycopg2

## params
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## logging
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdlr = logging.StreamHandler()
hdlr.setFormatter(fmt = fmt)
logging.basicConfig(level = LOG_LEVEL, handlers = [hdlr])
logger = logging.getLogger(name = __name__)
logger.propagate = True

## client to database
class WriteClient():
    def __init__(self,
                 ws_host,
                 db_name, db_user, db_pswd, db_host, db_port,
                 sql_init, sql_agency, sql_events,
                 recon_tries = 3, recon_delay = 1, recon_timeo = 60):

        self.ws_host = ws_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_pswd = db_pswd
        self.db_host = db_host
        self.db_port = db_port
        self.sql_init = sql_init
        self.sql_agency = sql_agency
        self.sql_events = sql_events
        self.recon_tries = recon_tries
        self.recon_delay = recon_delay
        self.recon_timeo = recon_timeo
        self.lock = threading.Lock()

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
                    port = self.db_port
                )
                logger.info(msg = 'Client successfully connected to database.')
                break
            except Exception as e:
                logger.warning(msg = 'Client failed to connect to database. Reconnection attempt {x} of {y}: {z}.'.format(
                        x = i + 1,
                        y = self.recon_tries,
                        z = e
                    )
                )
                i += 1
                time.sleep(self.recon_delay)

        if i == self.recon_tries:
            logger.error(msg = 'Client failed to connect to database. Max number of reconnection attempts.')
            raise Exception('Client failed to connect to database.')

    ## read sql file
    def db_read(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                logger.debug(msg = 'Client successfully read SQL query.')
                return f.read()  ## query contents
        else:
            return ''  ## empty string if file does not exist

    ## initialize database
    def db_init(self):
        
        ## check for existing tables
        self.cursor = self.connect.cursor()
        self.cursor.execute("SELECT to_regclass('public.agency')")
        if self.cursor.fetchone()[0] is not None:
            logger.info(msg = 'Client already initialized database.')

        ## init first run
        else:
            query = self.db_read(path = self.sql_init) ## init query file path
            self.cursor = self.connect.cursor()
            self.cursor.execute(query = query)
            self.connect.commit()
            logger.info(msg = 'Client successfully initialized database.')

        ## create transit agency table
        self.cursor.execute("SELECT to_regclass('public.agency')")
        if self.cursor.fetchone()[0] is None:
            query = self.db_read(path = self.sql_agency)  ## agency query file path
            self.cursor.execute(query = query)
            self.connect.commit()
            logger.info(msg = 'Client successfully created agency table.')

    ## initialize websocket
    def ws_init(self):
        self.sio = socketio.Client(
            reconnection = True,
            reconnection_attempts = self.recon_tries,
            reconnection_delay = self.recon_delay,
            reconnection_delay_max = self.recon_timeo,
            logger = False
        )

        ## websocket event handler
        @self.sio.event
        def connect():
            logger.info(
                msg = 'Client successfully connected to {x}.'.format(
                    x = self.ws_host
                )
            )

        @self.sio.event
        def connect_error(data):  # Updated this line
            logger.error(
                msg = 'Client failed to connect to {x}: {y}'.format(  # Updated this line
                    x = self.ws_host,
                    y = data  # This is the error message passed by socketio
                )
            )

        @self.sio.event
        def disconnect():
            logger.warning(
                msg = 'Client disconnected from {x}.'.format(
                    x = self.ws_host
                )
            )

        @self.sio.on('ping')
        def on_ping(data):
            if data is None or len(data) == 0:
                logger.warning(msg = 'Client received empty ping from server.')
                self.sio.emit('pong', 'default data')

        @self.sio.on('events')  ## listen for events titled 'events'
        def on_message(json_data):
            if not self.sio.connected:
                logger.warning(msg = 'Client is not connected to the websocket server.')
                return

            ## parse json response
            try:
                data = json.loads(json_data)
                if len(data) == 0:
                    logger.warning(msg = 'Client received empty websocket response.')
                    return

            except Exception as e:
                logger.error(msg = 'Client failed to parse websocket response.')

            ## insert events into table
            try:
                with self.lock:
                    cursor = self.connect.cursor()
                    for i in data:
                        query = self.db_read(path = self.sql_events)
                        logger.debug(msg = 'Client successfully read SQL query.')

                        cursor.execute(
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

                    ## save changes to database
                    self.connect.commit()
                    logger.info(msg = 'Client successfully wrote to database.')
                    time.sleep(0.1)  ## patch for packet queue is empty error

            ## undo insert attempt
            except psycopg2.extensions.TransactionRollbackError as e:
                self.connect.rollback()
                logger.error(
                    msg = 'Client failed to write to database: {x}.'.format(
                        x = e
                    )
                )

    ## return immediately if the websocket connection cannot be established
    def ws_thrd(self):
        for i in range(0, self.recon_tries):
            try:
                self.sio.connect(
                    url = self.ws_host,
                    transports = 'websocket',
                    wait_timeout = self.recon_timeo
                )
                if self.sio.connected:
                    break
            except (Exception, socket.timeout) as e:
                logger.warning(
                    msg = 'Client failed to connect to websocket server. Reconnection attempt {x} of {y}: {z}.'.format(
                        x = i + 1,
                        y = self.recon_tries,
                        z = e
                    )
                )
                time.sleep(self.recon_delay)
        else:
            logger.error(msg = 'Client failed to connect to websocket server. Max number of reconnection attempts.')

    ## connect to websocket
    def ws_conn(self):
        if hasattr(self, 'sio') and self.sio.connected:
            logger.info(msg = 'Client already connected to websocket server.')
            return

        if self.ws_host == None:
            logger.error(msg = 'Client has no websocket server specified.')
            raise Exception('Client has no websocket server specified.')

        ## start websocket thread
        self.ws_thread = threading.Thread(target = self.ws_thrd)
        self.ws_thread.start()

    ## close database connection and websocket
    def close(self):
        if hasattr(self, 'connect') and self.connect is not None: 
            try:
                if self.connect.closed == 0:
                    self.connect.close()
                    logger.info(msg = 'Database connection closed.')
            except Exception as e:
                logger.error(
                    msg = 'Error closing database connection: {x}'.format(
                        x = e
                    )
                )

        ## disconnect websocket
        if hasattr(self, 'sio') and self.sio is not None:
            try:
                if self.sio.connected:
                    self.sio.disconnect()
                    logger.info(msg = 'Disconnected from websocket.')
            except Exception as e:
                logger.error(
                    msg = 'Error disconnecting Websocket client: {x}'.format(
                        x = e
                    )
                )

        ## stop active threads
        if hasattr(self, 'ws_thread') and self.ws_thread.is_alive():
            self.ws_thread.join()
            logger.info(msg = 'Websocket thread stopped.')

    ## run client
    def run(self):
        try:
            self.db_conn()  ## connect database
            self.db_init()  ## initialize database
            self.ws_init()  ## initialize websocket
            self.ws_conn()  ## connect websocket

        except Exception as e:
            self.close()  ## clean resources
            logger.error('Client encountered an error while running: {x}.'.format(
                x = e
                )
            )

## end program