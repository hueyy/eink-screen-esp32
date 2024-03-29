def init():
    import gc

    gc.enable()
    gc.threshold(10000)
    gc.collect()

    # connect to WiFi
    from lib.wifi import connect_to_wifi

    wifi = connect_to_wifi()
    if not wifi:
        from lib.wifi import activate_wifi_captive_portal
        activate_wifi_captive_portal()

    from lib.api_server import start_api_server

    start_api_server()
