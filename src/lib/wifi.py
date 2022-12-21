def connect_to_wifi() -> bool:
    import network

    wlan = network.WLAN(network.STA_IF)

    if wlan.isconnected():
        return True

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
    return True
