## library
import os
from multiprocessing import cpu_count

## params
LOG_LEVEL = os.getenv(key = 'LOG_LEVEL', default = 'INFO')

## host and port (inside container)
bind = "127.0.0.1:8000"

## number of workers (outbound traffic)
workers = cpu_count()  ## sufficient for multiple clients
threads = workers * 2

## resouce limits
max_requests = 20  ## restart worker after 10mins, given 30s per request
max_requests_jitter = 33  ## avoid worker restart at the same time

## timeouts
timeout = 30
graceful_timeout = timeout + 5

## logging
loglevel = LOG_LEVEL
accesslog = None
errorlog = '-'
capture_output = True if loglevel == 'DEBUG' else False

## end config