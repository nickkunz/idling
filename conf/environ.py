## library
import socket

## default
class Env(object):
    DEBUG = False
    TESTING = False
    LOGGING = True

## local machine
class LocalEnv(Env):
    DEBUG = True
    LOGGING = False
    URL = socket.gethostname()

## development server
class DevEnv(Env):
    DEBUG = True
    LOGGING = False

## testing server
class TestEnv(Env):
    TESTING = True

## staging server
class StgEnv(Env):
    DEBUG = False

## production server
class ProdEnv(Env):
    DEBUG = False
