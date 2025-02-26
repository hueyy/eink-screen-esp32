# MCU

## Hardware

The chip is ESP32-D0WDQ6 (revision v1.0), i.e. [ESP32 driver board from Waveshare](https://www.waveshare.com/e-paper-esp32-driver-board.htm). It has the following specifications:

- WiFi:  802.11b/g/n
- Flash size: 4MB
- SRAM size: 520KB
- ROM size: 448KB

The screen is a Waveshare [7.5inch_e-Paper (B)](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B)_Manual#Introduction).

## Development

1. [Installing Poetry dependencies](#install-poetry-dependencies)
2. [Install MicroPython firmware](#install-micropython-firmware)
3. Understand the [file structure](#file-structure)
4. Run code with [RShell](#rshell)

### Install Poetry dependencies

This project uses the Poetry dependency manager. Install that and run the following to install the poetry dependencies:

```bash
cd mcu
poetry install
```

### Install MicroPython firmware

```shell
poetry shell
sh scripts/list_ports.sh
```

Example output:

```shell
                              Connected boards
┏━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━━┓
┃Serial      ┃Family     ┃Port ┃Board                          ┃CPU  ┃Version┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━━┩
│/dev/ttyACM0│micropython│esp32│ESP32_GENERIC                  │ESP32│v1.22.2│
│            │           │     │Generic ESP32 module with ESP32│     │       │
└────────────┴───────────┴─────┴───────────────────────────────┴─────┴───────┘
```

Download the [latest stable MicroPython firmware](https://micropython.org/download/esp32/):

```shell
mpflash download --board ESP32_GENERIC --version ?
```

This uses [mpflash](https://github.com/Josverl/micropython-stubber/tree/main/src/mpflash) to automatically download the MicroPython firmware. 

Proceed to install the new firmware:

```shell
sh scripts/flash_micropython.sh
```

### File structure

There are 2 main MicroPython scripts:

- **boot.py**: this is run immediately after the device boots up and by convention contains only code initialising debuggers, REPLs, etc.
- **main.py**: this is run immediately after `boot.py` runs and should contain your application code. You can import other dependencies in this file.


### RShell

You can use [rshell](https://github.com/dhylands/rshell) to transfer your code to the MCU and get a REPL.

```bash
poetry shell
rshell
```

And then within rshell's interactive prompt, connect to the device (if RShell doesn't automatically connect):

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

You can reboot the device using the following command:

```
repl ~ import machine ~ machine.soft_reset() ~
```

The controls are emacs-style, so use `[C-x]`, i.e. <kbd>Ctrl-A</kbd> <kbd>Ctrl-X</kbd>.

Useful development commands:

```bash
./scripts/flash_src.sh # to transfer and run new files in a single command
```

## Secrets

Create a `mcu/src/lib/secrets.py` file based on the `secrets.sample.py` file. 

## Reference

For my own reference

- **Fonts**: [peterhinch/micropython-font-to-py](https://github.com/peterhinch/micropython-font-to-py)
  - `./scripts/font-to-py.py -x input.ttf <font_size> out.py`
- **Images**: [image2cpp](https://javl.github.io/image2cpp/)
- `archive` folder
