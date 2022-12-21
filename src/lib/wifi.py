import network
from lib.secrets import WIFI_NETWORKS


class WiFi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self) -> bool:
        if self.wlan.isconnected():
            return True

        self.wlan.active(True)
        self.wlan.config(
            reconnects=3
        )  # can only configure after activating the interface, see https://forum.micropython.org/viewtopic.php?t=11445&p=62604
        print("Scanning WiFi networks...")
        networks = self.wlan.scan()
        print("Networks in vicinity: ", networks)
        KNOWN_SSIDS = [ssid for ssid, _ in WIFI_NETWORKS]
        known_network = None
        try:
            known_network = next(
                (
                    ssid
                    for ssid in [network[0].decode("utf-8") for network in networks]
                    if ssid in KNOWN_SSIDS
                )
            )
        except StopIteration:
            # no known network found
            print("No known networks in range")
            return False

        print("Connecting to: ", known_network)
        ssid, password = [
            network for network in WIFI_NETWORKS if network[0] == known_network
        ][0]
        self.wlan.connect(ssid, password)
        while not self.wlan.isconnected():
            pass
        print("Network configuration: ", self.wlan.ifconfig())
        return True


w = WiFi()
w.connect()
