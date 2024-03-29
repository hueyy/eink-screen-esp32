def get_wifi_status():
    import network

    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        return wlan.ifconfig()

    return False


def get_wifi_networks():
    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
    return networks


def connect_to_wifi() -> bool:
    import network

    wlan = network.WLAN(network.STA_IF)

    if wlan.isconnected():
        print("Already connected")
        print("IP address: ", wlan.ifconfig()[0])
        return True

    print("Enabling WiFi adapter...")
    wlan.active(True)
    wlan.config(
        reconnects=3
    )  # can only configure after activating the interface, see https://forum.micropython.org/viewtopic.php?t=11445&p=62604
    print("Scanning WiFi networks...")
    networks = wlan.scan()
    print("Networks in vicinity: ", networks)

    from lib.secrets import WIFI_NETWORKS

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
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print("Network configuration: ", wlan.ifconfig())
    print("IP address: ", wlan.ifconfig()[0])
    return True


def disconnect_from_wifi():
    import network

    wlan = network.WLAN(network.STA_IF)

    if wlan.isconnected():
        print("Disconnecting from WiFi...")
        wlan.disconnect()

    wlan.active(False)
    print("Disabling WiFi adapter...")


def activate_ap():
    import network

    ap = network.WLAN(network.AP_IF)

    from lib.secrets import AP_CREDENTIALS

    ap.config(
        ssid=AP_CREDENTIALS[0], key=AP_CREDENTIALS[1], security=network.AUTH_WPA2_PSK
    )
    ap.ifconfig(("192.168.10.1", "255.255.255.0", "192.168.10.1", "192.168.10.1"))
    ap.config(max_clients=3)
    ap.active(True)
    return ap


def deactivate_ap(ap):
    ap.active(false)
    return


def activate_wifi_captive_portal():
    import uasyncio as asyncio
    from lib.wifi import activate_ap

    activate_ap()

    return
