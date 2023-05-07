def init():
    import gc

    gc.enable()
    gc.threshold(10000)
    gc.collect()

    # connect to WiFi
    from lib.wifi import connect_to_wifi

    connect_to_wifi()

    # start API server
    import uasyncio as asyncio

    loop = asyncio.get_event_loop()
    from lib.api_server import start_api_server

    loop.create_task(start_api_server())
    loop.run_forever()
    loop.close()
