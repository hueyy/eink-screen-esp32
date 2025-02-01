import math
from typing import Final, Literal

CANVAS_WIDTH: Final[int] = 800
CANVAS_HEIGHT: Final[int] = 480

DITHER_THRESHOLD: Final[int] = 128

RGB = tuple[int, int, int]

COLOUR_PALETTE: Final[tuple[RGB, ...]] = (
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 0),
)


def determine_bit(red: int, green: int, blue: int, alpha: int) -> bool:
    # true is white
    # false is black
    if alpha < 127:
        return True
    if (red + blue + green) / 3 > DITHER_THRESHOLD:
        return True
    return False


def get_average_luminosity(rgb: RGB) -> float:
    r, g, b = rgb
    return (r + g + b) / 3


def get_colour_distance(color1: RGB, color2: RGB) -> int:
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return (r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2


def get_nearest_colour_index(palette: tuple[RGB, ...], input_colour: RGB) -> int:
    distances = [get_colour_distance(p, input_colour) for p in palette]
    lowest = min(distances)
    return distances.index(lowest)


def is_red(red: int, green: int, blue: int, threshold: int = 50) -> bool:
    return red >= 255 - threshold and green <= threshold and blue <= threshold


def convert_image_data_to_mono_red_hlsb(
    input_buffer: bytes, width: int = CANVAS_WIDTH, height: int = CANVAS_HEIGHT
) -> bytes:
    """
    Buffer should contain a 1-dimensional array of integers from 0-255
    in the RGBA format, representing pixels proceeding from left to
    right and then downwards

    Output should be in the MONO_HLSB format whereby bits in a byte are
    horizontally mapped with bit 7 being the leftmost.
    Subsequent bytes appear at successive horizontal locations until
    the rightmost edge is reached. Further bytes are rendered on the
    next row, one pixel lower.
    Output contains the same image in concatenated black and red arrays
    """
    current_black_byte = 0
    current_red_byte = 0
    byte_index = 7

    black_byte_buffer = bytearray((width * height) // 8)
    red_byte_buffer = bytearray((width * height) // 8)

    for i in range(0, len(input_buffer), 4):
        red = input_buffer[i]
        green = input_buffer[i + 1]
        blue = input_buffer[i + 2]
        alpha = input_buffer[i + 3]

        if is_red(red, green, blue, 40):
            current_red_byte += 0
            current_black_byte += 2**byte_index
        else:
            current_red_byte += 2**byte_index
            current_black_byte += (
                2 ** byte_index if determine_bit(red, green, blue, alpha) else 0
            )

        if byte_index == 0:
            black_byte_buffer[(i - 28) // 32] = (
                current_black_byte  # one iteration before 32
            )
            red_byte_buffer[(i - 28) // 32] = (
                current_red_byte  # one iteration before 32
            )
            current_black_byte = 0
            current_red_byte = 0
            byte_index = 7
        else:
            byte_index -= 1

    return bytes(black_byte_buffer + red_byte_buffer)


DitherMode = Literal["none", "binary", "ternary", "floydSteinberg", "floydSteinbergRed"]


def clamp(value: int | float, min_value: int = 0, max_value: int = 255) -> int:
    return int(max(min_value, min(value, max_value)))


def dither_image_data(
    image_data: bytes, dither_mode: DitherMode = "floydSteinbergRed"
) -> bytes:
    image_data = bytearray(image_data)
    match dither_mode:
        # TODO: Bill Atkinson dithering and Riemersma dithering?
        case "none":
            return bytes(image_data)

        case "binary":
            for current_pixel in range(0, len(image_data), 4):
                average_luminosity = (
                    image_data[current_pixel]
                    + image_data[current_pixel + 1]
                    + image_data[current_pixel + 2]
                ) / 3
                image_data[current_pixel] = (
                    0 if average_luminosity < DITHER_THRESHOLD else 255
                )
                image_data[current_pixel + 1] = image_data[current_pixel]
                image_data[current_pixel + 2] = image_data[current_pixel]
            return bytes(image_data)

        case "ternary":
            for current_pixel in range(0, len(image_data), 4):
                if is_red(
                    image_data[current_pixel],
                    image_data[current_pixel + 1],
                    image_data[current_pixel + 2],
                ):
                    image_data[current_pixel] = 255
                    image_data[current_pixel + 1] = image_data[current_pixel + 2] = 0
                else:
                    average_luminosity = (
                        image_data[current_pixel]
                        + image_data[current_pixel + 1]
                        + image_data[current_pixel + 2]
                    ) / 3
                    image_data[current_pixel] = (
                        0 if average_luminosity < DITHER_THRESHOLD else 255
                    )
                    image_data[current_pixel + 1] = image_data[current_pixel]
                    image_data[current_pixel + 2] = image_data[current_pixel]
            return bytes(image_data)

        case "floydSteinberg":
            for current_pixel in range(0, len(image_data), 4):
                average_luminosity = get_average_luminosity(
                    (
                        image_data[current_pixel],
                        image_data[current_pixel + 1],
                        image_data[current_pixel + 2],
                    )
                )
                if average_luminosity < 240 and average_luminosity > 20:
                    new_pixel = (
                        0 if image_data[current_pixel] < DITHER_THRESHOLD else 255
                    )
                    err = int((image_data[current_pixel] - new_pixel) / 16)
                    image_data[current_pixel] = new_pixel
                    image_data[current_pixel + 4] += err * 7
                    image_data[current_pixel + 4 * CANVAS_WIDTH - 4] += err * 3
                    image_data[current_pixel + 4 * CANVAS_WIDTH] += err * 5
                    image_data[current_pixel + 4 * CANVAS_WIDTH + 4] += err * 1
                    image_data[current_pixel + 1] = image_data[current_pixel]
                    image_data[current_pixel + 2] = image_data[current_pixel]
            return bytes(image_data)

        case "floydSteinbergRed":
            for current_pixel in range(0, len(image_data), 4):
                nearest_colour_index = get_nearest_colour_index(
                    COLOUR_PALETTE,
                    (
                        image_data[current_pixel],
                        image_data[current_pixel + 1],
                        image_data[current_pixel + 2],
                    ),
                )
                new_colour = COLOUR_PALETTE[nearest_colour_index]

                quant_error = (
                    image_data[current_pixel] - new_colour[0],
                    image_data[current_pixel + 1] - new_colour[1],
                    image_data[current_pixel + 2] - new_colour[2],
                )

                image_data[current_pixel] = new_colour[0]
                image_data[current_pixel + 1] = new_colour[1]
                image_data[current_pixel + 2] = new_colour[2]

                x: int = (current_pixel // 4) % CANVAS_WIDTH
                y: int = math.floor((current_pixel / 4) / CANVAS_WIDTH)

                for dx, dy, fraction in [
                    (1, 0, 7 / 16),
                    (-1, 1, 3 / 16),
                    (0, 1, 5 / 16),
                    (1, 1, 1 / 16),
                ]:
                    x1 = x + dx
                    y1 = y + dy
                    if 0 <= x1 < CANVAS_WIDTH and 0 <= y1 < CANVAS_HEIGHT:
                        index1: int = 4 * (x1 + y1 * CANVAS_WIDTH)
                        for i in range(3):
                            image_data[index1 + i] = int(quant_error[i] * fraction)
            return bytes(image_data)

        case _:
            return bytes(image_data)
