#/bin/sh
poetry run rshell -f ./scripts/flash_src.rshell
poetry run mpremote mip install aioble github:miguelgrinberg/microdot/src/microdot.py
