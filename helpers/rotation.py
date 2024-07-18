from enum import IntEnum


class Rotation(IntEnum):
    NONE = 0
    ANTICLOCKWISE = 90
    HALF = 180
    CLOCKWISE = 270


NoRotations = {Rotation.NONE}
"""A set containing only the NONE rotation."""

AllRotations = {Rotation.NONE, Rotation.CLOCKWISE, Rotation.HALF, Rotation.ANTICLOCKWISE}
"""A set containing all rotations."""


rotate_clockwise: dict[Rotation, Rotation] = {
    Rotation.NONE: Rotation.CLOCKWISE,
    Rotation.CLOCKWISE: Rotation.HALF,
    Rotation.HALF: Rotation.ANTICLOCKWISE,
    Rotation.ANTICLOCKWISE: Rotation.NONE,
}

rotate_anticlockwise: dict[Rotation, Rotation] = {
    Rotation.NONE: Rotation.ANTICLOCKWISE,
    Rotation.ANTICLOCKWISE: Rotation.HALF,
    Rotation.HALF: Rotation.CLOCKWISE,
    Rotation.CLOCKWISE: Rotation.NONE,
}
