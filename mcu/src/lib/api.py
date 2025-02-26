import usocket, ssl  # type: ignore
from micropython import const  # type: ignore
from lib.display import Display
from lib.secrets import API_HOSTNAME

CHUNK_SIZE = const(1000)  # 1KiB


def capitalize_word(word: str):
    return word[0].upper() + word[1:] if word else ""


def capitalize_header_key(key: str):
    return "-".join(capitalize_word(word) for word in key.split("-"))


def parse_headers(header_string: str):
    headers = {
        capitalize_header_key(key.strip()): value.strip()
        for line in header_string.split("\r\n")[1:]
        if ":" in line
        for key, value in [line.split(":", 1)]
        if key and value
    }
    return headers


def compose_request(etag: str | None):
    headers = [
        "GET /static/current HTTP/1.1",
        f"Host: {API_HOSTNAME}",
        "User-Agent: micropython-esp32-huey-eink-screen",
        "Accept-Encoding: identity",
    ]

    if etag is not None and len(etag) > 0:
        headers.append(f"If-None-Match: {etag}")

    headers.extend(["Connection: close\r\n", ""])
    return "\r\n".join(headers)


def fetch_screen(etag: str | None = None):
    try:
        # Hostname to IP adddress
        socket_address = usocket.getaddrinfo(API_HOSTNAME, 443)[0][-1]

        s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        s.connect(socket_address)
        s.settimeout(60)

        ssl_socket = ssl.wrap_socket(s, server_hostname=API_HOSTNAME)  # type: ignore

        request = compose_request(etag)
        print("Making request: ")
        print(request)

        ssl_socket.write(request.encode())

        headers_complete: bool = False

        content_length: int = 0
        half_content_length: int = 0
        new_etag = None
        status_code = None
        clear_screen: bool = False

        d = Display()

        # to address some odd bug
        d.epd.clear()
        d.epd.reset()

        while True:
            chunk = ssl_socket.read(CHUNK_SIZE)

            if not chunk:
                print("No more chunks")
                break

            if not headers_complete:
                header_end = chunk.find(b"\r\n\r\n")
                if header_end != -1:
                    headers_str = chunk[:header_end].decode()
                    headers = parse_headers(headers_str)
                    headers_complete = True
                    print("Headers: ", headers)

                    status_code = int(headers_str.split()[1])
                    new_etag = headers.get("Etag")

                    chunk = chunk[header_end + 4 :]

                    if status_code == 304:  # Not Modified
                        print("HTTP 304 Not Modified")
                        break
                    if status_code != 200:
                        print("Non-200 status code: ", status_code)
                        print(chunk)
                        break

                    content_length = int(headers.get("Content-Length"))

                    d.init_epd()

                    if not (content_length > 0):
                        print("Clearing screen")
                        clear_screen = True
                        d.clear()
                        break

                    d.epd.begin_black_data_transmission()

                    half_content_length = content_length // 2
                else:
                    print("Could not find end of header")
                    print(chunk)

            try:
                # chunk may contain some red data and some black data
                chunk_with_some_red: bool = (
                    content_length > half_content_length
                    and (content_length - len(chunk)) <= half_content_length
                )

                if chunk_with_some_red:
                    black_data_length = content_length - half_content_length
                    d.epd.send_data(chunk[:black_data_length])
                    content_length -= black_data_length

                if content_length == half_content_length:
                    print("Begin red data transmission")
                    d.epd.send_data(0x92)
                    d.epd.begin_red_data_transmission()

                print("Current content_length: ", content_length)
                if chunk_with_some_red:
                    # just send the remainder
                    d.epd.send_data(chunk[black_data_length:])
                    content_length -= len(chunk) - black_data_length
                else:
                    d.epd.send_data(chunk)
                    content_length -= len(chunk)

            except Exception as e:
                print("Error decoding chunk:", e)

        ssl_socket.close()

        if status_code == 200 and new_etag is not None:
            etag = new_etag
            print("Set Etag to: ", etag)

            if not clear_screen:
                print("Updating screen")
                d.epd.turn_on_display()

    except Exception as e:
        raise e

    return etag
