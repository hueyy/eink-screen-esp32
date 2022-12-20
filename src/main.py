# from display import Display
# import assets.fonts.fira_sans_bold_32 as fira_sans_bold_32
# import assets.fonts.fira_sans_regular_24 as fira_sans_regular_24


# d = Display()
# d.framebuf.fill(1)
# d.display_text("Ministry of Floof Singapore", 40, 40, fira_sans_bold_32, 1, 0)
# d.display_text("@mof_sg@kopiti.am", 40, 80, fira_sans_regular_24, 1, 0)

# d.display_text("henlo world", 40, 135, fira_sans_regular_24, 1, 0)

# d.display_text("17 December 2022, 8:04 AM", 40, 170, fira_sans_regular_24, 1, 0)

# d.update()
# d.epd.sleep()

from lib.bt import BT

b = BT()
b.wait_for_connection()
