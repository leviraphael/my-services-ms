import time

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from bicointer_converter import BitcoinConverter
from redis_util import RedisUtil

app = FastAPI()
_bc_converter = BitcoinConverter()
ru = RedisUtil()
average = 0
bc_rate_every_2sec = 0


@app.get("/current", status_code=200)
def get_btc_rate():
    return bc_rate_every_2sec


@app.get("/average")
def get_current_avg():
    return average


@app.on_event('startup')
@repeat_every(seconds=60*10)
def get_average():
    conn = ru.connect_to_redis()
    lst = conn.mget(conn.keys())
    print(f'all values are {lst}')
    conn.flushall()
    _get_average(lst)
    print(f'average is { int(average) }')


@app.on_event('startup')
@repeat_every(seconds=10)
def get_current_btc_rate():
    global bc_rate_every_2sec
    current = int(time.time())
    try:
        bc_rate_every_2sec = _set_btc_rate(current)
    except Exception as e:
        print(f'cannot get value at {current} got exception {e}')
    return {"200"}


def _set_btc_rate(current):
    r = ru.connect_to_redis()
    btc_rate = _bc_converter.convert_to_usd()
    r.set(current, btc_rate)
    return btc_rate


def _get_average(lst):
    global average
    total = sum([int(i) for i in lst if type(i) == int or i.isdigit()])
    average = total / len(lst)
