#!/bin/sh
set -e
/etc/init.d/nginx start
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -c /etc/gunicorn/gunicorn.conf.py sub.app:app --log-level=$(echo ${LOG_LEVEL:-INFO} | tr '[:upper:]' '[:lower:]') --access-logfile - --access-logformat ""