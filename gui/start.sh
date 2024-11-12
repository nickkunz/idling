#!/bin/sh
/etc/init.d/nginx start
npm run build
tail -f /dev/null