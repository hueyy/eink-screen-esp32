from micropython import const

MAX_WIDTH = const(800)
MAX_HEIGHT = const(480)

BACKGROUND = const(1)
FOREGROUND = const(0)

BAUD_RATE = const(20000000)


class Display:
    """
    If you want to use the framebuffer, you have to call
    init_buffer() after initialising the display.
    """

    def __init__(self, width=MAX_WIDTH, height=MAX_HEIGHT):
        from machine import Pin, SPI
        from lib.epaper7in5b_V2 import EPD

        sck = Pin(13)
        dc = Pin(27)
        cs = Pin(15)
        busy = Pin(25)
        rst = Pin(26)
        mosi = Pin(14)
        self.spi = SPI(2, baudrate=BAUD_RATE, polarity=0, phase=0, sck=sck, mosi=mosi)
        self.epd = EPD(self.spi, cs, dc, rst, busy)

        self.buffer_size = width * height // 8
        self.width = width
        self.height = height

    def init_epd(self):
        self.epd.init()

    def init_buffer(self):
        self.init_epd()
        from framebuf import FrameBuffer, MONO_HLSB

        self.black_buffer = bytearray(self.buffer_size)
        self.black_framebuf = FrameBuffer(
            self.black_buffer,
            self.width,
            self.height,
            MONO_HLSB,
        )

        # TODO: handle red in same buffer
        # self.red_buffer = bytearray(BUFFER_SIZE)
        # self.red_framebuf = FrameBuffer(
        #     self.red_buffer,
        #     MAX_WIDTH,
        #     MAX_HEIGHT,
        #     MONO_HLSB,
        # )

    def update(
        self,
        black_buffer: bytearray | None = None,  # , red_buffer: bytearray | None = None
    ):
        target_black_buffer = (
            self.black_buffer if black_buffer is None else black_buffer
        )
        self.epd.display_frame(target_black_buffer)
        # target_red_buffer = self.red_buffer if red_buffer is None else red_buffer
        # self.epd.display_frame(target_black_buffer, target_red_buffer)

    def fill(self, color: int):
        self.black_framebuf.fill(color)
        # self.red_framebuf.fill(color)
        self.update()

    def fill_black(self, color: int):
        self.black_framebuf.fill(color)
        self.update()

    # def fill_red(self, color: int):
    #     self.red_framebuf.fill(color)
    #     self.update()

    def clear(self):
        self.epd.clear()
        # self.init_buffer()
        # self.fill(1)

    def sleep(self):
        self.epd.sleep()

    # def display_text(
    #     self,
    #     text: str,
    #     x: int,
    #     y: int,
    #     font,
    #     background_colour: int,
    #     text_colour: int,
    # ):
    #     from lib.writer import Writer

    #     wri = Writer(
    #         self.black_framebuf,
    #         font,
    #         self.width,
    #         self.height,
    #         background_colour,
    #         text_colour,
    #     )
    #     wri.set_textpos(self.black_framebuf, y, x)
    #     wri.printstring(text)

    # def display_toot(self, toot):
    #     self.black_framebuf.fill(BACKGROUND)
    #     name, username, content, timestamp = toot

    #     import assets.fonts.fira_sans_bold_32 as fira_sans_bold_32

    #     self.display_text(name, 40, 40, fira_sans_bold_32, BACKGROUND, FOREGROUND)

    #     import assets.fonts.fira_sans_regular_24 as fira_sans_regular_24

    #     self.display_text(
    #         username, 40, 80, fira_sans_regular_24, BACKGROUND, FOREGROUND
    #     )
    #     self.display_text(
    #         content, 40, 135, fira_sans_regular_24, BACKGROUND, FOREGROUND
    #     )
    #     self.display_text(
    #         timestamp, 40, 170, fira_sans_regular_24, BACKGROUND, FOREGROUND
    #     )
    #     self.update()
