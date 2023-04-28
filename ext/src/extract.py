## libraries
import sys
import base64
import aiohttp
import asyncio
from google.transit import gtfs_realtime_pb2

## modules
sys.path.insert(0, './')
from conf.conf import ini_key, env_var

## fix for selectors bug
import selectors
selectors._PollLikeSelector.modify = (
    selectors._BaseSelectorImpl.modify
)

## extract data from source
class ExtractData():
    def __init__(self, env_file, ini_file, ini_sect):

        """
        Desc:
            Extracts GTFS Real-Time telemetry vehicle positions directly from 
            specified transportation agency API's.

        Args:
            env_file (str): Path to .env file containing environment variables.
            ini_file (str): Path to .ini configuration file.
            ini_sect (str): Section of the .ini configuration file to use.

        Returns:
            A tuple with three elements:
            - A serialized protobuf message containing real-time transit data.
            - An HTTP status code (always 200).
            - A dictionary with a single key-value pair indicating that the 
              message is in the 'application/x-protobuf' format.
        
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

        ## api keys
        self.keys = env_var(
            file = self.env_file
        )

        ## api urls
        self.urls = ini_key(
            file = self.ini_file,
            sect = self.ini_sect
        )

        ## add api key to urls
        self.add_key()

    ## add api key to urls
    def add_key(self):
        for k in self.urls.keys():
            if k.startswith('url_'):
                key = k.upper()[4:] + '_API_KEY'
                if key in self.keys:
                    self.urls[k] += self.keys[key]

    ## extract data
    async def ext_dat(self):
        try:
            async with aiohttp.ClientSession(trust_env = True) as sess:
                conn = list()
                for k, i in self.urls.items():

                    ## los angeles and baltimore and miami auth headers
                    if k in ['url_lax', 'url_bwi', 'url_mia']:
                        head = {'Authorization': self.keys['LBM_API_KEY']}
                        conn.append(
                            sess.get(i, headers = head)
                        )

                    ## chicago user and pass auth headers
                    elif k == 'url_ord':
                        auth = self.keys['ORD_API_USR'] + ":" + self.keys['ORD_API_PWD']
                        auth = base64.b64encode(auth.encode()).decode()
                        head = {'Authorization': 'Basic ' + auth}
                        conn.append(
                            sess.get(i, headers = head)
                        )

                    ## washington dc auth headers
                    elif k == 'url_dca':
                        head = {'api_key': self.keys['DCA_API_KEY']}
                        conn.append(
                            sess.get(i, headers = head)
                        )

                    ## montreal auth headers
                    elif k == 'url_yul':
                        head = {'apiKey': self.keys['YUL_API_KEY']}
                        conn.append(
                            sess.get(i, headers = head)
                        )

                    ## sydney auth headers
                    elif k == 'url_syd':
                        head = {'Authorization': 'apikey ' + self.keys['SYD_API_KEY']}
                        conn.append(
                            sess.get(i, headers = head)
                        )

                    ## other cities no auth headers
                    else:
                        conn.append(
                            sess.get(i)
                        )

                ## join requests
                resps = await asyncio.gather(
                    *conn, 
                    return_exceptions = False
                )

                ## process responses
                feeds = bytes()
                for url, i in enumerate(resps):
                    content = await i.content.read()

                    ## parse protobuf
                    message = gtfs_realtime_pb2.FeedMessage()
                    message.ParseFromString(bytes(content))

                    # validate header
                    header = message.header
                    if (header.gtfs_realtime_version == '2.0' or \
                        header.gtfs_realtime_version == '1.0') and \
                        header.incrementality == gtfs_realtime_pb2.FeedHeader.FULL_DATASET:

                            ## validate entity
                            entity = message.entity
                            entity_valid = [j for j in entity if (
                                j.vehicle.vehicle.id and 
                                j.vehicle.trip.route_id and 
                                j.vehicle.trip.trip_id and 
                                j.vehicle.timestamp and 
                                j.vehicle.position.latitude and 
                                j.vehicle.position.longitude
                                )
                            ]

                            ## use vehicle label field as data source
                            url_key = list(self.urls.keys())[url]
                            url_src = self.urls[url_key]
                            for j in entity_valid:
                                j.vehicle.vehicle.label = url_src

                            ## validation end
                            del message.entity[:]
                            message.entity.extend(entity_valid)

                            ## serialize message and append to feed
                            feeds += message.SerializeToString()

                    # close the connection
                    await i.release()

                ## close session
                await sess.close()

                ## protobuf, http code, content type
                return feeds, 200, {
                    'Content-Type': 'application/x-protobuf'
                }

        ## session error
        except:
            return b'', 500, {
                'Content-Type': 'application/x-protobuf'
            }

## end of program