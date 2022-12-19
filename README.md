# eink-screen

## Development

1. [Installing Poetry dependencies](#install-poetry-dependencies)
2. [Install MicroPython firmware](#install-micropython-firmware)
3. Understand the [file structure](#file-structure)
4. Use either [WebREPL](#webrepl) or [RShell](#rshell)

### Install Poetry dependencies

This project uses the Poetry dependency manager. Install that and run the following to install the poetry dependencies:

```bash
poetry install
```

### Install MicroPython firmware

Enter the virtualenv created by Poetry:

```bash
poetry shell
```

Identify the serial port your Watchy is connected to:

```bash
python -m serial.tools.list_ports
```

Example output:

```bash
/dev/ttyUSB0
1 ports found
```

If the serial port is inaccessible, you may need to give yourself the necessary permissions:

```bash
sudo usermod -aG tty $USER
sudo usermod -aG dialout $USER

# re-enter your shell
exec su -l $USER
cd watchy_py
poetry shell
```

Download the [latest stable MicroPython firmware](https://micropython.org/download/esp32/).

Proceed to install the new firmware:

```bash
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 ~/Downloads/esp32-20220618-v1.19.1.bin
```

### File structure

There are 2 main MicroPython scripts:

- **boot.py**: this is run immediately after the Watchy boots up and by convention contains only code initialising debuggers, REPLs, etc.
- **main.py**: this is run immediately after `boot.py` runs and should contain your application code. You can import other dependencies in this file.


### mpremote

You can use [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) to transfer code and use a REPL.

Use <kbd>Ctrl</kbd><kbd>]</kbd> to exit the REPL.

```bash
mpremote run src/main.py

mpremote cp -r src/ .
```

### Restarting

Since the reset pin on Watchy isn't easily accessible, you may want to do the following using rshell:

```bash
cp reset.py /pyboard/
repl ~ import reset ~
```

### Assets

- **Fonts**: [peterhinch/micropython-font-to-py](https://github.com/peterhinch/micropython-font-to-py)
  - `./scripts/font-to-py.py -x input.ttf <font_size> out.py`
- **Images**: [image2cpp](https://javl.github.io/image2cpp/)