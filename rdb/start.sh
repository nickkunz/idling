#!/bin/sh
/etc/init.d/nginx start
gunicorn -c /etc/gunicorn/gunicorn.conf.py rdb.app:app