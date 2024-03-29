#/bin/sh

poetry run esptool.py --chip esp32 --port /dev/ttyACM0 erase_flash
poetry run esptool.py --chip esp32 --port /dev/ttyACM0 write_flash -z 0x1000 ~/Downloads/ESP32_GENERIC-20240222-v1.22.2.bin
