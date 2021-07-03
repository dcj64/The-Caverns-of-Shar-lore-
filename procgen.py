import random
from typing import Iterator, Tuple

import tcod

from game_map import GameMap
import tile_types


class RetangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
)  -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5: # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    #Generate the co-ordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RetangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RetangularRoom(x=35, y=15, width=10, height=15)
    room_3 = RetangularRoom(x=50, y=3, width=10, height=10)
    room_4 = RetangularRoom(x=5, y=5, width=10, height=10)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor
    dungeon.tiles[room_3.inner] = tile_types.floor
    dungeon.tiles[room_4.inner] = tile_types.floor

    for x, y in tunnel_between(room_2.center, room_1.center):
        dungeon.tiles[x, y] = tile_types.floor
    for x, y in tunnel_between(room_2.center, room_3.center):
        dungeon.tiles[x, y] = tile_types.floor
    for x, y in tunnel_between(room_1.center, room_4.center):
        dungeon.tiles[x, y] = tile_types.floor

    return dungeon
