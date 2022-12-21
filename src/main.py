import gc


class Device:
    def __init__(self):
        self.mode = 0

    def top_toot_mode(self, tag: str):
        from lib.wifi import connect_to_wifi

        if not connect_to_wifi():
            print("Failed to connect to WiFi")
            return

        from lib.data import get_latest_toot_by_tag

        toot = get_latest_toot_by_tag(tag)
        print("Got toot:", toot)

        if toot is not None:
            from lib.display import Display

            display = Display()
            display.init_buffer()
            display.display_toot(toot)
            display.sleep()

    def test_bluetooth(self):
        from lib.bt import BT

        b = BT()
        b.wait_for_connection()
