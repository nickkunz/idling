# GRD-TRT-BUF-4I: Ground Truth Buffer for Idling
This is an implementation of GRD-TRT-BUF-4I from the research in "Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling." The system detects, stores, and visualizes urban transit bus idling data in realtime. The microservice system is containerized and designed to be locally tested and configurable to deploy on a cloud-based platform.

### Microservices
- __Extract__ (ext): Collects protocol buffers from GTFS Realtime sources.
- __Subset__ (sub): Filters and computes idling data for websocket streaming and storage.
- __Write__ (wrt): Stores the idling data in a database for retrieval.
- __Database__ (db): Manages idling data storage and retrieval.
- __Read__ (rdb): Retrieves data from the database for visualization and consumption.
- __Interface__ (gui): Frontend data visualization and general project information.

### Version
Imhotep 0.1.0<br>
_Updated: Feb. 2024_

## Dependencies
1. OS: Ubuntu 20.04
2. Language: Python 3.8
3. Web App: Flask/Quart
4. WSGI/ASGI: Gunicorn/Uvicorn
5. Proxy Server: Nginx
6. Database: PostgreSQL 16
7. Interface: Node JS, React, Deck GL

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

### Port Conventions
The design pattern follows the port conventions below:
- `8080`: Extract (ext)
- `7080`: Subset (sub)
- `6080`: Write (wrt)
- `5432`: Database (db)
- `6180`: Read (db)
- `80`: Interface (int)

## Contributions

GRD-TRT-BUF-4I is open for improvements and maintenance. Your help is valued to make the system better for everyone.

## Contacts
* Nick Kunz: nhk37@cornell.edu
* H. Oliver Gao: hg55@cornell.edu

## License

© Nick Kunz, 2024. Licensed under the General Public License v3.0 (GPLv3).

## References
Kunz, N., Gao, H. O. (2024). Global Geolocated Realtime Data of Interfleet Urban Transit Bus Idling. _In Preparation._