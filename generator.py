import tcod as libtcod
# Tiles needed 4 small map 33x43
from inputHandlers import handleKeys
from entity import Entity
from renderFunctions import clear_all, render_all
from subsectorMap import ssMap

def main():
    screenWidth = 100
    screenHeight = 64
    mapWidth = 76
    mapHeight = 64

    colors = {
        'HexDivider': libtcod.Color(100, 100, 100),
        'HexInterior': libtcod.Color(5, 5, 5)
    }

    entities = []
    subsectorMap = ssMap(mapWidth, mapHeight)
    subsectorMap.make_map(entities)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    con = libtcod.console_new(screenWidth, screenHeight)

    libtcod.console_set_custom_font('lefont.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screenWidth, screenHeight, 'MGTMapper', False)

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_blit(con, 0, 0, screenWidth, screenHeight, 0, 0, 0)
        render_all(con, entities, subsectorMap, screenWidth, screenHeight, colors)
        libtcod.console_flush()
        clear_all(con, entities)

        action = handleKeys(key)

        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()