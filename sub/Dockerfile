## base image
FROM ubuntu:20.04

## auth container images
ARG DOCKER_CONTENT_TRUST=1

## suppress dialog
ARG DEBIAN_FRONTEND=noninteractive

## default log level
ENV LOG_LEVEL=INFO

## install dependencies
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y curl software-properties-common
RUN apt-get install -y --no-install-recommends --fix-missing\
    python3-pip\
    gunicorn\
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
COPY ./sub/conf/nginx.conf /etc/nginx/
COPY ./sub/conf/gunicorn.conf.py /etc/gunicorn/

## symlink server configs
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

## create non-root user and permissions
RUN groupadd -g 999 group &&\
    useradd -u 999 -g group -d /home/user -m -s /bin/bash user &&\
    chown -R user:group /var/lib/nginx /var/log/nginx /etc/nginx /run

## set working directory
WORKDIR /app

## copy application
COPY . /app

## install python libraires
RUN pip3 install -r ./sub/requirements.txt

## open port
EXPOSE 7080

## run non-root user
USER user

## run application
ENTRYPOINT ["bash", "./sub/start.sh"]

## end container