from dataclasses import dataclass
from helpers.direction import Direction
from wfc.abstract_socket import SocketSet


TileID = int | str

DirectionalSocketSetMap = dict[Direction, SocketSet]


@dataclass
class TileDefinition:
    id: TileID
    socket_sets: DirectionalSocketSetMap
    prob_weight: float = 1
    rotatable: bool = False
    flippable: bool = False
