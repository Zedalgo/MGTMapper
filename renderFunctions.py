import tcod as libtcod

from tile import Tile


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             name)


def get_names_under_mouse(mouse, entities):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == x and entity.y == y]
    names = ', '.join(names)

    return names.capitalize()


def get_hex_x_under_mouse(mouse, game_map, mapWidth, mapHeight):
    (x, y) = (mouse.cx, mouse.cy)

    if y >= mapHeight or x >= mapWidth:
        return ' '
    else:
        hexx = game_map.tiles[x]
        return str(hexx)


def get_hex_y_under_mouse(mouse, game_map, mapWidth, mapHeight):
    (x, y) = (mouse.cx, mouse.cy)

    if y >= mapHeight or x >= mapWidth:
        return ' '
    else:
        hexy = game_map.tiles[y]
        return str(hexy)


def render_all(con, panel, entities, game_map, screenWidth, screenHeight, colors, mouse, panelWidth, panel_x,
               mapWidth, mapHeight):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                libtcod.console_set_char_background(con, x, y, colors.get('HexDivider'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con, x, y, colors.get('HexInterior'), libtcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity)

    # Hopefully shows the name of a world under the mouse
    entity_name = get_names_under_mouse(mouse, entities)
    hex__x = get_hex_x_under_mouse(mouse, game_map, mapWidth, mapHeight)
    hex__y = get_hex_y_under_mouse(mouse, game_map, mapWidth, mapHeight)

    libtcod.console_blit(con, 0, 0, screenWidth, screenHeight, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    render_bar(panel, 1, 1, 10, entity_name, 8, 10, libtcod.red, libtcod.darker_red)
    render_bar(panel, 1, 2, 10, hex__x, 8, 10, libtcod.red, libtcod.darker_red)
    render_bar(panel, 1, 3, 10, hex__y, 8, 10, libtcod.red, libtcod.darker_red)
    libtcod.console_blit(panel, 0, 0, panelWidth, screenHeight, 0, panel_x, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
