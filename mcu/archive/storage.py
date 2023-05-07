from esp32 import NVS
import json

NAMESPACE = "usr"

TOOT_KEY = "toot"
TOOT_LENGTH_KEY = "toot_len"


def store_toot(toot: tuple[str, str, str, str]):
    # assume ASCII for now, but note characters can take up to 4 bytes
    nvs = NVS(NAMESPACE)
    toot_json = json.dumps(toot)
    nvs.set_blob(TOOT_KEY, toot_json)
    nvs.set_i32(TOOT_LENGTH_KEY, len(toot_json))
    nvs.commit()
    return


def retrieve_toot() -> tuple[str, str, str, str]:
    nvs = NVS(NAMESPACE)
    toot_length = nvs.get_i32(TOOT_LENGTH_KEY)
    b = bytearray(toot_length)
    nvs.get_blob(TOOT_KEY, b)
    return json.loads(b.decode("utf-8"))


def erase_toot():
    nvs = NVS(NAMESPACE)
    nvs.erase_key(TOOT_LENGTH_KEY)
    nvs.erase_key(TOOT_KEY)
