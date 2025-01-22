def init():
    # connect to WiFi
    from lib.wifi import connect_to_wifi

    wifi = connect_to_wifi()
    if not wifi:
        from lib.wifi import activate_wifi_captive_portal

        activate_wifi_captive_portal()

    from lib.api import fetch_screen
    import time

    etag = None

    while True:
        print("Running fetch_screen")
        etag = fetch_screen(etag)
        print("fetch_screen done")
        time.sleep(2)

    # import uasyncio

    # from lib.api_server import start_api_server

    # uasyncio.run(start_api_server())
