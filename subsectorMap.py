import tcod as libtcod

from data_handlers import Planet
from dice_functions import roll
from entity import Entity
from random import randint
from richard_help import clamp
from shapes import Hex
from tile import Tile, HexInfo


class ssMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_hex(self, room, hexes, grid_x, grid_y):
        # Generates a hex shape using 3 rectangles
        for x in range(room.x - 3, room.x + 4):
            for y in range(room.y - 2, room.y + 3):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                hex_data = HexInfo(x, y, grid_x, grid_y)
                hexes.append(hex_data)
        x_column_1 = room.x - 4
        for y in range(room.y - 1, room.y + 2):
            self.tiles[x_column_1][y].blocked = False
            self.tiles[x_column_1][y].block_sight = False
            hex_data = HexInfo(x_column_1, y, grid_x, grid_y)
            hexes.append(hex_data)
        x_column_2 = room.x + 4
        for y in range(room.y - 1, room.y + 2):
            self.tiles[x_column_2][y].blocked = False
            self.tiles[x_column_2][y].block_sight = False
            hex_data = HexInfo(x_column_2, y, grid_x, grid_y)
            hexes.append(hex_data)
        x_edge_1 = room.x - 5
        x_edge_2 = room.x + 5
        self.tiles[x_edge_1][room.y].blocked = False
        self.tiles[x_edge_1][room.y].block_sight = False
        self.tiles[x_edge_2][room.y].blocked = False
        self.tiles[x_edge_2][room.y].block_sight = False
        edge_data_1 = HexInfo(x_edge_1, room.y, grid_x, grid_y)
        edge_data_2 = HexInfo(x_edge_2, room.y, grid_x, grid_y)
        hexes.append(edge_data_1)
        hexes.append(edge_data_2)

    def make_map(self, hexes, planets):
        # Create the Hex Grid
        for x in range(4):
            for y in range(10):
                grid_x = 2 * (x + 1) - 1
                grid_y = y + 1
                self.create_hex(Hex(18*x+6, 6*y+3), hexes, grid_x, grid_y)
                self.world_gen(grid_x, grid_y, planets)
        for x in range(4):
            for y in range(10):
                grid_x = 2*(x + 1)
                grid_y = y + 1
                self.create_hex(Hex(18*x+15, 6*y+6), hexes, grid_x, grid_y)
                self.world_gen(grid_x, grid_y, planets)

    def world_gen(self, grid_x, grid_y, planets):
        if randint(0, 1) == 1:
            # Gas Giant Check 2d6<11
            if roll(2, 6) < 11:
                gas_giant = True
            else:
                gas_giant = False

            # Size 2d6-2
            size = roll(2, 6) - 2

            # Atmosphere 2d6 - 7 + Size
            atmosphere = clamp(0, roll(2, 6) - 7 + size, 15)

            # Temperature
            baseTemperature = roll(2, 6)
            habitableZone = randint(1, 100)
            habDM = 0

            if atmosphere <= 3:
                atmosphereDM = -2
            elif atmosphere <= 5 or atmosphere == 14:
                atmosphereDM = -1
            elif atmosphere <= 7:
                atmosphereDM = 0
            elif atmosphere <= 9:
                atmosphereDM = 1
            elif atmosphere == 10 or atmosphere == 13 or atmosphere == 15:
                atmosphereDM = 2
            else:
                atmosphereDM = 6

            if habitableZone <= 10:
                habDM = -4
            elif habitableZone >= 90:
                habDM = 4

            if atmosphere <= 1:
                Temperature = 1
            else:
                calcTemp = baseTemperature + atmosphereDM + habDM
                if calcTemp <= 2:
                    Temperature = 2
                elif calcTemp <= 4:
                    Temperature = 3
                elif calcTemp <= 9:
                    Temperature = 4
                elif calcTemp <= 11:
                    Temperature = 5
                else:
                    Temperature = 6

            # Hydrographics
            baseHydrographics = roll(2, 6) - 7 + size
            atmosphereHydroDM = 0
            temperatureHydroDM = 0

            if size <= 1:
                Hydrographics = 0
            else:
                if atmosphere <= 1 or 10 <= atmosphere <= 12:
                    atmosphereHydroDM = -4

                if Temperature == 5:
                    temperatureHydroDM = -2
                elif Temperature == 6:
                    temperatureHydroDM = -4

                Hydrographics = baseHydrographics + atmosphereHydroDM + temperatureHydroDM

            # Population
            Population = max(1, roll(2, 6) - 2)

            # Government
            Government = clamp(0, roll(2, 6) - 7 + Population, 13)

            # Law Level
            Law_Level = clamp(0, roll(2, 6) - 7 + Government, 9)

            # Starport
            Starport = roll(2, 6)

            # Tech Level
            baseTL = randint(1, 6)

            if 11 <= Starport <= 12:
                starTL = baseTL + 6
            elif 9 <= Starport <= 10:
                starTL = baseTL + 4
            elif 7 <= Starport <= 8:
                starTL = baseTL + 2
            elif Starport == 2:
                starTL = baseTL - 4
            else:
                starTL = baseTL

            if 0 <= size <= 1:
                sizeTL = starTL + 2
            elif 2 <= size <= 4:
                sizeTL = starTL + 1
            else:
                sizeTL = starTL

            if (0 <= atmosphere <= 3) or (10 <= atmosphere <= 15):
                atmoTL = sizeTL + 1
            else:
                atmoTL = sizeTL

            if Hydrographics == 0 or Hydrographics == 9:
                hydroTL = atmoTL + 1
            elif Hydrographics == 10:
                hydroTL = atmoTL + 2
            else:
                hydroTL = atmoTL

            if 1 <= Population <= 5 or Population == 9:
                popTL = hydroTL + 1
            elif Population == 10:
                popTL = hydroTL + 2
            elif Population == 11:
                popTL = hydroTL + 3
            elif Population == 12:
                popTL = hydroTL + 4
            else:
                popTL = hydroTL

            if Government == 0 or Government == 5:
                govTL = popTL + 1
            elif Government == 7:
                govTL = popTL + 2
            elif Government == 13 or Government == 14:
                govTL = popTL - 2
            else:
                govTL = popTL

            if (0 <= atmosphere <= 1) and (govTL < 8):
                finalTL = 8
            elif (2 <= atmosphere <= 3) and (govTL < 5):
                finalTL = 5
            elif (atmosphere == 4 or atmosphere == 7 or atmosphere == 9) and (govTL < 3):
                finalTL = 3
            elif (atmosphere == 10) and (govTL < 8):
                finalTL = 8
            elif (atmosphere == 11) and (govTL < 9):
                finalTL = 9
            elif (atmosphere == 12) and (govTL < 10):
                finalTL = 10
            elif (13 <= atmosphere <= 14) and (govTL < 5):
                finalTL = 5
            elif (atmosphere == 15) and (govTL < 8):
                finalTL = 8
            else:
                finalTL = max(0, govTL)

            World = Planet(grid_x, grid_y, size, atmosphere, Temperature, Hydrographics, Population, Government,
                           Law_Level, finalTL, gas_giant)

            print(World.grid_x)
            print(World.grid_y)
            planets.append(World)
