import tcod as libtcod
# Tiles needed 4 small map 33x43
from inputHandlers import handle_keys, handle_mouse
from entity import Entity
from renderFunctions import clear_all, render_all
from subsectorMap import ssMap

def main():
    screenWidth = 111
    screenHeight = 80
    mapWidth = 76
    mapHeight = 64
    panel_x = mapWidth
    panelWidth = 35

    colors = {
        'HexDivider': libtcod.Color(50, 50, 100),
        'HexInterior': libtcod.Color(5, 5, 5)
    }

    entities = []
    subsectorMap = ssMap(mapWidth, mapHeight)
    subsectorMap.make_map(entities)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    con = libtcod.console_new(screenWidth, screenHeight)
    panel = libtcod.console_new(panelWidth, screenHeight)

    libtcod.console_set_custom_font('lefont.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screenWidth, screenHeight, 'MGTMapper', False)

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_blit(con, 0, 0, screenWidth, screenHeight, 0, 0, 0)
        render_all(con, panel, entities, subsectorMap, screenWidth, screenHeight, colors, mouse, panelWidth, panel_x)
        libtcod.console_flush()
        clear_all(con, entities)

        action = handle_keys(key)
        mouse_action = handle_mouse(mouse)

        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

if __name__ == '__main__':
    main()