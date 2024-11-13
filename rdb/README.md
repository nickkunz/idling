# GRD-TRT-BUF-4I: Read Microservice

## Dependencies
1. OS: Ubuntu 20.04 LTS (Focal Fossa)
2. Language: Python 3.8 
3. Web App: Flask 2.3.1
4. WSGI: Gunicorn (Latest)
5. Reverse Proxy: Nginx (Latest)

## Getting Started
Ensure the __Read__ and __Database__ microservices are running and have had sufficient time to collect an historical record of data.

Using the endpoint `http://localhost:4080/` specify one of the three following routes:
- `/agency`: Retrieves transit agency table.
- `/events`: Retrieves idling events table
- `/idle`: Joins agency table with events table.

Parameters for each route can be specified as such:
- `format`: `geojson` or `csv` (e.g. `format=csv`).
- `iata_id`: IATA code of transit agency (e.g. `iata_id=NYC`).

Additional parameters that apply to the `/agency` and `/idle` routes:
- `agency`: Name of transit agency.
- `city`: City of transit agency.
- `country`: Country of transit agency.
- `region`: Region of transit agency.
- `continent`: Continent of transit agency.

Additional parameters that apply to `/events` and `/idle` routes:
- `vehicle_id`: Vehicle ID of idling events.
- `route_id`: Route ID of idling events.
- `trip_id`: Trip ID of idling events.
- `datetime`: POSIX time of idling events.
- `start_datetime`: Start POSIX time of idling events.
- `end_datetime`: End POSIX time of idling events.
- `duration`: Duration of idling events (seconds).
- `min_duration`: Minimum duration of idling events (seconds).
- `max_duration`: Maximum duration of idling events (seconds).

For example, to retrieve all idling events in New York City in CSV format:
```
http://localhost:4080/idle?format=csv&iata_id=NYC
```

or to retrieve all idling events in Montreal longer than 5 minutes in GeoJSON format:
```
http://localhost:4080/idle?format=geojson&iata_id=YUL&min_duration=300
```
