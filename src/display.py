from constants import BLACK, WHITE
from machine import Pin, SPI
import framebuf
from lib.writer import Writer
from lib.epaper7in5_V2 import EPD


class Display:
    BACKGROUND = 0
    FOREGROUND = 1

    MAX_WIDTH = 800
    MAX_HEIGHT = 480

    def __init__(self):
        sck = Pin(13)
        dc = Pin(27)
        cs = Pin(15)
        busy = Pin(25)
        rst = Pin(26)
        mosi = Pin(14)
        self.spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, mosi=mosi)
        self.epd = EPD(self.spi, cs, dc, rst, busy)
        self.epd.init()
        self.buffer = bytearray(self.MAX_WIDTH * self.MAX_HEIGHT // 8)
        self.framebuf = framebuf.FrameBuffer(
            self.buffer,
            self.MAX_WIDTH,
            self.MAX_HEIGHT,
            framebuf.MONO_HLSB,
        )

    def update(self, buffer: bytearray | None = None, mirror_y=True, partial=False):
        target_buffer = self.buffer if buffer is None else buffer
        self.epd.display_frame(target_buffer)

    def fill(self, color: int):
        self.framebuf.fill(color)
        self.update()

    def clear(self):
        self.epd.clear()
