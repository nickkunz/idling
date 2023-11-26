## libraries
import os
import sys
from quart import Quart, Response

## source
sys.path.insert(0, './')
from .src.extract import ExtractClient

## params
INI_FILE = str(os.getenv(key = 'INI_PATH', default = '/app/ext/conf/feed/ww-full.ini'))
INI_SECT = str(os.getenv(key = 'INI_SECT', default = 'api'))
ENV_FILE = str(os.getenv(key = 'ENV_FILE', default = './ext/.env'))
LOG_LEVEL = str(os.getenv(key = 'LOG_LEVEL', default = 'INFO'))

## app
app = Quart(import_name = __name__)

## logging
app.logger.propagate = False
app.logger.setLevel(level = LOG_LEVEL)
app.debug = True if LOG_LEVEL == 'DEBUG' else False

## client instance
client = ExtractClient(
    env_file = ENV_FILE,
    ini_file = INI_FILE,
    ini_sect = INI_SECT
)

## test app
@app.route(rule = '/', methods = ['GET'])
def test():
    app.logger.info(msg = 'Client application layer tested sucessfully.')
    return Response(
        response = None,
        status = 200
    )

## extract data
@app.route(rule = '/extract', methods = ['GET'])
async def extract():
    response, status, headers = await client.run()
    app.logger.info(msg = 'Client application layer executed sucessfully.')
    return Response(
        response = response,
        status = status,
        headers = headers
    )

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run()

## end application