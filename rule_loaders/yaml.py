from typing import Any
import yaml
from pathlib import Path
from wfc.tile import TileDefinition, DirectionalSocketSetMap
from wfc.basic_socket import SocketID, BasicSocket, SocketType
from helpers.rotation import Rotation
from helpers.direction import Direction


class YamlRulesLoader:
    _supported_file_versions = [1]

    def __init__(self, yaml_file: Path) -> None:
        self._data = yaml.load(yaml_file.open(), Loader=yaml.Loader)

        match self._data:
            case {"version": version}:
                if version not in self._supported_file_versions:
                    raise RuntimeError(f"Unsupported file version {version}: (supported versions are {self._supported_file_versions})")

            case _:
                raise RuntimeError("Failed to get rule configuration version")

    def load(self) -> list[TileDefinition]:
        socket_defs = self._load_socket_data()

        tiles = self._load_tile_data(socket_defs)

        return tiles

    def _load_tile_data(self, socket_defs: dict[SocketID, BasicSocket]) -> list[TileDefinition]:
        match self._data:
            case {"tiles": [*tiles]}:
                tiles = self._load_tiles(tiles, socket_defs)

                return tiles

            case _:
                raise RuntimeError("Failed to parse tile definitions")

    @staticmethod
    def _load_tiles(tiles: list[Any], socket_defs: dict[SocketID, BasicSocket]) -> list[TileDefinition]:
        tile_definitions: list[TileDefinition] = []

        for tile_data in tiles:
            match tile_data:
                case {"id": id, "sockets": socket_sets, **extra_data}:
                    socket_sets = YamlRulesLoader._load_tile_socket_sets(socket_sets, socket_defs)

                    extras = {}
                    if "prob_weight" in extra_data:
                        extras["prob_weight"] = float(extra_data["prob_weight"])
                    if "allowed_rotations" in extra_data:
                        extras["allowed_rotations"] = YamlRulesLoader._load_allowed_rotations(extra_data["allowed_rotations"])

                    tile_definition = TileDefinition(id=id, socket_sets=socket_sets, **extras)

                    tile_definitions.append(tile_definition)

                case _:
                    raise RuntimeError(f"Failed to parse tile definition: {repr(tile_data)}")

        return tile_definitions

    @staticmethod
    def _load_allowed_rotations(allowed_rotations_data: Any) -> set[Rotation]:
        rotations: set[Rotation] = set()

        match allowed_rotations_data:
            case [*rotations_data]:

                for rotation_data in rotations_data:
                    match rotation_data:
                        case "none":
                            rotations.add(Rotation.NONE)
                        case "clockwise":
                            rotations.add(Rotation.CLOCKWISE)
                        case "anticlockwise":
                            rotations.add(Rotation.ANTICLOCKWISE)
                        case "half":
                            rotations.add(Rotation.HALF)

                        case _:
                            raise RuntimeError(f"Failed to parse allowed rotation definition: {repr(rotation_data)}")

            case _:
                raise RuntimeError(f"Failed to parse allowed rotations definition: {repr(allowed_rotations_data)}")

        return rotations

    @staticmethod
    def _load_tile_socket_sets(socket_sets: Any, socket_defs: dict[SocketID, BasicSocket]) -> DirectionalSocketSetMap:
        match socket_sets:
            case {"left": [*left_data], "right": [*right_data], "up": [*up_data], "down": [*down_data]}:

                return {
                    Direction.UP: {socket_defs[s] for s in up_data},
                    Direction.LEFT: {socket_defs[s] for s in left_data},
                    Direction.RIGHT: {socket_defs[s] for s in right_data},
                    Direction.DOWN: {socket_defs[s] for s in down_data},
                }

            case _:
                raise RuntimeError(f"Failed to parse socket set definitions: {repr(socket_sets)}")

    def _load_socket_data(self) -> dict[SocketID, BasicSocket]:
        match self._data:
            case {"sockets": [*sockets]}:
                return self._load_sockets(sockets)

            case _:
                raise RuntimeError("Failed to parse socket definitions")

    @staticmethod
    def _load_sockets(sockets_data: list[Any]) -> dict[SocketID, BasicSocket]:
        sockets: dict[SocketID, BasicSocket] = {}

        for socket_data in sockets_data:
            match socket_data:
                case {"id": id, "type": "symmetric"}:
                    symmetric_socket = BasicSocket(id=id, type=SocketType.SYMMETRIC)
                    sockets[id] = symmetric_socket

                case {"id": id, "type": "asymmetric", "counterpart": counterpart}:
                    asymmetric_socket = BasicSocket(id=id, type=SocketType.ASYMMETRIC)
                    sockets[id] = asymmetric_socket
                    sockets[counterpart] = asymmetric_socket.asymmetric_counterpart()

                case _:
                    raise RuntimeError(f"Failed to parse socket definition: {repr(socket_data)}")

        return sockets
