## libraries
import os
import sys
from quart import Quart, Response

## modules
sys.path.insert(0, './')
from .src.extract import ExtractData

## params
ENV_FILE = './ext/.env'
INI_FILE = str(os.getenv('INI_PATH'))
INI_SECT = str(os.getenv('INI_SECT'))
LOG_LEVEL = str(os.getenv('LOG_LEVEL', 'INFO'))

## app
app = Quart(__name__)
app.debug = False
app.logger.setLevel(LOG_LEVEL)

## test route
@app.route(rule = '/', methods = ['GET'])
def test():
    return Response(
        response = None,
        status = 200
    )

## extract source data
@app.route(rule = '/extract', methods = ['GET'])
async def extract():
    response, status, headers = await ExtractData(
        env_file = ENV_FILE,
        ini_file = INI_FILE,
        ini_sect = INI_SECT
    ).ext_dat()

    return Response(
        response = response,
        status = status,
        headers = headers
    )

## run app (does not execute with gunicorn)
# if __name__ == '__main__':
#     app.run(
#         debug = LocalEnv.DEBUG,
#         host = LocalEnv.URL,
#         port = 8000
#     )
