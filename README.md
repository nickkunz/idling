# GRD-TRT-BUF-4I: Ground Truth Buffer for Idling
This is an implementation of GRD-TRT-BUF-4I from the paper "Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling." The system detects, stores, and visualizes urban transit bus idling data in realtime. The system is designed using containerized microservices and is configurable to deploy on any cloud-based platform. Each microservice is listed below with a brief description.

### Microservices
- __Extract__ (ext): Collects and parses protocol buffers from GTFS Realtime sources.
- __Subset__ (sub): Filters and computes idling data for websocket streaming.
- __Write__ (wrt): Inserts the idling data into persistent storage.
- __Database__ (db): Manages idling data storage and retrieval.
- __Read__ (rdb): Retrieves stored idling data from database.
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
_Updated: Feb. 2024_

## Dependencies
0. Docker Desktop (Latest)
1. OS: Ubuntu 20.04
2. Language: Python 3.8
3. Web App: Flask 2.3.1 / Quart 0.18.3
4. WSGI/ASGI: Gunicorn / Uvicorn (Latest)
5. Proxy Server: Nginx (Latest)
6. Database: PostgreSQL 16
7. Frontend: React (17.0.2), Deck GL (8.9.33)

_Note: All dependencies are installed automatically when built with containers._

## Getting Started
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

    Build the container images using the `docker-compose` command.
    ```bash
    docker-compose up --build
    ```

    This command will also run the container images for each microservice, including the database.
    
    It may take awhile to complete the build process for each microservice.

3. __Connect to Websocket__

4. __Connect to Database__

4. __Browse Interface__

## Repository Structure
The repository follows the structure below:
```
├─ ext                   ## extract microservice
├─ gui                   ## interface microservice
├─ rdb                   ## read microservice
├─ sub                   ## subset microservice
├─ wrt                   ## write microservice
├─ .dockerignore         ## excluded file types in docker
├─ .gitignore            ## excluded file types in git
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

## Port Conventions
The design pattern follows these port conventions:
- `8080`: Extract (ext)
- `7080`: Subset (sub)
- `6080`: Write (wrt)
- `5432`: Database (db)
- `4080`: Read (rdb)
- `3080`: Interface (int)

## Contributions

GRD-TRT-BUF-4I is open for improvements and maintenance. Your help is valued to make the system better for everyone.

## Contacts
Nick Kunz, Cornell University: nhk37@cornell.edu

## License

© Nick Kunz, 2024. Licensed under the General Public License v3.0 (GPLv3).

## References
Kunz, N., Gao, H. O. (2024). Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling. _In Preparation._