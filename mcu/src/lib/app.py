def start_web_interface():
    import uasyncio as asyncio
    from lib.wifi import activate_ap

    activate_ap()

    loop = asyncio.get_event_loop()

    from lib.server import start_server

    loop.create_task(start_server())

    # from lib.dns import run_dns_server

    # loop.create_task(run_dns_server())

    loop.run_forever()
    loop.close()

    return
