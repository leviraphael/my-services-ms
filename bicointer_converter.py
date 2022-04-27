import dataclasses
import enum
import json

import requests
from requests import Response


class Currency(enum.Enum):
    USD = 0
    EUR = 1


@dataclasses.dataclass
class BitcoinRequests:
    base_url: str = 'https://api.alternative.me/v2/ticker/bitcoin/'

    def get(self, params: str):
        return requests.get(f'{self.base_url}?{params}')


@dataclasses.dataclass
class BitcoinConverter:
    _bc_requests: BitcoinRequests = BitcoinRequests()

    def convert(self, currency: Currency) -> Response:
        res = self._bc_requests.get(f'convert={currency.name}')
        return (int)(json.loads(res.content)['data']['1']['quotes'][currency.name]['price'])

    def convert_to_usd(self):
        return self.convert(currency=Currency.USD)
