# caseta-exporter

Export Lutron Caseta metrics to prometheus

Will export a metric `lutron_device` with labels for each device.

### Build
```
docker build . -t caseta-exporter

docker buildx build --platform linux/arm64,linux/amd64 --tag <registry>/caseta-exporter --push .
```

### Setup

1. Find IP address of Caseta Smart Bridge
```
$ python3 find.py
Press enter to exit...

SmartBridge: 192.168.0.37
```

2. On the first run, press the button on the smart bridge when prompted. It will generate the certificates to the data_dir
```
$ python3 app.py
```

Save the 3 certificates to a dir and mount it to /data when running in docker. This will allow the container to run without having to pair again.


### docker-compose

```
services:
  caseta-exporter:
    container_name: caseta-exporter
    image: caseta-exporter
    environment:
      - LUTRON_HOST=192.168.0.37
    volumes:
      - ./caseta:/data
    ports:
      - 8080:8080
    restart: unless-stopped
```

### promtheus.yml
```
scrape_configs:
  - job_name: 'caseta'
    honor_labels: true
    static_configs:
      - targets: ['caseta-exporter:8080']
```