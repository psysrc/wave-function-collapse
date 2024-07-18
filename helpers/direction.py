from enum import Enum


class Direction(Enum):
    LEFT = 0
    UP = 1
    DOWN = 2
    RIGHT = 3


opposite_direction = {
    Direction.LEFT: Direction.RIGHT,
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.RIGHT: Direction.LEFT,
}
"""Maps directions onto their opposites. For example, UP --> DOWN."""


move_clockwise: dict[Direction, Direction] = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}


move_anticlockwise: dict[Direction, Direction] = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP,
}
