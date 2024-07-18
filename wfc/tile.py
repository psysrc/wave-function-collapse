from dataclasses import dataclass, field
from helpers.direction import Direction
from helpers.rotation import NoRotations, Rotation
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
