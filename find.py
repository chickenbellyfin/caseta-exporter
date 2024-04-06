from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from zeroconf import IPVersion


class Listener(ServiceListener):

  def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
    pass

  def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
    pass

  def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
    info = zc.get_service_info(type_, name)
    addresses = info.parsed_addresses(IPVersion.V4Only)
    if len(addresses) > 0:
      print(f"{info.properties[b'SYSTYPE'].decode()}: {addresses[0]}")


zeroconf = Zeroconf()
browser = ServiceBrowser(zeroconf, "_lutron._tcp.local.", Listener())
try:
  input("Press enter to exit...\n\n")
finally:
  zeroconf.close()