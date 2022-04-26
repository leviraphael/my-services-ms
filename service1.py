import enum
import json
import time
import traceback

import requests
from fastapi import FastAPI
from requests import Response


class Currency(enum.Enum):
    USD = 0
    EUR = 1


class BitcoinRequests:
    base_url: str = 'https://api.alternative.me/v2/ticker/bitcoin/'

    def get(self, params: str):
        return requests.get(f'{self.base_url}?{params}')


class BitcoinConverter:
    _bc_requests: BitcoinRequests = BitcoinRequests()

    def convert(self, currency: Currency) -> Response:
        res = self._bc_requests.get(f'convert={currency.name}')
        return (int)(json.loads(res.content)['data']['1']['quotes'][currency.name]['price'])

    def convert_to_usd(self):
        return self.convert(currency=Currency.USD)


app = FastAPI()
_bc_converter = BitcoinConverter()

@app.get("/")
def root():
    return {"Welcome"}


@app.get("/convert/{currency}")
def convert(currency: str):
    try:
        c = Currency[currency.upper()]
        response = _bc_converter.convert(c)
        write_to_log(str(response))
        return response
    except:
        return {f"Error is {traceback.format_exc()} Cannot find currency in lists supported is only {list(map(lambda c: c.name, Currency))}"}


def write_to_log(message=""):
    with open("log.txt", mode="a") as log:
        content = f"[{int(time.time())}] [{message}]\n"
        log.write(content)
