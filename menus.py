import tcod as libtcod


def main_menu(con, background_image, screenWidth, screenHeight):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screenWidth / 2), int(screenHeight / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'MGT Map Generator')
    libtcod.console_print_ex(0, int(screenWidth / 2), int(screenHeight - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By Zedalgo')

    menu(con, '', ['Create a new subsector', 'Exit'], 24, screenWidth, screenHeight)
