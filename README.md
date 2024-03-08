<div align="center">
  <img src="https://github.com/nickkunz/idling/blob/dev/gui/public/banner.png">
</div>

# GRD-TRT-BUF-4I: Ground Truth Buffer for Idling
An implementation of GRD-TRT-BUF-4I from the paper "Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling." The system detects, stores, and visualizes urban transit bus idling data in realtime. It is designed using containerized microservices and is configurable to deploy on any cloud-based platform. Each microservice is listed below with a brief description.

### Microservices
- __Extract__ (ext): Collects and parses protocol buffers from GTFS Realtime sources.
- __Subset__ (sub): Filters and computes idling data for websocket streaming.
- __Write__ (wrt): Inserts the idling data into persistent storage.
- __Database__ (db): Manages idling data storage and retrieval.
- __Read__ (rdb): Retrieves stored idling data from database. Also contains data tests.
- __Interface__ (gui): Frontend idling data visualization and retrieval.

### Version
<!-- Unnamed Enterprise Edition 1.0.0 --> 
<!-- Via Appia 0.9.X --> 
<!-- Isidore 0.8.X --> 
<!-- Frontinus 0.7.X --> 
<!-- Anthemius 0.6.X --> 
<!-- Vitruvius 0.5.X --> 
<!-- Archimedes 0.4.X --> 
<!-- Qanats 0.3.X --> 
<!-- Eupalinos 0.2.X -->
Imhotep 0.1.X<br>
_Updated: Mar. 2024_

## Dependencies
- Docker Desktop (Latest)
- OS: Ubuntu 20.04
- Language: Python 3.8
- Web App: Flask 2.3.1 / Quart 0.18.3
- WSGI/ASGI: Gunicorn / Uvicorn (Latest)
- Proxy Server: Nginx (Latest)
- Database: PostgreSQL 16
- Frontend: React (17.0.2), Deck GL (8.9.33)

_Note: All dependencies are automatically installed when built with Docker._

## Requirements
- GTFS Realtime API Keys (see: [Extract README](ext/README.md))
- Mapbox Access Token (see: [Interface README](gui/README.md))

## Repository Structure
The repository follows the structure below:
```
├─ ext                   ## extract microservice
├─ gui                   ## interface microservice
├─ rdb                   ## read microservice and data tests
├─ sub                   ## subset microservice
├─ wrt                   ## write microservice
├─ .dockerignore         ## excluded files in docker
├─ .gitignore            ## excluded files in git
├─ docker-compose.yml    ## container orchestration
├─ LICENSE               ## software license
├─ README.md             ## documentation
```

### Backend
Each backend microservice is structured to follow the pattern below:
```
├─ ...
├─ abc
│   ├─ conf              ## config files
│   ├─ src               ## source code
│   ├─ test              ## test code
│   ├─ .env.example      ## env vars
│   ├─ app.py            ## main app
│   ├─ Dockerfile        ## container
│   ├─ README.md         ## documentation
│   ├─ requirements.txt  ## dependencies
│   └─ start.sh          ## startup script
├─ ...
```
### Frontend
The frontend microservice follows the structure below:
```
├─ ...
├─ gui
│   ├─ conf              ## config files
│   ├─ public            ## test code
│   ├─ src               ## source code
│   ├─ .env.example      ## env vars
│   ├─ Dockerfile        ## container
│   ├─ package-lock.json ## dependencies
│   ├─ package.json      ## dependencies
│   ├─ README.md         ## documentation
│   └─ start.sh          ## startup script
├─ ...
```

## Installation
0. __Acquire API Keys__

    There are two categories of API keys that are required. More information on how to obtain them is here:
    - GTFS Realtime API Keys (see: [Extract README](ext/README.md))
    - Mapbox Access Token (see: [Interface README](gui/README.md)).

1. __Install Docker__

    Ensure that Docker Desktop is installed on your local machine. You can download it here: 

    https://docs.docker.com/get-docker/


2. __Clone Repository__

    Clone this repository to a directory on your local machine.
    ```bash
    git clone
    ```

    Navigate to the project folder.
    ```
    cd <path to project folder>
    ```

3. __Build Container Images__

    Build the container images.
    ```bash
    docker-compose up --build
    ```

    This command will also run the container images for each microservice, including the database.
    
    It may take awhile to complete the build process for each microservice.

## Port Conventions
The design pattern follows these port conventions:
- `8080`: __Extract__ (ext)
- `7080`: __Subset__ (sub)
- `6080`: __Write__ (wrt)
- `5432`: __Database__ (db)
- `4080`: __Read__ (rdb)
- `3080`: __Interface__ (int)

## Usage
1. __Connect to Websocket__

    Ensure the __Extract__ and __Subset__ microservices are running. Use an API client like <a href="https://www.postman.com">Postman</a> or similar and connect to the endpoint `ws://localhost:7080` using __Socket.IO__. 
    
    Listen for the __Events__ titled `events`. There should be a continuous stream of idling data every 30 seconds in the following format:
    ```json
    {
        "iata_id": "",
        "vehicle_id": "",
        "route_id": "",
        "trip_id": "",
        "latitude": 0.01,
        "longitude": -0.01,
        "datetime": 123,
        "duration": 123
    }
    ```

4. __Read Database__

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
    http://localhost:4080/idling?format=csv&iata_id=NYC
    ```

    or to retrieve all idling events in Montreal longer than 5 minutes in GeoJSON format:
    ```
    http://localhost:4080/idling?format=geojson&iata_id=YUL&min_duration=300
    ```

4. __Browse Interface__

    Ensure the __Interface__ microservice is running. Navigate to `http://localhost:3080` in your browser to access the frontend interface.

## Citations
```
@article{Kunz_2024,
  title         = {{Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling}},
  author        = {Nichlas Kunz and H. Oliver Gao},
  eprint        = {2403.03489},
  year          = {2024},
  archivePrefix = {arXiv},
  primaryClass  = {eess.SY},
  howpublished  = "\url{https://arxiv.org/abs/2403.03489}"
}
```
```
@misc{GRD-TRT-BUF-4I_2023,
  title         = {{GRD-TRT-BUF-4I: Ground Truth Buffer for Idling}},
  author        = {Nicholas Kunz},
  year          = {2023},
  publisher     = {Github},
  version       = {Imhotep 0.1.0},
  url           = {https://github.com/nickkunz/idling},
  copyright     = {GPL v3.0}
}
```

## Contributions

GRD-TRT-BUF-4I is open for improvements and maintenance. Your help is valued to make the system better for everyone.

## Contacts
Nick Kunz, Cornell University: nhk37@cornell.edu

## License

© Nick Kunz, 2024. Licensed under the General Public License v3.0 (GPLv3).

## References
Kunz, N., Gao, H. O. (2024). Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling. Preprint. _arXiv:5451982_ [eess.SY]. https://arxiv.org/abs/2403.03489.
