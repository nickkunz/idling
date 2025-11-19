## library
import os

## params
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## host and port (inside container)
bind = "127.0.0.1:8000"

## workers (outbound traffic)
workers = 2
threads = 2

## timeouts
timeout = 300
graceful_timeout = timeout + 5
keepalive = 125

## logging
loglevel = LOG_LEVEL
accesslog = None
errorlog = None
capture_output = True if loglevel == 'DEBUG' else False

## end config