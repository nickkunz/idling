## libraries
import os
import ssl
import logging
import aiohttp
import asyncio
import selectors
import configparser
from datetime import datetime
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2
from aiohttp import ClientPayloadError

## params
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## logging
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdlr = logging.StreamHandler()
hdlr.setFormatter(fmt = fmt)
logging.basicConfig(level = LOG_LEVEL, handlers = [hdlr])
logger = logging.getLogger(name = __name__)
logger.propagate = True

## ssl certs
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

## selectors bug fix
selectors._PollLikeSelector.modify = (selectors._BaseSelectorImpl.modify)

## ini section keys
def ini_key(file, sect = None):

    """
    Desc:
        Loads a configuration variables from specified section in .ini file and 
        returns them as a dictionary. If no section is specified, it returns all 
        of the variables in the .ini file.

    Args:
        file (str): Path of the .ini configuration file.
        sect (str): Name of the section witin the .ini file. Default is None.

    Returns:
        dict: A dictionary containing the key-value pairs of the specified section, 
        or all key-value pairs in the .ini file if no section is specified.

    Raises:
        TypeError: The argument 'file' is not a string.
        TypeError: The argument 'sect' is not a string.
    """

    ## arg check
    if not isinstance(file, str):
        raise TypeError("The 'file' argument must be a string.")

    if sect is not None and not isinstance(sect, str):
        raise TypeError("The 'sect' argument must be a string or None.")

    ## input ini file 
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option  ## preserve uppercase vars
    config.read(file)

    ## output keys
    keys = dict()
    for i in config[sect]:
        value = config.get(sect, i)
        keys[i] = value

    return keys

## env variables
def env_var(file):

    """
    Desc:
        Loads environment variables from .env file and returns them as a dictionary.

    Args:
        file (str): The path of the .env file.

    Returns:
        dict: A dictionary containing the environment variables.

    Raises:
        TypeError: The argument 'file' is not a string.
    """

    ## arg check
    if not isinstance(file, str):
        raise TypeError("The 'file' argument must be a string.")

    ## load env vars
    load_dotenv(file)

    ## output vars
    vars = dict()
    for i in os.environ:
        vars[i] = os.environ[i]

    return vars

## client to extract data
class ExtractClient():
    def __init__(self, env_file, ini_file, ini_sect):
        """
        Desc:
            Extracts GTFS Realtime feeds from specified transit agency REST API endpoints.

        Args:
            env_file (str): Path to .env file containing environment variables.
            ini_file (str): Path to .ini configuration file containing API endpoints.
            ini_sect (str): Section of the .ini configuration file to use (optional).

        Returns:
            A tuple with three elements:
            - A serialized protobuf message respons.
            - An HTTP status code (200 good, 500 error).
            - A dictionary with three key-value pairs indicating content type, content
              length, and connection type.

        Raises:
            TypeError: If any of the arguments are not a string.
        """

        ## arg check
        if not isinstance(env_file, str):
            raise TypeError('env_file arg must be a string')
        if not isinstance(ini_file, str):
            raise TypeError('ini_file arg must be a string')
        if not isinstance(ini_sect, str):
            raise TypeError('ini_sect arg must be a string')

        self.env_file = env_file
        self.ini_file = ini_file
        self.ini_sect = ini_sect
        self.key_last = dict()

        ## api keys
        self.keys = env_var(
            file = self.env_file
        )

        ## api endpoints (gtfs realtime feeds)
        self.urls = ini_key(
            file = self.ini_file,
            sect = self.ini_sect
        )

    ## toggle between two api keys
    def alt_key(self, url, keys):
        second = datetime.now().second
        key = keys[second % len(keys)]

        logging.debug(msg = 'Client used API key {x} for URL {y}'.format(
            x = hash(key),  ## hash of the key for security
            y = url
            )
        )
        return key
    
    ## extract data
    async def run(self):
        connector = aiohttp.TCPConnector(
            ssl = ssl_context if 'https' in self.urls else False,
            keepalive_timeout = 125
        )

        ## stop auto headers
        skip_auto_headers = {
            aiohttp.hdrs.USER_AGENT,
            aiohttp.hdrs.ACCEPT_ENCODING, 
            aiohttp.hdrs.HOST
        }
        headers_master = {
            'User-Agent': 'GRD-TRT-BUF-4I/0.0.1',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }

        ## create session
        async with aiohttp.ClientSession(
            connector = connector,
            loop = asyncio.get_event_loop(),
            skip_auto_headers = skip_auto_headers,
            trust_env = True
            ) as session:

            ## add headers and params for selected endpoints
            connection = list()
            for i, url in self.urls.items():
                headers = headers_master.copy()

                ## new york
                if i == 'API_END_NYC':
                    params = {'key': self.keys['API_KEY_NYC']}
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
                        )
                    )
                ## wash dc
                elif i == 'API_END_DCA':
                    headers['api_key'] = self.keys['API_KEY_DCA']
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers
                        )
                    )
                ## los angeles, miami
                elif i in ['API_END_LAX', 'API_END_MIA']:
                    headers['Authorization'] = self.keys['API_KEY_LBM']
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers
                        )
                    )
                ## san fran
                elif i == 'API_END_SFO':
                    params = {
                        'api_key': self.keys['API_KEY_SFO'],
                        'agency': 'RG'
                    }
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
                        )
                    )
                ## portland
                elif i == 'API_END_PDX':
                    params = {'appID': self.keys['API_KEY_PDX']}
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
                        )
                    )
                ## phoenix
                elif i == 'API_END_PHX':
                    params = {'apiKey': self.keys['API_KEY_PHX']}
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
                        )
                    )
                ## montreal
                elif i == 'API_END_YUL':
                    headers['apiKey'] = self.keys['API_KEY_YUL']
                    headers['Accept'] = 'application/x-protobuf'  ## required to return protobufs
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers
                        )
                    )
                ## vancouver
                elif i == 'API_END_YVR':
                    params = {'apikey': self.keys['API_KEY_YVR']}
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
                        )
                    )
                ## stockholm
                elif i == 'API_END_ARN':
                    params = {'key': self.keys['API_KEY_ARN']}
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
                        )
                    )
                ## dublin
                elif i == 'API_END_DUB':
                    keys = (self.keys['API_KEY_DUB_A'], self.keys['API_KEY_DUB_B'])
                    headers['x-api-key'] = self.alt_key(  ## toggle api keys
                        url = url,
                        keys = keys
                    )
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers
                            )
                        )
                ## sydney
                elif i == 'API_END_SYD':
                    headers['Authorization'] = 'apikey' + ' ' + self.keys['API_KEY_SYD']
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers
                        )
                    )
                ## auckland
                elif i == 'API_END_AKL':
                    headers['Ocp-Apim-Subscription-Key'] = self.keys['API_KEY_AKL']
                    headers['Accept'] = 'application/x-protobuf'  ## required to return protobufs
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers
                        )
                    )
                ## christchurch
                elif i == 'API_END_CHC':
                    headers['Ocp-Apim-Subscription-Key'] = self.keys['API_KEY_CHC']
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers
                        )
                    )
                ## delhi
                elif i == 'API_END_DEL':
                    params = {'key': self.keys['API_KEY_DEL']}
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
                        )
                    )
                ## other cities without headers and params
                else:
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers_master
                        )
                    )

                ## log request headers before sending requests
                logging.debug('Request headers for {x}: {y}'.format(
                        x = url,
                        y = headers
                    )
                )

            ## join requests and process responses
            response = await asyncio.gather(*connection, return_exceptions = True)
            feeds = bytes()
            for url, k in enumerate(response):

                ## log response status
                url_log = list(self.urls.values())[url]
                content = None

                ## failed request
                if isinstance(k, Exception):
                    if hasattr(k, 'status'):

                        ## exceeded rate limit response
                        if k.status == 429:
                            t_retry = int(k.headers.get('Retry-After', 0))
                            logging.warning(
                                msg = 'GET request to {x} rate limited with HTTP status code {y}. Retry after {t} seconds.'.format(
                                    x = url_log,
                                    y = k.status,
                                    t = t_retry
                                )
                            )
                            continue  # proceeds to next url upon exception

                        ## other unsuccessful response
                        elif k.status != 200:
                            logging.warning(
                                msg = 'GET request to {x} unsuccessful with HTTP status code {y}.'.format(
                                    x = url_log,
                                    y = k.status
                                )
                            )
                            continue  ## proceeds to next url upon exception
                    else:
                        logging.error(
                            msg = 'GET request to {x} failed with unknown HTTP status.'.format(
                                x = url_log
                            )
                        )
                    continue ## proceeds to next url upon exception

                ## successful response
                else:
                    logging.debug(
                        msg = 'GET request to {x} successful with HTTP status code {y}.'.format(
                            x = url_log,
                            y = k.status
                        )
                    )
                    try:
                        content = await k.content.read()  ## bytes data type

                    ## payload error
                    except ClientPayloadError as e:
                        logging.error(
                            msg = '{x}.'.format(
                                x = e
                                )
                            )

                ## parse protobuf
                message = gtfs_realtime_pb2.FeedMessage()
                if content is not None:
                    try:
                        message.ParseFromString(bytes(content))  ## force bytes data type
                        logging.debug(
                            msg = 'Protobuf parsing successful for {x}.'.format(
                                x = url_log
                            )
                        )
                    except Exception as e:
                        logging.error(
                            msg = 'Protobuf parsing error: {x}'.format(
                                x = e
                            )
                        )
                        continue

                ## unsuccessful protobuf response, http status, headers (strict order)
                else:
                    logging.warning(msg = 'No protobuf response to parse.')
                    return None, 202, {
                        'Content-Type': 'application/x-protobuf',
                        'Content-Length': 0,
                        'Connection': 'keep-alive'
                    }

                # validate message header
                if (message.header.gtfs_realtime_version == '2.0' or \
                    message.header.gtfs_realtime_version == '1.0') and \
                    message.header.incrementality == gtfs_realtime_pb2.FeedHeader.FULL_DATASET:

                    ## validate entity
                    entity_valid = [j for j in message.entity if (
                        (j.vehicle.vehicle.id or (j.vehicle.vehicle.label and j.id)) and \
                        j.vehicle.timestamp and \
                        j.vehicle.position.latitude and \
                        j.vehicle.position.longitude and \
                        (j.vehicle.trip.route_id or j.vehicle.trip.trip_id)
                        )
                    ]
                    url_key = list(self.urls.keys())[url]
                    for j in entity_valid:
                        if not j.vehicle.vehicle.id and j.vehicle.vehicle.label and j.id:
                            j.vehicle.vehicle.id = j.id  ## reassign vehicle id with label
                        j.vehicle.vehicle.label = url_key.upper()[-3:]  ## reassign vehicle label with iata code

                    ## final message validation
                    del message.entity[:]
                    message.entity.extend(entity_valid)
                    logging.debug(
                        msg = 'Protobuf validation successful for {x}.'.format(
                            x = url_log
                        )
                    )

                    ## serialize message, append to feed, update content length
                    feeds += message.SerializeToString()
                    content_length = len(feeds) if feeds else 0

            ## successful protobuf response, http status, headers (strict order)
            return feeds, 200, {
                'Content-Type': 'application/x-protobuf',
                'Content-Length': str(content_length),
                'Connection': 'keep-alive'
            }

## end program