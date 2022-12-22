from micropython import const
from bluetooth import UUID

WHITE = const(1)
BLACK = const(0)

_IMAGE_BUFFER_SERVICE_UUID = UUID("5eabe403-2988-48b4-90e9-a714538f0080")
_IMAGE_BUFFER_CHARACTERISTIC_UUID = UUID("6c9494c0-d4f8-418c-af2c-084c32baf2d3")
BT_NAME = "Huey's eInk Screen"
