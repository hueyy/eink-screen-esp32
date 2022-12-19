#/bin/sh

esptool.py --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32 --port /dev/ttyACM0 write_flash -z 0x1000 ~/Downloads/esp32-20220618-v1.19.1.bin
