"""
Adapted from https://github.com/tanahy/micropython-waveshare-epaper/blob/dev/epaper7in5b.py

MicroPython Waveshare 7.5" Black/White/Red GDEW075Z09 e-paper display driver
https://github.com/mcauser/micropython-waveshare-epaper

MIT License
Copyright (c) 2017 Waveshare
Copyright (c) 2018 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# also works for black/white/yellow GDEW075C21?

from micropython import const
from time import sleep_ms  # type: ignore
import ustruct

# Display resolution
EPD_WIDTH = const(800)
EPD_HEIGHT = const(480)

# Display commands
PANEL_SETTING = const(0x00)
POWER_SETTING = const(0x01)
POWER_OFF = const(0x02)
# POWER_OFF_SEQUENCE_SETTING     = const(0x03)
POWER_ON = const(0x04)
# POWER_ON_MEASURE               = const(0x05)
BOOSTER_SOFT_START = const(0x06)
DEEP_SLEEP = const(0x07)
DATA_START_TRANSMISSION_1 = const(0x10)  # for black data
# DATA_STOP                      = const(0x11)
DISPLAY_REFRESH = const(0x12)
DATA_START_TRANSMISSION_2 = const(0x13)  # for red data
# IMAGE_PROCESS                  = const(0x13)
# LUT_FOR_VCOM                   = const(0x20)
# LUT_BLUE                       = const(0x21)
# LUT_WHITE                      = const(0x22)
# LUT_GRAY_1                     = const(0x23)
# LUT_GRAY_2                     = const(0x24)
# LUT_RED_0                      = const(0x25)
# LUT_RED_1                      = const(0x26)
# LUT_RED_2                      = const(0x27)
# LUT_RED_3                      = const(0x28)
# LUT_XON                        = const(0x29)
PLL_CONTROL = const(0x30)
# TEMPERATURE_SENSOR_COMMAND     = const(0x40)
TEMPERATURE_CALIBRATION = const(0x41)
# TEMPERATURE_SENSOR_WRITE       = const(0x42)
# TEMPERATURE_SENSOR_READ        = const(0x43)
VCOM_AND_DATA_INTERVAL_SETTING = const(0x50)
# LOW_POWER_DETECTION            = const(0x51)
TCON_SETTING = const(0x60)
TCON_RESOLUTION = const(0x61)
# SPI_FLASH_CONTROL              = const(0x65)
# REVISION                       = const(0x70)
# GET_STATUS                     = const(0x71)
# AUTO_MEASUREMENT_VCOM          = const(0x80)
# READ_VCOM_VALUE                = const(0x81)
VCM_DC_SETTING = const(0x82)
FLASH_MODE = const(0xE5)

BUSY = const(0)  # 0=busy, 1=idle


class EPD:
    def __init__(self, spi, cs, dc, rst, busy):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

    def send_command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)
        if data is not None:
            self.send_data(data)

    def send_data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(
            data
            if isinstance(data, bytearray) or isinstance(data, bytes)
            else bytearray(data)
            if isinstance(data, list)
            else bytearray([data])
        )
        self.cs(1)

    def turn_on_display(self):
        self.send_command(DISPLAY_REFRESH)
        sleep_ms(100)
        self.wait_until_idle()

    def init(self):
        self.reset()
        self.send_command(POWER_SETTING, [0x37, 0x00])
        self.send_command(PANEL_SETTING, [0xCF, 0x08])
        self.send_command(BOOSTER_SOFT_START, [0xC7, 0xCC, 0x28])
        self.send_command(POWER_ON)
        self.wait_until_idle()
        self.send_command(PLL_CONTROL, 0x3C)
        self.send_command(TEMPERATURE_CALIBRATION, 0x00)
        self.send_command(VCOM_AND_DATA_INTERVAL_SETTING, 0x77)
        self.send_command(TCON_SETTING, 0x22)
        self.send_command(TCON_RESOLUTION, ustruct.pack(">HH", EPD_WIDTH, EPD_HEIGHT))
        self.send_command(VCM_DC_SETTING, 0x1E)  # decide by LUT file
        self.send_command(FLASH_MODE, 0x03)

    def wait_until_idle(self):
        while self.busy.value() == BUSY:
            sleep_ms(100)

    def reset(self):
        self.rst(0)
        sleep_ms(200)
        self.rst(1)
        sleep_ms(200)

    # draw the current frame memory
    def display_frame(self, frame_buffer):
        # send black data
        self.send_black_buffer(frame_buffer)

        self.send_data(0x92)

        # send red data
        # self.send_command(DATA_START_TRANSMISSION_2, red_frame_buffer)
        self.turn_on_display()

    def send_black_buffer(self, frame_buffer):
        self.send_command(DATA_START_TRANSMISSION_1, frame_buffer)

    def clear(self):
        self.send_command(DATA_START_TRANSMISSION_1)
        for i in range(self.width * self.height // 8):
            self.send_data(0xFF)

        # red data
        self.send_command(DATA_START_TRANSMISSION_2)
        for i in range(self.width * self.height // 8):
            self.send_data(0xFF)

        self.turn_on_display()

    # to wake call reset() or init()
    def sleep(self):
        self.send_command(POWER_OFF)
        self.wait_until_idle()
        self.send_command(DEEP_SLEEP, 0xA5)
