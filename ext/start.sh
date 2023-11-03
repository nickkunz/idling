#!/bin/sh
set -e
/etc/init.d/nginx start
gunicorn -k uvicorn.workers.UvicornWorker -c /etc/gunicorn/gunicorn.conf.py ext.app:app --log-level=$(echo ${LOG_LEVEL:-INFO} | tr '[:upper:]' '[:lower:]') --access-logfile - --access-logformat ""