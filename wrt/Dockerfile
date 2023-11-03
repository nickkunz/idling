## base image
FROM ubuntu:20.04

## auth container images
ARG DOCKER_CONTENT_TRUST=1

## suppress dialog
ARG DEBIAN_FRONTEND=noninteractive

## install dependencies
RUN apt-get update &&\
    apt-get upgrade -y &&\
    apt-get install -y curl software-properties-common
RUN apt-get install -y --no-install-recommends --fix-missing\
    python3-pip

## upgrade pip
RUN pip3 install --upgrade --no-cache-dir pip

## reduce dependencies
RUN apt-get autoremove -y &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

## create non-root user and permissions
RUN groupadd -g 999 group &&\
    useradd -u 999 -g group -d /home/user -m -s /bin/bash user

## set working directory
WORKDIR /scp

## copy script
COPY . /scp

## install libraires
RUN pip3 install -r ./wrt/requirements.txt

## run non-root user
USER user

## run application
ENTRYPOINT ["bash", "./wrt/start.sh"]

## end container