import machine


def top_toot_mode(tag: str):
    from lib.display import Display

    display = Display()
    display.init_buffer()

    toot = None
    try:
        from lib.storage import retrieve_toot, erase_toot

        toot = retrieve_toot()
        erase_toot()
        display.display_toot(toot)
        display.sleep()
        return
    except OSError:
        print("No toot stored")

    from lib.wifi import connect_to_wifi

    if not connect_to_wifi():
        print("Failed to connect to WiFi")
        return

    from lib.data import get_latest_toot_by_tag

    toot = get_latest_toot_by_tag(tag)

    print("Got toot:", toot)

    from lib.wifi import disconnect_from_wifi

    disconnect_from_wifi()

    if toot is not None:
        from lib.storage import store_toot

        store_toot(toot)
        print("Stored toot")
        machine.reset()


def test_bluetooth():
    from lib.bt import BT

    b = BT()
    b.wait_for_connection()


def display_test():
    from lib.display import Display
    import assets.fonts.fira_sans_bold_32 as fira_sans_bold_32

    display = Display()
    display.init_buffer()
    display.display_text("Hello World!", 50, 50, fira_sans_bold_32, 1, 0)
    display.update()
