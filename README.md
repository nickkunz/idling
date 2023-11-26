# GRD-TRT-BUF-4I: Ground Truth Buffer for Idling
Main Description

## Dependencies
1. OS: Ubuntu 20.04
2. Language: Python 3.8
3. Web App: Flask/Quart
4. WSGI/ASGI: Gunicorn/Uvicorn
5. Proxy Server: Nginx
6. Database: PostGIS (PostgreSQL)
7. Interface: Streamlit

## Getting Started
1. Install Docker
2. Clone Repository
3. Build Docker Image
4. Run Docker Container

### Repo Structure
The repository follows the structure below:
```
├─ ext                   ## extract microservice
├─ sub                   ## subset microservice
├─ wrt                   ## write microservice
├─ .dockerignore         ## excluded file types in docker image
├─ .gitignore            ## excluded file types in version control
├─ docker-compose.yml    ## container orchestration
├─ LICENSE               ## software license
├─ README.md             ## documentation
```

Each microservice is structured to follow the pattern below:
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

### Port Convention of Microservices
- 8xxx: Extract (ext)
- 7xxx: Subset (sub)
- 6xxx: Write (wrt)
- 5xxx: Database (db)
- 4xxx: Interface (int)

stop and remove all images including running containers
docker rmi -f $(docker images -a -q)

extract-base is never actually run by Docker Compose. Instead, it serves as a shared configuration for the other services. 


Docker Commands
docker-compose up --build
docker-compose up -d --build ## detached mode
docker-compose up build --no-cache ## no cache mode

docker-compose down ## stop and remove containers, networks, images, and volumes
docker rmi $(docker images -q) ## remove all images
docker rmi -f $(docker images -q) ## remove all images (force)

docker system prune
