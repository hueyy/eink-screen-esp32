from micropython import const

MAX_WIDTH = const(800)
MAX_HEIGHT = const(480)

BACKGROUND = const(1)
FOREGROUND = const(0)

BAUD_RATE = const(20000000)
BUFFER_SIZE = const(MAX_WIDTH * MAX_HEIGHT // 8)


class Display:
    def __init__(self):
        from machine import Pin, SPI
        from lib.epaper7in5_V2 import EPD

        sck = Pin(13)
        dc = Pin(27)
        cs = Pin(15)
        busy = Pin(25)
        rst = Pin(26)
        mosi = Pin(14)
        self.spi = SPI(2, baudrate=BAUD_RATE, polarity=0, phase=0, sck=sck, mosi=mosi)
        self.epd = EPD(self.spi, cs, dc, rst, busy)
        self.epd.init()

    def init_buffer(self):
        from framebuf import FrameBuffer, MONO_HLSB

        self.buffer = bytearray(BUFFER_SIZE)
        self.framebuf = FrameBuffer(
            self.buffer,
            MAX_WIDTH,
            MAX_HEIGHT,
            MONO_HLSB,
        )

    def update(self, buffer: bytearray | None = None):
        target_buffer = self.buffer if buffer is None else buffer
        self.epd.display_frame(target_buffer)

    def fill(self, color: int):
        self.framebuf.fill(color)
        self.update()

    def clear(self):
        self.epd.clear()

    def sleep(self):
        self.epd.sleep()

    def display_text(
        self,
        text: str,
        x: int,
        y: int,
        font,
        background_colour: int,
        text_colour: int,
    ):
        from lib.writer import Writer

        wri = Writer(
            self.framebuf,
            font,
            MAX_WIDTH,
            MAX_HEIGHT,
            background_colour,
            text_colour,
        )
        wri.set_textpos(self.framebuf, y, x)
        wri.printstring(text)

    def display_toot(self, toot):
        self.framebuf.fill(BACKGROUND)
        name, username, content, timestamp = toot

        import assets.fonts.fira_sans_bold_32 as fira_sans_bold_32

        self.display_text(name, 40, 40, fira_sans_bold_32, BACKGROUND, FOREGROUND)

        import assets.fonts.fira_sans_regular_24 as fira_sans_regular_24

        self.display_text(
            username, 40, 80, fira_sans_regular_24, BACKGROUND, FOREGROUND
        )
        self.display_text(
            content, 40, 135, fira_sans_regular_24, BACKGROUND, FOREGROUND
        )
        self.display_text(
            timestamp, 40, 170, fira_sans_regular_24, BACKGROUND, FOREGROUND
        )
        self.update()
