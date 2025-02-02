from typing import LiteralString

CURRENT_FILE_PATH: LiteralString = "server/static/current"
CURRENT_FILE_IMAGE_PATH: LiteralString = "server/static/current.png"


def write_to_file(file_path: str, value: bytes | str):
    open_mode = "w" if type(value) is str else "wb"
    with open(file_path, open_mode) as file:
        file.write(value)


def read_from_file(file_path: str):
    open_mode = "r"
    with open(file_path, open_mode) as file:
        return file.read()


def write_current_canvas(value: bytes | str):
    return write_to_file(CURRENT_FILE_PATH, value)


def write_current_canvas_image(value: bytes):
    return write_to_file(CURRENT_FILE_IMAGE_PATH, value)
