import tcod as libtcod
import re


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


def render_string(panel, x, y, name):
    libtcod.console_print_ex(panel, int(len(name) / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             name)


def get_names_under_mouse(mouse, entities):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == x and entity.y == y]
    names = ', '.join(names)

    return names.capitalize()


def get_hex_x_under_mouse(mouse, hexes, mapWidth, mapHeight):
    (x, y) = (mouse.cx, mouse.cy)

    if y >= mapHeight or x >= mapWidth:
        return ' '
    else:
        namex = str([HexInfo.hex_x for HexInfo in hexes if HexInfo.x == x and HexInfo.y == y])
        namex = re.sub("\[|\]", "", namex)  # Regex to filter out brackets.
        return namex


def get_hex_y_under_mouse(mouse, hexes, mapWidth, mapHeight):
    (x, y) = (mouse.cx, mouse.cy)

    if y >= mapHeight or x >= mapWidth:
        return ' '
    else:
        namey = str([HexInfo.hex_y for HexInfo in hexes if HexInfo.x == x and HexInfo.y == y])
        namey = re.sub("\[|\]", "", namey)
        return namey


def planet_y_mouse(mouse, hexes, planets, mapWidth, mapHeight):
    (x, y) = (mouse.cx, mouse.cy)
    xint = get_hex_x_under_mouse(mouse, hexes, mapWidth, mapHeight)
    yint = get_hex_y_under_mouse(mouse, hexes, mapWidth, mapHeight)

    if xint == '' or xint == ' ':
        xint = 0
    else:
        xint = int(xint)

    if yint == '' or yint == ' ':
        yint = 0
    else:
        yint = int(yint)

    if y >= mapHeight or x >= mapWidth:
        return 'greb'
    else:
        gridy = str([World.grid_y for World in planets if World.grid_x == xint and World.grid_y == yint])
        gridy = re.sub("\[|\]", "", gridy)
        return gridy


def render_all(con, panel, entities, hexes, planets, game_map, screenWidth, screenHeight, colors, mouse, panelWidth, panel_x,
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

    # Will eventually show the name of a world under the mouse
    hex__x = get_hex_x_under_mouse(mouse, hexes, mapWidth, mapHeight)
    hex__y = get_hex_y_under_mouse(mouse, hexes, mapWidth, mapHeight)
    planet_y = planet_y_mouse(mouse, hexes, planets, mapWidth, mapHeight)

    # print(planet_y)

    libtcod.console_blit(con, 0, 0, screenWidth, screenHeight, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    render_string(panel, 1, 1, str(hex__x) + ', ' + str(hex__y))
    render_bar(panel, 1, 2, 10, hex__x, 8, 10, libtcod.red, libtcod.darker_red)
    render_bar(panel, 1, 3, 10, hex__y, 8, 10, libtcod.red, libtcod.darker_red)
    render_bar(panel, 1, 4, 10, planet_y, 8, 10, libtcod.red, libtcod.darker_red)
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
