import os
import asyncio
from pylutron_caseta.smartbridge import Smartbridge
from pylutron_caseta.cli import async_pair
from prometheus_client import Gauge, start_http_server

DEVICE_TYPE_MAP = {
   'light': {'DivaSmartDimmer', 'DivaSmartSwitch', 'PlugInDimmer'},
   'sensor': {'RPSOccupancySensor'},
   'shade': {'SerenaHoneycombShade'}
}

device_guage = Gauge('lutron_device', '', ['id', 'name', 'type', 'product_type', 'device_name'])

async def pair(host, data_dir):
    def _ready():
        print("Press the small black button on the back of the bridge.")
    
    data = await async_pair(host, _ready)
    with open(os.path.join(data_dir, "caseta-bridge.crt"), "w") as cacert:
        cacert.write(data["ca"])
    with open(os.path.join(data_dir, "caseta.crt"), "w") as cert:
        cert.write(data["cert"])
    with open(os.path.join(data_dir, "caseta.key"), "w") as key:
        key.write(data["key"])
    print(f"Successfully paired with {data['version']}")



async def main():
    host = os.getenv('LUTRON_HOST')
    data_dir = os.getenv('DATA_DIR', 'data')
    
    if not host:
      print('Set LUTRON_HOST to Smart Bridge IP address')   
      exit(1)
    
    print(f'host={host}, data_dir={data_dir}')

    if not os.path.exists(os.path.join(data_dir, 'caseta.key')):
      await pair(host, data_dir)

    bridge = Smartbridge.create_tls(
        host,
        os.path.join(data_dir, "caseta.key"),
        os.path.join(data_dir, "caseta.crt"), 
        os.path.join(data_dir, "caseta-bridge.crt")
    )
    await bridge.connect()

    while True:
      devices = bridge.get_devices()
      for device in devices.values():
        device_type = 'other'
        for dtype, products in DEVICE_TYPE_MAP.items():
          if device['type'] in products:
              device_type = dtype

        device_guage.labels(
          device['device_id'],
          device['name'],
          device_type,
          device['type'],
          device['device_name'],
        ).set(device['current_state'])

      await asyncio.sleep(30)

if __name__ == '__main__':
  start_http_server(8080)
  asyncio.run(main())