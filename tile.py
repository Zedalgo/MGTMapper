class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight


class HexInfo:
    def __init__(self, x, y, hex_x, hex_y):
        self.x = x
        self.y = y
        self.hex_x = hex_x
        self.hex_y = hex_y
