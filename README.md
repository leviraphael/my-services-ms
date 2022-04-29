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


## Docker Deployment 

Create an azure container repository 

```bash
az acr create --resource-group <resource_group> \
  --name <container_name> --sku Basic
```

Using:

```bash
https://github.com/leviraphael/my-services-ms/blob/main/azure-pipelines.yml
```

Push your docker files to your ACR, change the value with your ACR values you've created previously

```bash
variables:
  # Container registry service connection established during pipeline creation
  dockerRegistryServiceConnection: '<service_connection>'
  imageRepository: '<image_repo>'
  containerRegistry: '<container_name>.azurecr.io'
```

Note: To this pipeline we can easily add code inspection like [Pylint](https://pylint.pycqa.org/en/latest/).

Also the unit tests located [here](https://github.com/leviraphael/my-services-ms/tree/main/unittests) should be run before releasing the Docker.

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
aks-engine.exe generate "https://github.com/leviraphael/my-services-ms/blob/main/installations_files/kubernetes.json"
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
