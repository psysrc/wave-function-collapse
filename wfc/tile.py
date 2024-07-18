from dataclasses import dataclass, field
from helpers.direction import Direction, move_anticlockwise
from helpers.rotation import NoRotations, Rotation, rotate_anticlockwise
from wfc.abstract_socket import SocketSet


TileID = int | str

DirectionalSocketSetMap = dict[Direction, SocketSet]


@dataclass
class TileDefinition:
    id: TileID
    socket_sets: DirectionalSocketSetMap
    prob_weight: float = 1
    allowed_rotations: set[Rotation] = field(default_factory=lambda: NoRotations)

    def __post_init__(self) -> None:
        if len(self.allowed_rotations) == 0:
            self.allowed_rotations = NoRotations


def rotate_socket_sets(socket_sets: DirectionalSocketSetMap, rotation: Rotation) -> DirectionalSocketSetMap:
    rotated_socket_sets: DirectionalSocketSetMap = socket_sets.copy()

    while (rotation != Rotation.NONE):
        # Remove one rotation from the rotation value itself, and add one rotation to the socket sets
        rotation = rotate_anticlockwise[rotation]
        rotated_socket_sets = _rotate_socket_sets_clockwise(rotated_socket_sets)

    return rotated_socket_sets


def _rotate_socket_sets_clockwise(socket_sets: DirectionalSocketSetMap) -> DirectionalSocketSetMap:
    rotated_socket_sets: DirectionalSocketSetMap = {
        Direction.UP: socket_sets[move_anticlockwise[Direction.UP]],
        Direction.RIGHT: socket_sets[move_anticlockwise[Direction.RIGHT]],
        Direction.DOWN: socket_sets[move_anticlockwise[Direction.DOWN]],
        Direction.LEFT: socket_sets[move_anticlockwise[Direction.LEFT]],
    }

    return rotated_socket_sets
