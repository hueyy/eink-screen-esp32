#/bin/sh
poetry run rshell -f ./scripts/flash_src.rshell
poetry run mpremote mip install github:miguelgrinberg/microdot/src/microdot.py github:miguelgrinberg/microdot/src/microdot_asyncio.py
