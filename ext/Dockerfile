## base image
FROM ubuntu:20.04

## auth container images
ARG DOCKER_CONTENT_TRUST=1

## suppress dialog
ARG DEBIAN_FRONTEND=noninteractive

## install dependencies
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y curl software-properties-common &&\
    apt-get install -y --no-install-recommends --fix-missing\
    python3-pip\
    gunicorn\
    uvicorn\
    nginx

## upgrade pip
RUN pip3 install --upgrade --no-cache-dir pip

## reduce dependencies
RUN apt-get autoremove -y &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

## remove server default configs
RUN rm /etc/nginx/nginx.conf &&\
    rm /etc/nginx/sites-enabled/default

## copy server and wsgi configs
COPY ./ext/conf/nginx.conf /etc/nginx/
COPY ./ext/conf/gunicorn.conf.py /etc/gunicorn/

## symlink server configs
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

## create cache directory
RUN mkdir -p /var/cache/nginx/cache

## create non-root user and permissions
RUN groupadd -g 999 group &&\
    useradd -u 999 -g group -d /home/user -m -s /bin/bash user &&\
    chown -R user:group /var/lib/nginx /var/log/nginx /etc/nginx /run /var/cache/nginx/cache /etc/gunicorn/

## set working directory
WORKDIR /app

## copy application
COPY . /app

## install libraires
RUN pip3 install -r ./ext/requirements.txt

## open port
EXPOSE 8080

## run non-root user
USER user

## run application
ENTRYPOINT ["bash", "./ext/start.sh"]

## end container