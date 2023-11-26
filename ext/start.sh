#!/bin/sh
set -e
/etc/init.d/nginx start
gunicorn -k uvicorn.workers.UvicornWorker -c /etc/gunicorn/gunicorn.conf.py ext.app:app