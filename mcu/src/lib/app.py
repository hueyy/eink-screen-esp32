def init():
    import gc

    gc.enable()
    gc.threshold(10000)
    gc.collect()

    # connect to WiFi
    from lib.wifi import connect_to_wifi

    connect_to_wifi()

    from lib.api_server import start_api_server

    start_api_server()
