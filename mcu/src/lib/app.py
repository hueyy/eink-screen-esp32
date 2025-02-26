def init():
    # connect to WiFi
    from lib.wifi import connect_to_wifi

    wifi = connect_to_wifi()
    if not wifi:
        from lib.wifi import activate_wifi_captive_portal

        activate_wifi_captive_portal()

    from lib.api import fetch_screen

    # from lib.display import Display
    import time

    # d = Display()

    etag = None

    while True:
        print("Running fetch_screen")
        etag = fetch_screen(etag)
        print("fetch_screen done")
        # d.epd.sleep()
        time.sleep(60 * 5)
        # d.epd.reset()
        # machine.deepsleep(60000 * 5)  # re-fetch every 5 minutes
