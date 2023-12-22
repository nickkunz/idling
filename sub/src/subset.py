## libaries
import os
import time
import json
import logging
import requests as rq
from google.transit import gtfs_realtime_pb2

## params
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## logging
fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
hdlr = logging.StreamHandler()
hdlr.setFormatter(fmt = fmt)
logging.basicConfig(level = LOG_LEVEL, handlers = [hdlr])
logger = logging.getLogger(name = __name__)
logger.propagate = True

## get request
def get_req_par(url, key = None):

    """ 
    Desc:
        Makes a GET request to 'url' with 'key' in header. Expects a valid 
        protobuf response and parses it.
    
    Args:
        url (str): URL of API endpoint (default empty).
        key (str): API auth token (default None).

    Returns:
        A list of protobuf entities. 

    Raises:
        ValueError: If response is invalid or missing required field.
    """

    ## make request
    response = rq.get(
        url = url,
        headers = key
    )
    logging.debug(msg = 'Client GET request to {x} completed successfully.'.format(
        x = url
        )
    )

    ## parse protobuf
    message = gtfs_realtime_pb2.FeedMessage()
    message.ParseFromString(response.content)
    logging.debug(msg = 'Client successfully parsed protobuf from {x}.'.format(
        x = url
        )
    )

    ## validate header
    if (message.header.gtfs_realtime_version == '2.0' or \
        message.header.gtfs_realtime_version == '1.0' or \
        message.header.gtfs_realtime_version == '0.1') and \
        message.header.incrementality == gtfs_realtime_pb2.FeedHeader.FULL_DATASET:
        logging.debug(msg = 'Client successfully validated protobuf header from {x}.'.format(
            x = url
            )
        )

        ## validate entity
        entity_valid = [i for i in message.entity if (
            i.vehicle.vehicle.id and \
            i.vehicle.timestamp and \
            i.vehicle.position.latitude and \
            i.vehicle.position.longitude and \
            (i.vehicle.trip.route_id or i.vehicle.trip.trip_id)
            )
        ]
        logging.debug(msg = 'Client successfully validated message entity from {x}.'.format(
            x = url
            )
        )

        ## output message validation
        del message.entity[:]
        message.entity.extend(entity_valid)
        logging.info(msg = 'Client successfully processed GET request.')
    return message.entity

## parse ids
def set_ids(feed):

    """ 
    Desc: 
        Extracts unique IDs from the vehicle object in a protobuf feed and 
        returns them as a set.
        
    Args:
        feed (object): protobuf

    Returns:
        A set.

    Raises:
        None.
    """
    
    return set(
        [i.vehicle.vehicle.id for i in feed]
    )

## exclude ids
def exd_ids(feed_x, ids_x):

    """
    Desc:
        Returns a list of entities from a given feed that do not have a 
        vehicle ID in a list of excluded IDs.

    Args:
        feed_x (list): A list of entity objects to filter.
        ids_x (list): A list of vehicle IDs to exclude.

    Returns:
        A list of entity objects from `feed_x` whose vehicle ID is not in 
        `ids_x`.

    Raises:
        None.
    """

    return [i for i in feed_x if i.vehicle.vehicle.id not in ids_x]

## omit dupl and empty ids
def del_ids(feed):

    """
    Desc: 
        Removes duplicate and empty vehicle IDs from a valid protobuf feed 
        and returns a list of the unique vehicles.

    Args:
        feed (object): A protobuf feed containing entities.

    Returns:
        A list of protobuf entities with unique IDs.

    Raises:
        None.
    """

    feed = [
        i for i in feed if 
            i.vehicle.vehicle.id and \
            (i.vehicle.trip.trip_id or i.vehicle.trip.route_id) and \
            i.vehicle.position.latitude and \
            i.vehicle.position.longitude and \
            i.vehicle.timestamp
        ]

    return list(
        {i.vehicle.vehicle.id: i for i in feed}.values()
    )

## find idle events
def feed_idle(buffer, feed_h, move_k, move_m, time_h):
    
    """
    Desc:

    Args:
        buffer (list): array of protobufs (default empty).
        feed_h (list): array of protobufs (default empty).
        move_k (dict): dictionary of counters (default empty).
        move_m (pos int): number of times to omit events (default empty).
        time_h (pos int): time-horizon interval (default empty).

    Returns:
        2 lists. List 1 is the feed Y. List 2 is feed H.

    Raises:
        ValueError: 'GTFS feeds A and B not of equal length.'
        
    """

    ## init feeds
    try:
        feed_a, feed_b, feed_c = buffer[0], buffer[time_h], buffer[time_h + 1]
        logging.debug(msg = 'Client successfully initialized sets A, B, and C.')

    except Exception as e:
        logger.error(msg = 'Client failed to initialized sets A, B, C: {x}.'.format(
            x = e
            )
        )

    ## omit dupl and empty ids
    feed_a = del_ids(feed = feed_a)
    feed_b = del_ids(feed = feed_b)
    feed_c = del_ids(feed = feed_c)

    ## intersect of feed a and feed b from symmet diff
    ids_a = set_ids(feed = feed_a)
    ids_b = set_ids(feed = feed_b)
    ids_w = ids_a.symmetric_difference(ids_b)
    if len(ids_w) > 0:
        feed_a = exd_ids(
            feed_x = feed_a, 
            ids_x = ids_w
        )
        feed_b = exd_ids(
            feed_x = feed_b, 
            ids_x = ids_w
        )

    ## find events for feed h from intersect of feed a and feed b
    time_d = list()
    for a, b in zip(feed_a, feed_b):
        if a.vehicle.vehicle.id == b.vehicle.vehicle.id and \
        ((a.vehicle.trip.trip_id == b.vehicle.trip.trip_id if hasattr(a.vehicle.trip, 'trip_id') and hasattr(b.vehicle.trip, 'trip_id') else True) or 
        (a.vehicle.trip.route_id == b.vehicle.trip.route_id if hasattr(a.vehicle.trip, 'route_id') and hasattr(b.vehicle.trip, 'route_id') else True)) and \
        a.vehicle.position.latitude == b.vehicle.position.latitude and \
        a.vehicle.position.longitude == b.vehicle.position.longitude and \
        a.vehicle.timestamp < b.vehicle.timestamp:
            
            ## filter for unique events in feed h
            idle_h = next((i for i in feed_h
                if i.vehicle.vehicle.id == b.vehicle.vehicle.id and \
                ((i.vehicle.trip.trip_id == b.vehicle.trip.trip_id if hasattr(i.vehicle.trip, 'trip_id') and hasattr(b.vehicle.trip, 'trip_id') else True) or 
                (i.vehicle.trip.route_id == b.vehicle.trip.route_id if hasattr(i.vehicle.trip, 'route_id') and hasattr(b.vehicle.trip, 'route_id') else True)) and \
                i.vehicle.position.latitude == b.vehicle.position.latitude and \
                i.vehicle.position.longitude == b.vehicle.position.longitude),
                None
            )
            if idle_h is not None:
                if idle_h.vehicle.timestamp > b.vehicle.timestamp:
                    continue
            else:
                feed_h.append(b)

                ## compute time lag of telemtry
                if len(feed_h) > 0:
                    time_g = int(b.vehicle.timestamp) - int(a.vehicle.timestamp)
                    if time_g > time_h:
                        time_d.append({
                            'vehicle_id': b.id,
                            'duration': time_g - time_h
                        }
                    )

    ## intersect of feed h and feed c from symmet diff
    ids_h = set_ids(feed = feed_h)
    ids_c = set_ids(feed = feed_c)
    ids_z = ids_h.symmetric_difference(ids_c)
    if len(ids_z) > 0:
        feed_c = exd_ids(
            feed_x = feed_c,
            ids_x = ids_z
        )

    ## init feed c attr
    attr_c = {(
        i.vehicle.vehicle.id,
        i.vehicle.trip.trip_id if hasattr(i.vehicle.trip, 'trip_id') else None,
        i.vehicle.trip.route_id if hasattr(i.vehicle.trip, 'route_id') else None,
        i.vehicle.position.latitude,
        i.vehicle.position.longitude
        ) for i in feed_c
    }

    ## keep count of times feed h attr not in feed c attr
    for i in feed_h:
        attr_h = (
            i.vehicle.vehicle.id,
            i.vehicle.trip.trip_id if hasattr(i.vehicle.trip, 'trip_id') else None,
            i.vehicle.trip.route_id if hasattr(i.vehicle.trip, 'route_id') else None,
            i.vehicle.position.latitude,
            i.vehicle.position.longitude
        )

        ## init counter
        if attr_h not in move_k:
            move_k[attr_h] = 0

        ## increment counter
        if attr_h not in attr_c:
            move_k[attr_h] += 1

        ## reset counter
        else:
            move_k[attr_h] = 0

        ## omit events from feed h when not in feed c, m number of times
        if move_k.get(attr_h, 0) >= move_m:
            feed_h.remove(i)
            move_k.pop(attr_h, None)

    ## intersect of feed h and feed c
    feed_y = list()
    for i in feed_h:
        for j in feed_c:
            if i.vehicle.vehicle.id == j.vehicle.vehicle.id and \
            ((i.vehicle.trip.trip_id == j.vehicle.trip.trip_id if hasattr(i.vehicle.trip, 'trip_id') and hasattr(j.vehicle.trip, 'trip_id') else True) or 
            (i.vehicle.trip.route_id == j.vehicle.trip.route_id if hasattr(i.vehicle.trip, 'route_id') and hasattr(j.vehicle.trip, 'route_id') else True)) and \
            i.vehicle.position.latitude == j.vehicle.position.latitude and \
            i.vehicle.position.longitude == j.vehicle.position.longitude and \
            i.vehicle.timestamp < j.vehicle.timestamp:

                ## create idle event
                idle_y = {
                    'iata_id': j.vehicle.vehicle.label,
                    'vehicle_id': j.vehicle.vehicle.id,
                    'trip_id': j.vehicle.trip.trip_id if hasattr(j.vehicle.trip, 'trip_id') else None,
                    'route_id': j.vehicle.trip.route_id if hasattr(j.vehicle.trip, 'route_id') else None,
                    'latitude': j.vehicle.position.latitude,
                    'longitude': j.vehicle.position.longitude,
                    'datetime': j.vehicle.timestamp,
                    'duration': int(j.vehicle.timestamp) - int(i.vehicle.timestamp)
                }

                ## add time lag of telemetry
                time_y = next(
                    (k for k in time_d if k['vehicle_id'] == idle_y['vehicle_id']), 
                    None
                )
                if time_y is not None:
                    idle_y['duration'] = int(
                        idle_y['duration'] + time_y['duration']
                    )

                ## add idle event to final output
                if idle_y['duration'] > 0:  ## ensure no time sync errors
                    feed_y.append(idle_y)

    ## idle event feeds
    return feed_y, feed_h

## find idle events
def find_idle(url, key = None, time_r = 30, time_h = 1, move_m = 10, loop_n = None):

    """
    Desc:
        Generator function that returns a list of idle events from a GTFS 
        realtime feed.

    Args:
        url (str): API end point.
        key (str): API auth key (default None).
        time_r (pos int): seconds between requests (default 30).
        time_h (pos int): time-horizon interval (default 1).
        move_m (pos int): number of times to omit events (default 10).
        loop_n (pos int): limit number of iterations (default None).

    Returns:
        Generator object.

    Raises:
        None.
    """

    ## init buffer
    buffer = list()
    t_cap = time_h + 1
    t = 0

    ## init feed h and move c
    feed_h = list()
    move_k = dict()
    
    ## cont buffer
    while True:

        ## fill buffer
        try:
            response = get_req_par(
                url = url,
                key = key
            )

            buffer.append(
                response
            )

        ## skip iter
        except Exception as e:
            logger.error(msg = e)
            continue

        ## limit buffer length
        if t > t_cap:
            del buffer[0]

            ## compute idle events
            idle_y, feed_h = feed_idle(
                buffer = buffer,  ## feed a, feed b, feed c
                feed_h = feed_h,
                move_m = move_m,
                move_k = move_k,
                time_h = time_h
            )

            ## return generator object
            yield json.dumps(
                obj = idle_y,
                indent = 2
            )

        ## increment time
        t += 1

        ## limit number of loops
        if loop_n is not None and t == loop_n:
            break
        
        ## limit request rate
        time.sleep(time_r)

## end of program