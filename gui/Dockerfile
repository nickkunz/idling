## base image
FROM ubuntu:20.04

## auth container images
ARG DOCKER_CONTENT_TRUST=1

## suppress dialog
ARG DEBIAN_FRONTEND=noninteractive

## install dependencies
RUN apt-get clean &&\
    apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y curl software-properties-common &&\
    curl -sL https://deb.nodesource.com/setup_20.x | bash - &&\
    apt-get install -y nodejs\
    nginx

## reduce dependencies
RUN apt-get autoremove -y &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

## remove server default configs
RUN rm /etc/nginx/nginx.conf &&\
    rm /etc/nginx/sites-enabled/default

## copy server configs
COPY ./gui/conf/nginx.conf /etc/nginx/

## symlink server configs
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/

## set working directory
WORKDIR /app/gui

## copy script
COPY . /app

## install nodejs libraires and build
ENV NODE_OPTIONS=--max-old-space-size=4096
RUN npm cache clean --force &&\
    npm install

## create non-root user and permissions
RUN groupadd -g 999 group &&\
    useradd -u 999 -g group -d /home/user -m -s /bin/bash user &&\
    chown -R user:group /var/lib/nginx /var/log/nginx /etc/nginx /run /app/gui

## run non-root user
USER user

## open port
EXPOSE 3080

## run application
ENTRYPOINT ["bash", "./start.sh"]
