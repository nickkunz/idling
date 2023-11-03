## libraries
import os
import sys
import logging
import aiohttp
import asyncio
import configparser
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2

## modules
sys.path.insert(0, './')

## params
LOG_LEVEL = str(os.getenv('LOG_LEVEL', 'INFO'))

## logging config
logging.basicConfig(
    level = LOG_LEVEL,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

## fix for selectors bug
import selectors
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

## extract data from source
class ExtractData():
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
            raise TypeError("env_file arg must be a string")
        if not isinstance(ini_file, str):
            raise TypeError("ini_file arg must be a string")
        if not isinstance(ini_sect, str):
            raise TypeError("ini_sect arg must be a string")

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
        if url not in self.key_last:
            self.key_last[url] = keys[0]  ## default first key

        ## alternating logic
        key_a = self.key_last[url]
        key_b = keys[1] if key_a == keys[0] else keys[0]
        self.key_last[url] = key_b
        return key_b

    ## extract data
    async def ext_dat(self):

        ## create session
        headers_master = {
            'User-Agent': 'GRD-TRT-BUF-4I/1.0',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
        connector = aiohttp.TCPConnector(
            ssl = True if 'https' in self.urls else False
        )
        async with aiohttp.ClientSession(
            connector = connector,
            trust_env = True
            ) as session:

            ## add auth headers for cities
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
                        'agency': 'SF'
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
                    params = {'token': self.keys['API_KEY_YUL']}
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers,
                            params = params
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
                    keys = [self.keys['API_KEY_DUB_A'], self.keys['API_KEY_DUB_B']]
                    key = self.alt_key(  ## toggle api keys
                        url = url,
                        keys = keys
                    )
                    headers['x-api-key'] = key
                    connection.append(
                        session.get(
                            url=url,
                            headers=headers
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
                ## other cities without auth headers
                else:
                    connection.append(
                        session.get(
                            url = url,
                            headers = headers_master
                        )
                    )

            ## log request headers before sending requests
            logging.debug(f"Request headers for ({url}): {headers}")

            ## join requests and process responses
            response = await asyncio.gather(*connection)
            feeds = bytes()
            for url, k in enumerate(response):

                ## log response status
                url_log = list(self.urls.values())[url]
                if isinstance(k, Exception):
                    logging.error(
                        msg = f"GET request to {url_log} failed with exception: {k}"
                    )
                    continue
                if k.status != 200:
                    logging.warning(
                        msg = f"GET request to {url_log} unsuccessful with HTTP status code {k.status}."
                    )
                    continue  ## proceeds to next url upon exception
                else:
                    logging.info(
                        msg = f"GET request to {url_log} successful with HTTP status code {k.status}."
                    )
                    content = await k.content.read()

                ## parse protobuf
                message = gtfs_realtime_pb2.FeedMessage()
                message.ParseFromString(bytes(content))

                # validate message header
                if (message.header.gtfs_realtime_version == '2.0' or \
                    message.header.gtfs_realtime_version == '1.0') and \
                    message.header.incrementality == gtfs_realtime_pb2.FeedHeader.FULL_DATASET:

                    valid_entity = [j for j in message.entity if (
                        j.vehicle.vehicle.id and \
                        j.vehicle.timestamp and \
                        j.vehicle.position.latitude and \
                        j.vehicle.position.longitude and \
                        (j.vehicle.trip.route_id or j.vehicle.trip.trip_id)
                        )
                    ]
                    url_key = list(self.urls.keys())[url]
                    for j in valid_entity:
                        j.vehicle.vehicle.label = url_key.upper()[-3:]

                    ## end message validation
                    del message.entity[:]
                    message.entity.extend(valid_entity)

                    ## serialize message, append to feed, update content length
                    feeds += message.SerializeToString()
                    content_length = len(feeds)

            ## successful protobuf response, http status, headers (strict order)
            return feeds, 200, {
                'Content-Type': 'application/x-protobuf',
                'Content-Length': str(content_length),
                'Connection': 'keep-alive'
            }

## end program