## Solution explaination

We've used a Bitcoin API to get the current rate

```python
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
```

We've used [FastAPI](https://fastapi.tiangolo.com/) as framework and [Redis](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-overview) as in memory cache service. 

We are using Redis to store the bitcoin rate every 10 seconds 

```python
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
``` 

Then every 10 minutes we calculate the average of these values.

```python
@app.on_event('startup')
@repeat_every(seconds=60*10)
def get_average():
    conn = ru.connect_to_redis()
    lst = conn.mget(conn.keys())
    print(f'all values are {lst}')
    conn.flushall()
    _get_average(lst)
    print(f'average is { int(average) }')
```

Then cleaning the memory cache

```python 
http://localhost/current
```
Return the current Bitcoin rate in USD

```python 
http://localhost/average
```
Return the current average for the last 10 min
