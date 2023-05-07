import aioble
from lib.constants import (
    _IMAGE_BUFFER_SERVICE_UUID,
    BT_NAME,
    _IMAGE_BUFFER_CHARACTERISTIC_UUID,
)
import uasyncio
from micropython import const


_ADV_INTERVAL_MS = const(250_000)


class BT:
    def __init__(self):
        self.image_buffer_service = aioble.Service(_IMAGE_BUFFER_SERVICE_UUID)
        self.image_buffer_characteristic = aioble.Characteristic(
            self.image_buffer_service,
            _IMAGE_BUFFER_CHARACTERISTIC_UUID,
            write=True,
            # capture=True,
            # notify=True,
        )
        aioble.register_services(self.image_buffer_service)

    async def read_image_buffer_characteristic(self):
        data = await self.image_buffer_characteristic.written()
        print("a", data)

    def wait_for_connection(self):
        async def receive_connection():
            while True:
                print("Waiting for BT connection")
                connection = await aioble.advertise(
                    _ADV_INTERVAL_MS,
                    name=BT_NAME,
                    services=[_IMAGE_BUFFER_SERVICE_UUID],
                )
                print("BT connection from", connection.device)

                # await self.read_image_buffer_characteristic()
                # t = asyncio.create_task(l2cap_task(connection))
                # await control_task(connection)
                # t.cancel()

                # await connection.disconnected()

        async def main():
            await receive_connection()

        uasyncio.run(main())
