## library
from multiprocessing import cpu_count

## host and port
bind = "127.0.0.1:8000"

## number of workers
workers = cpu_count() * 2 + 1
threads = workers * 2
timeout = 90
keepalive = 120
