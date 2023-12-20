# GRD-TRT-BUF-4I: Ground Truth Buffer for Idling
Main Description

## Dependencies
1. OS: Ubuntu 20.04
2. Language: Python 3.8
3. Web App: Flask/Quart
4. WSGI/ASGI: Gunicorn/Uvicorn
5. Proxy Server: Nginx
6. Database: PostgreSQL 16
7. Interface: Streamlit

### Repository Structure
The repository follows the structure below:
```
├─ ext                   ## extract microservice
├─ sub                   ## subset microservice
├─ gui                   ## interface microservice
├─ wrt                   ## write microservice
├─ .dockerignore         ## excluded file types in docker image
├─ .gitignore            ## excluded file types in version control
├─ docker-compose.yml    ## container orchestration
├─ LICENSE               ## software license
├─ README.md             ## documentation
```
## Getting Started (Local Development & Testing)
1. Install Docker
2. Clone Repository
3. Build Container Image
4. Run Container Image

## Kuebernetes Deployment (Staging & Production)
1. Install Kubernetes

### Microservice Pattern
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

The frontend microservice is structured in follow the pattern:
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
- 8xxx: Extract (ext)
- 7xxx: Subset (sub)
- 6xxx: Write (wrt)
- 5xxx: Database (db)
- 80: Interface (int)

## References
