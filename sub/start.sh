#!/bin/sh
/etc/init.d/nginx start
gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -c /etc/gunicorn/gunicorn.conf.py sub.app:app