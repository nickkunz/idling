## libraries
import sys
from quart import Quart, Response

## modules
sys.path.insert(0, './')
from .src.extract import ExtractData
from conf.environ import LocalEnv

## app
app = Quart(__name__)

## test route
@app.route('/', methods = ['GET'])
def test():
    return Response(status = 200)

## extract data from source
@app.route('/extract', methods = ['GET'])
async def extract():
    return await ExtractData(
        env_file = './.env',
        ini_file = './conf/us-east.ini',
        ini_sect = 'url_dat_src'
    ).ext_dat()

## run app (does not run with gunicorn)
# if __name__ == '__main__':
#     app.run(
#         debug = LocalEnv.DEBUG,
#         host = LocalEnv.URL,
#         port = 8000
#     )
