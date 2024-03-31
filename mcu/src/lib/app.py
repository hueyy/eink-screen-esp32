def init():
    import gc

    gc.enable()
    gc.threshold(10000)
    gc.collect()

    from lib.RTC import store_rtc_value, read_rtc_value
    mode = read_rtc_value("mode")
    if mode is None:
        mode = "REMOTE"
        store_rtc_value(mode)

    # connect to WiFi
    from lib.wifi import connect_to_wifi

    wifi = connect_to_wifi()
    if not wifi:
        from lib.wifi import activate_wifi_captive_portal
        activate_wifi_captive_portal()

    import uasyncio

    from lib.api_server import start_api_server

    uasyncio.run(start_api_server())

