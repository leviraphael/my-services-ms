## Usage

Before deployment you need to create azure secret to access to your ACR

```bash
kubectl create secret docker-registry <secret-name> \
    --namespace <namespace> \
    --docker-server=<container-registry-name>.azurecr.io \
    --docker-username=<service-principal-ID> \
    --docker-password=<service-principal-password>
```

Replace in your [yaml file](https://github.com/leviraphael/my-services-ms/blob/main/k8s/services.yaml) the docker images and secret to access to your ACR

```bash
 containers:
      - name: service1
        image: <serviceA_image>
```


```bash
 containers:
      - name: service1
        image: <serviceA_image>
```

```bash
      imagePullSecrets:
      - name: <azure-secret>
```
