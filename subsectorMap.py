import tcod as libtcod

from random import randint
from tile import Tile
from shapes import Hex
from entity import Entity


class ssMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_hex(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x - 2, room.x + 3):
            for y in range(room.y - 2, room.y + 3):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        for x in range(room.x - 3, room.x + 4):
            for y in range(room.y - 1, room.y + 2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        for x in range(room.x - 4, room.x + 5):
            self.tiles[x][room.y].blocked = False
            self.tiles[x][room.y].block_sight = False

    def make_map(self, entities):
        # Create the Hex Grid
        for x in range(4):
            for y in range(10):
                self.create_hex(Hex(14*x+4, 6*y+2))
                self.world_gen(Hex(14*x+4, 6*y+2), entities)
        for x in range(4):
            for y in range(10):
                self.create_hex(Hex(14*x+11, 6*y+5))
                self.world_gen(Hex(14*x+11, 6*y+5), entities)

    def world_gen(self, room, entities):
        if randint(0, 1) == 1:
            populated_hex = Entity(room.x, room.y - 1, 'O', libtcod.white)
            entities.append(populated_hex)
            if randint(1, 6) + randint(1, 6) < 11:
                GasGiant = Entity(room.x+2, room.y-1, 'G', libtcod.dark_orange)
                entities.append(GasGiant)

            size = randint(1, 6) + randint(1, 6) - 2
            if size < 10:
                sizdes = size
            else:
                sizdes = 'A'
            tcSize = Entity(room.x -4, room.y, @, libtcod.white)
            entities.append(tcSize)
"""
            atmo = randint(1, 6) + randint(1, 6) - 7 + size
            if atmo < 0:
                atmodes = 0
            elif atmo < 10:
                atmodes = atmosphere
            elif atmo = 10:
                atmodes = 'A'
            elif atmo = 11:
                atmodes = 'B'
            elif atmo = 12:
                atmodes = 'C'
            elif atmo = 13:
                atmodes = 'D'
            elif atmo = 14:
                atmodes = 'E'
            else:
                atmodes = 'F'

            worldtempbase = randint(1, 6) + randint(1, 6)
            habzonevalue = randint(1,100)
            if habzonevalue < 16:
                habcheck = 'cold'
            elif habzonevalue > 85:
                habcheck = 'hot'
            else
                habcheck = 0
            if atmodes < 2:
                temp = 'swing'
            elif atmodes < 4:
                temp = worldtempbase - 2
            elif atmodes < 6 or atmo = 14:
                temp = worldtempbase - 1
            elif atmodes < 8:
                temp = worldtempbase
            elif atmo=10 or atmo=13 or atmo=15:
                temp = worldtempbase + 2
            elif atmo = 11 or atmo
"""
