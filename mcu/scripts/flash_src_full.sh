#/bin/sh
poetry run rshell -f ./scripts/flash_src.rshell
poetry run mpremote mip install requests
# poetry run mpremote mip install github:miguelgrinberg/microdot/src/microdot/microdot.py
