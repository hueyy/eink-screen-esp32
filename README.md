# eink-screen

## Development

1. [Installing Poetry dependencies](#install-poetry-dependencies)
2. [Install MicroPython firmware](#install-micropython-firmware)
3. Understand the [file structure](#file-structure)
4. Run code with [RShell](#rshell)

Chip is ESP32-D0WDQ6 (revision v1.0).

Screen is Waveshare [7.5inch_e-Paper_HAT_(B)](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)).

### Install Poetry dependencies

This project uses the Poetry dependency manager. Install that and run the following to install the poetry dependencies:

```bash
poetry install
poetry run mpremote mip install aioble 
```

### Install MicroPython firmware

Enter the virtualenv created by Poetry:

```bash
poetry shell
```

Identify the serial port your device is connected to:

```bash
python -m serial.tools.list_ports
```

Example output:

```bash
/dev/ttyACM0
1 ports found
```

If the serial port is inaccessible, you may need to give yourself the necessary permissions:

```bash
sudo usermod -aG tty $USER
sudo usermod -aG dialout $USER

# re-enter your shell
exec su -l $USER
cd eink-screen
poetry shell
```

Download the [latest stable MicroPython firmware](https://micropython.org/download/esp32/).

Proceed to install the new firmware:

```bash
esptool.py --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32 --port /dev/ttyACM0 write_flash -z 0x1000 ~/Downloads/esp32-20220618-v1.19.1.bin
```

### File structure

There are 2 main MicroPython scripts:

- **boot.py**: this is run immediately after the device boots up and by convention contains only code initialising debuggers, REPLs, etc.
- **main.py**: this is run immediately after `boot.py` runs and should contain your application code. You can import other dependencies in this file.


### mpremote

You can use [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) to transfer code and use a REPL.

Use <kbd>Ctrl</kbd><kbd>]</kbd> to exit the REPL.

When developing, my preference is to use a `src/test.py` file:

```bash
mpremote mount src
import test
```

Use <kbd>Ctrl</kbd><kbd>D</kbd> to soft reload the device and remount the directory.

You can use mpremote to transfer all the files later when deploying.

### RShell

Alternatively, you can use [rshell](https://github.com/dhylands/rshell). Note that using both mpremote and RShell at the same time may cause issues and lead to the device freezing up.

```bash
poetry shell
rshell
```

And then within rshell's interactive prompt, connect to the device:

```bash
connect serial /dev/ttyACM0
```

You can then access the filesystem:

```bash
ls /pyboard
cp src/main.py /pyboard/
```

Or even edit a file directly:

```bash
edit /pyboard/main.py
```

You can get a Python REPL prompt over the serial port:

```shell
repl
```

The controls are emacs-style, so use `[C-x]`, i.e. <kbd>Ctrl-A</kbd> <kbd>Ctrl-X</kbd>.

Useful development commands:

```bash
./scripts/flash_micropython.sh # to re-flash micropython firmware if the MCU freezes up
./scripts/flash_src.sh # to transfer and run new files in a single command
```

### Assets

- **Fonts**: [peterhinch/micropython-font-to-py](https://github.com/peterhinch/micropython-font-to-py)
  - `./scripts/font-to-py.py -x input.ttf <font_size> out.py`
- **Images**: [image2cpp](https://javl.github.io/image2cpp/)