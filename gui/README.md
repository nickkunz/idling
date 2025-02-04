# GRD-TRT-BUF-4I: Interface Microservice

__Version__: 0.1.3<br>
__Updated__: November 2024

## Dependencies
- OS: Ubuntu 20.04 LTS (Focal Fossa)
- Language: JavaScript (V8 v11.3, Chromium 113)
- Web App: Node.js 20.9.0 (Iron)
- Reverse Proxy: Nginx (Latest)

## Requirements
- Mapbox Access Token

## Getting Started
1. Obtain a Mapbox Access Token here: https://docs.mapbox.com/help/getting-started/access-tokens/

2. Using the `.env.example` file in the `./gui` service folder, rename it to `.env` and create an environment variable with your Mapbox Access Token: `REACT_APP_MAPBOX_TOKEN=<your token here>`.

3. Build and execute the Docker container using the following command:
```
docker-compose up --build -d interface
```