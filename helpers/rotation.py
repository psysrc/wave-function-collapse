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
