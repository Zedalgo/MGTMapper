import tcod as libtcod

from random import randint
from tile import Tile
from shapes import Hex
from entity import Entity
from richard_help import clamp


class ssMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_hex(self, room):
        # Generates a hex shape using 3 rectangles
        for x in range(room.x - 3, room.x + 4):
            for y in range(room.y - 2, room.y + 3):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        for x in range(room.x - 4, room.x + 5):
            for y in range(room.y - 1, room.y + 2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        for x in range(room.x - 5, room.x + 6):
            self.tiles[x][room.y].blocked = False
            self.tiles[x][room.y].block_sight = False

    def make_map(self, entities):
        # Create the Hex Grid
        for x in range(4):
            for y in range(10):
                self.create_hex(Hex(18*x+6, 6*y+3))
                self.world_gen(Hex(18*x+6, 6*y+3), entities)
        for x in range(4):
            for y in range(10):
                self.create_hex(Hex(18*x+15, 6*y+6))
                self.world_gen(Hex(18*x+15, 6*y+6), entities)

    def world_gen(self, room, entities):
        if randint(0, 1) == 1:
            populated_hex = Entity(room.x, room.y - 1, 'O', libtcod.white)
            entities.append(populated_hex)
            if randint(1, 6) + randint(1, 6) < 11:
                GasGiant = Entity(room.x+2, room.y-1, 'G', libtcod.dark_orange)
                entities.append(GasGiant)

            """
            World Size
            2d6-2
            """
            size = randint(1, 6) + randint(1, 6) - 2
            if size < 10:
                sizdes = size
            else:
                sizdes = 'A'

            """
            Atmosphere
            2d6-7 + size
            """
            atmo = randint(1, 6) + randint(1, 6) - 7 + size
            if atmo < 0:
                atmodes = 0
            elif atmo < 10:
                atmodes = atmo
            elif atmo == 10:
                atmodes = 'A'
            elif atmo == 11:
                atmodes = 'B'
            elif atmo == 12:
                atmodes = 'C'
            elif atmo == 13:
                atmodes = 'D'
            elif atmo == 14:
                atmodes = 'E'
            else:
                atmodes = 'F'

            """
            Temperature
            2d6 +- AtmosphereMods +- HabZoneLocation
            """
            worldtempbase = randint(1, 6) + randint(1, 6)
            habzonevalue = randint(1, 100)

            if atmo < 2:
                tempA = -30
                # Swinging temp is arbitrarily set to -30 bc it is outside reachable values for normal gen
            elif atmo < 4:
                tempA = worldtempbase - 2
            elif atmo < 6 or atmo == 14:
                tempA = worldtempbase - 1
            elif atmo < 8:
                tempA = worldtempbase
            elif atmo < 10:
                tempA = worldtempbase + 1
            elif (atmo == 10) or (atmo == 13) or (atmo == 15):
                tempA = worldtempbase + 2
            else:
                tempA = worldtempbase + 6

            if (tempA == -30) or (15 < habzonevalue < 86):
                tempB = tempA
            elif habzonevalue < 16:
                tempB = tempA - 4
            else:
                tempB = tempA + 4

            """
            The Final Temperature
            1 - Swinging Temp
            2 - Frozen
            3 - Cold
            4 - Temperate
            5 - Hot
            6 - Roasting
            """
            if tempB == -30:
                worldTemp = 1
            elif tempB < 3:
                worldTemp = 2
            elif tempB < 5:
                worldTemp = 3
            elif tempB < 10:
                worldTemp = 4
            elif tempB < 12:
                worldTemp = 5
            else:
                worldTemp = 6

            """
            Hydrographics
            """
            baseWetness = randint(1, 6) + randint(1, 6) - 7 + size

            if (-1 < atmo < 2) or (9 < atmo < 13):
                atmoWetness = baseWetness - 4
            else:
                atmoWetness = baseWetness

            if size < 2:
                wetness = 0
            elif worldTemp == 5:
                wetness = atmoWetness - 2
            elif worldTemp == 6:
                wetness = atmoWetness - 6
            else:
                wetness = atmoWetness

            if wetness < 0:
                wetness = 0
            elif wetness > 9:
                wetness = 'A'

            """
            Population
            """
            ultraPop = randint(1, 100)
            if ultraPop == 100:
                population = randint(1, 6) + randint(1, 6)
            elif ultraPop > 95:
                population = randint(1, 6) + randint(1, 6) - 1
            else:
                population = randint(1, 6) + randint(1, 6) - 2

            if population == 10:
                popdes = 'A'
            elif population == 11:
                popdes = 'B'
            elif population == 12:
                popdes = 'C'
            elif population == 13:
                popdes = 'D'
            elif population == 14:
                popdes = 'E'
            elif population == 15:
                popdes = 'F'
            else:
                popdes = population

            """
            Gov't
            """
            baseGovt = randint(1, 6) + randint(1, 6) - 7 + population

            if baseGovt == 10:
                govtdes = 'A'
            elif baseGovt == 11:
                govtdes = 'B'
            elif baseGovt == 12:
                govtdes = 'C'
            elif baseGovt >= 13:
                govtdes = 'D'
            elif (baseGovt < 0) and (population > 5):
                govtdes = 7
            elif baseGovt < 0:
                govtdes = 0
            else:
                govtdes = baseGovt

            """
            Minor Factions to be added whn I can actually display them
            """

            """
            Law Level
            """
            lawdes = clamp(0, randint(1, 6) + randint(1, 6) - 7 + baseGovt, 9)

            """
            Starport
            """
            starport = randint(1, 6) + randint(1, 6)
            if starport == 2:
                stardes = 'X'
            elif starport < 5:
                stardes = 'E'
            elif starport < 7:
                stardes = 'D'
            elif starport < 9:
                stardes = 'C'
            elif starport < 11:
                stardes = 'B'
            else:
                stardes = 'A'

            """
            Starport Fixtures and Bases
            """
            # Coming Soon^(tm)
            """
            Tech Level
            """
            baseTL = randint(1, 6)

            if starport == 'A':
                starTL = baseTL + 6
            elif starport == 'B':
                starTL = baseTL + 4
            elif starport == 'C':
                starTL = baseTL + 2
            elif starport == 'X':
                starTL = baseTL - 4
            else:
                starTL = baseTL

            if 0 <= size <= 1:
                sizeTL = starTL + 2
            elif 2 <= size <= 4:
                sizeTL = starTL + 1
            else:
                sizeTL = starTL

            if (0 <= atmo <= 3) or (10 <= atmo <= 15):
                atmoTL = sizeTL + 1
            else:
                atmoTL = sizeTL

            if wetness == 0 or wetness == 9:
                hydroTL = atmoTL + 1
            elif wetness == 'A':
                hydroTL = atmoTL + 2
            else:
                hydroTL = atmoTL

            if 1 <= population <= 5 or population == 9:
                popTL = hydroTL + 1
            elif population == 'A':
                popTL = hydroTL + 2
            elif population == 'B':
                popTL = hydroTL + 3
            elif population == 'C':
                popTL = hydroTL + 4
            else:
                popTL = hydroTL

            if govtdes == 0 or govtdes == 5:
                govTL = popTL + 1
            elif govtdes == 7:
                govTL = popTL + 2
            elif govtdes == 'D' or govtdes == 'E':
                govTL = popTL - 2
            else:
                govTL = popTL

            if (0 <= atmo <= 1) and (govTL < 8):
                finalTL = 8
            elif (2 <= atmo <= 3) and (govTL < 5):
                finalTL = 5
            elif (atmo == 4 or atmo == 7 or atmo == 9) and (govTL < 3):
                finalTL = 3
            elif (atmodes == 'A') and (govTL < 8):
                finalTL = 8
            elif (atmodes == 'B') and (govTL < 9):
                finalTL = 9
            elif (atmodes == 'C') and (govTL < 10):
                finalTL = 10
            elif (13 <= atmo <= 14) and (govTL < 5):
                finalTL = 5
            elif (atmodes == 'F') and (govTL < 8):
                finalTL = 8
            elif govTL < 0:
                finalTL = 0
            else:
                finalTL = govTL

            """
            Travel Code Display
            """
            # Starport
            tcSPort = Entity(room.x - 5, room.y, str(stardes), libtcod.white)
            entities.append(tcSPort)
            # Size, Atmo, Hydro, Pop, Gov't, Law
            tcSize = Entity(room.x - 3, room.y, str(sizdes), libtcod.white)
            entities.append(tcSize)
            tcAtmo = Entity(room.x - 2, room.y, str(atmodes), libtcod.white)
            entities.append(tcAtmo)
            tcHydro = Entity(room.x - 1, room.y, str(wetness), libtcod.white)
            entities.append(tcHydro)
            tcPop = Entity(room.x, room.y, str(popdes), libtcod.white)
            entities.append(tcPop)
            tcGovt = Entity(room.x + 1, room.y, str(govtdes), libtcod.white)
            entities.append(tcGovt)
            tcLaw = Entity(room.x + 2, room.y, str(lawdes), libtcod.white)
            entities.append(tcLaw)
            # A dash (-)
            hyphon = Entity(room.x + 3, room.y, 45, libtcod.white)
            entities.append(hyphon)
            # Tech Level
            stringTL = str(finalTL)
            if finalTL > 9:
                TLev1 = Entity(room.x + 4, room.y, stringTL[:1], libtcod.white)
                entities.append(TLev1)
                TLev2 = Entity(room.x + 5, room.y, stringTL[:-1], libtcod.white)
                entities.append(TLev2)
            else:
                TLev = Entity(room.x + 5, room.y, str(finalTL), libtcod.white)
                entities.append(TLev)
