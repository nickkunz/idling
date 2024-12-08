## libraries
import os
import time
import json
import logging
import threading
import socket
import socketio
import psycopg2
from psycopg2.pool import SimpleConnectionPool

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
                 recon_tries = 20, recon_delay = 1, recon_timeo = 120):

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

        ## initialize the connection pool
        self.db_pool = None
        self.connect = None

    ## connect to database
    def db_conn(self):
        if self.db_pool is None:
            i = 0
            while i < self.recon_tries:
                try:
                    self.db_pool = SimpleConnectionPool(
                        minconn = 1, 
                        maxconn = 10,
                        database = self.db_name,
                        user = self.db_user,
                        password = self.db_pswd,
                        host = self.db_host,
                        port = self.db_port
                    )
                    logger.info("Connection pool successfully created.")
                    break
                except Exception as e:
                    logger.warning('Failed to create connection pool. Attempt {}/{}: {}'.format(
                        i + 1, self.recon_tries, e
                    ))
                    i += 1
                    time.sleep(self.recon_delay)
            
            if i == self.recon_tries:
                logger.error('Failed to create connection pool after maximum attempts.')
                
                ## close all connections to free resources
                if self.db_pool is not None:
                    self.db_pool.closeall()
                    self.db_pool = None
                raise Exception('Failed to create connection pool.')

        ## connection from the pool
        if self.connect and self.connect.closed == 0:
            logger.info('Database connection already exists.')
            return

        i = 0
        while i < self.recon_tries:
            try:
                self.connect = self.db_pool.getconn()
                if self.connect and self.connect.closed == 0:
                    logger.info('Client successfully acquired a connection from the pool.')
                    break
            except Exception as e:
                logger.warning('Failed to get connection from pool. Attempt {}/{}: {}'.format(
                    i + 1, self.recon_tries, e
                ))
            i += 1
            time.sleep(self.recon_delay)

        if i == self.recon_tries or not self.connect or self.connect.closed != 0:
            logger.error('Failed to get a valid connection from the pool.')
            
            ## close the connection pool with no valid connection
            if self.db_pool is not None:
                self.db_pool.closeall()
                self.db_pool = None
            raise Exception('Failed to get a valid connection from the pool.')

    ## read sql file
    def db_read(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                logger.debug('Client successfully read SQL query.')
                return f.read()  ## query contents
        else:
            return ''  ## empty string if file does not exist

    ## initialize database
    def db_init(self):
        self.cursor = self.connect.cursor()

        ## init database
        query = self.db_read(path = self.sql_init)  ## init query file path
        self.cursor.execute(query = query)
        self.connect.commit()
        logger.info('Client successfully initialized database.')

        ## create agency table
        query = self.db_read(path = self.sql_agency)  ## agency query file path
        self.cursor.execute(query = query)
        self.connect.commit()
        logger.info('Client successfully created agency table.')

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
            logger.info('Client successfully connected to {}.'.format(self.ws_host))

        @self.sio.event
        def connect_error(data):
            logger.error('Client failed to connect to {}: {}'.format(self.ws_host, data))

        @self.sio.event
        def disconnect():
            logger.warning('Client disconnected from {}.'.format(self.ws_host))

        @self.sio.on('ping')
        def on_ping(data):
            if data is None or len(data) == 0:
                logger.warning('Client received empty ping from server.')
                self.sio.emit('pong', 'default data')

        @self.sio.on('events')
        def on_message(json_data):
            if not self.sio.connected:
                logger.warning('Client is not connected to the websocket server.')
                return

            ## check if database connection is closed
            if self.connect.closed != 0:
                logger.warning("Database connection closed. Attempting to reconnect...")
                
                ## return the closed connection
                if self.connect:
                    self.db_pool.putconn(self.connect, close = False)
                    self.connect = None

                self.db_conn()
                if self.connect.closed != 0:
                    logger.error("Failed to reconnect to database before processing events.")
                    return

            ## parse json response
            try:
                data = json.loads(json_data)
                if len(data) == 0:
                    logger.warning('Client received empty websocket response.')
                    return
            except Exception as e:
                logger.error('Client failed to parse websocket response.')
                return

            ## insert events into table
            max_write_retries = 5
            for attempt in range(1, max_write_retries + 1):
                try:
                    with self.lock:
                        cursor = self.connect.cursor()
                        for i in data:
                            query = self.db_read(path = self.sql_events)
                            logger.debug('Client successfully read SQL query.')

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
                        
                        ## successful write
                        self.connect.commit()
                        logger.info('Client successfully wrote observations to database.')
                        break

                except psycopg2.InterfaceError as ie:
                    logger.error('Database connection lost during write (Attempt {}): {}'.format(attempt, ie))
                    ## put the broken connection back if possible and get a fresh one
                    if self.connect:
                        self.db_pool.putconn(self.connect, close = False)
                        self.connect = None
                    self.db_conn()

                    if attempt == max_write_retries:
                        logger.error('Exceeded maximum write retries due to connection issues.')
                        return

                except Exception as e:
                    self.connect.rollback()
                    logger.error('Client failed to write to database: {}.'.format(e))
                    if attempt == max_write_retries:
                        logger.error('Exceeded maximum write retries due to repeated errors.')
                        return
                    time.sleep(1)

    ## connect to websocket with threading
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
                logger.warning('Client failed to connect to websocket server. Reconnection attempt {} of {}: {}'.format(
                    i + 1,
                    self.recon_tries,
                    e
                ))
                time.sleep(self.recon_delay)
        else:
            logger.error('Client failed to connect to websocket server. Max number of reconnection attempts.')

    def ws_conn(self):
        if hasattr(self, 'sio') and self.sio.connected:
            logger.info('Client already connected to websocket server.')
            return

        if self.ws_host is None:
            logger.error('Client has no websocket server specified.')
            raise Exception('Client has no websocket server specified.')

        ## start websocket thread
        self.ws_thread = threading.Thread(target = self.ws_thrd)
        self.ws_thread.start()

    ## close database connection and websocket
    def close(self):
        
        ## remove connection from pool
        if hasattr(self, 'connect') and self.connect is not None:
            try:
                self.db_pool.putconn(self.connect, close = True)
                self.connect = None
                logger.info('Database connection returned to pool.')
            except Exception as e:
                logger.error('Error returning database connection to pool: {}'.format(e))

        ## disconnect websocket
        if hasattr(self, 'sio') and self.sio is not None:
            try:
                if self.sio.connected:
                    self.sio.disconnect()
                    logger.info('Disconnected from websocket.')
            except Exception as e:
                logger.error('Error disconnecting websocket client: {}'.format(e))

        ## stop active threads
        if hasattr(self, 'ws_thread') and self.ws_thread.is_alive():
            self.ws_thread.join()
            logger.info('Websocket thread stopped.')

    ## run client
    def run(self):
        while True:
            try:
                ## connect database
                self.db_conn()

                try:
                    ## initialize database
                    self.db_init()
                except Exception as init_ex:
                    logger.error('Database initialization failed: {}. Retrying...'.format(init_ex))
                    
                    ## return any allocated connection before retrying
                    if self.connect:
                        self.db_pool.putconn(self.connect, close = False)
                        self.connect = None
                    time.sleep(5)
                    continue

                ## initialize websocket and connect
                self.ws_init()
                self.ws_conn()
                while not self.sio.connected:  ## wait for websocket connection
                    time.sleep(1)

                logger.info("All connections established. Running main loop.")

                ## main loop
                while True:
                    if self.connect.closed != 0:
                        logger.warning("Database connection lost. Reconnecting...")
                        if self.connect:
                            self.db_pool.putconn(self.connect, close = False)
                            self.connect = None
                        self.db_conn()

                    if not self.sio.connected:
                        logger.warning("Websocket connection lost. Reconnecting...")
                        self.close()
                        break  ## breaks out of inner loop and restarts from the outer loop

                    time.sleep(5)

            except Exception as e:
                self.close()  ## clean resources
                logger.error('Client encountered an error while running: {}.'.format(e))
                time.sleep(5)

## end program