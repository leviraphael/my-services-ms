# Task

Create Kubernetes cluster Using AKS-Engine (on Azure Cloud provider)

Setup K8s cluster with the latest stable version, with RBAC enabled.

The Cluster should have 2 services deployed – Service A and Service B:

Service A is a WebServer that exposes the following:

Current value of Bitcoin in dollar (updated every 10 seconds).

Average value over the last 10 minutes.

Service B is a REST API service, which expose a single controller that responses 200 status code.

Cluster should have nginx Ingress controller deployed, and corresponding ingress rules for Service A and Service B.

Service A should not be able to communicate with Service B.


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

## Docker Deployment 

Create an azure container repository 

Using:

```bash
https://github.com/leviraphael/my-services-ms/azure-pipelines.yml
```
You can create push docker files to your ACR.

To this pipeline we can easily add code inspection like [Pylint](https://pylint.pycqa.org/en/latest/).

Also the unit tests located [here](https://github.com/leviraphael/my-services-ms/unittests) should be run before releasing the Docker.

```python
    # Convert to USD - no Currency error
    def test_convert_to_usd(self):
        res_usd = TestBitcoinConverter._bc_converter.convert(Currency.USD)
        res = TestBitcoinConverter._bc_converter.convert_to_usd()
        # Almost equal in case there is a different convert rate between the 2 calls
        self.assertAlmostEqual(res, res_usd,places=-2)
```

Note we'll use these images to deploy later our Cluster

## Installation

Create a new group

```bash
az group create --location centralus --name k8s-rl
```

Create a Kubernetes Cluster using Azure API (file )

```bash
aks-engine.exe generate "https://github.com/leviraphael/my-services-ms/installations_files/kubernetes.json"
```

It will generate an output directory with all required files to deploy your cluster

Deploy your cluster

```bash
az deployment group create --name k8s-raphael-deploy --resource-group k8s-raphael --template-file "<path_to_output_files>/_output/azuredeploy.json" --parameters "<path_to_output_files>/_output/azuredeploy.parameters.json"
```

Create a Kubernetes Cluster using Azure API

```bash
aks-engine.exe generate .\kubernetes-windows-complete.json
```
Now you can access/ssh your cluster

## Deployment

To manage your cluster deployment it's recommended to use [Helm](https://helm.sh/)

For this exercise I've used kubctl commands to deploy it 

```bash
kubectl apply -f https://github.com/leviraphael/my-services-ms/k8s/services.yaml
kubectl apply -f https://github.com/leviraphael/my-services-ms/k8s/nginx.yaml
```

## Results

It will generate a new deployment including a service connected to 2 replicas (for high availability purpose) with 2 pods (Service A and Service B) 

```bash
http://<ingress_external_ip>/service1/current
http://<ingress_external_ip>/service1/average
http://<ingress_external_ip>/service2/
``` 

Using kubectl we can also manage the auto-scaling per need 
