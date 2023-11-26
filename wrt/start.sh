#!/bin/sh
set -e
/etc/init.d/nginx start
gunicorn -c /etc/gunicorn/gunicorn.conf.py wrt.app:app &
sleep 5
curl http://host.docker.internal:6080/write
wait