from dataclasses import dataclass
import random
from enum import Enum
from helpers.rotation import Rotation
from wfc.abstract_socket import SocketSet
from wfc.tile import TileDefinition, TileID, DirectionalSocketSetMap, rotate_socket_sets
from helpers.direction import Direction, opposite_direction


Entropy = int


class Superposition(Enum):
    """Describes the state of a superposition."""

    SUPERPOSITION = 0
    COLLAPSED = 1
    INVALID = 2


@dataclass(frozen=True)
class TileDeployment:
    """Describes a tile in a specific position."""

    id: TileID
    rotation: Rotation = Rotation.NONE


@dataclass
class TileSuperposition:
    """Describes a superposition of tiles."""

    superposition: Superposition

    tile: TileDeployment | None  # TODO: Make this a list of TileDeployment, and maybe get rid of `superposition`
    """
    If the `superposition` field is `SUPERPOSITION` or `INVALID`, this field will be `None`.
    Otherwise, this field will contain a valid `Tile` instance.
    """

@dataclass
class _InternalTileDeployment:
    tile_deployment: TileDeployment
    socket_sets: DirectionalSocketSetMap


Coordinate = tuple[int, int]


class _TileSuperposition:
    def __init__(self, possibilities: list[_InternalTileDeployment]) -> None:
        if len(possibilities) == 0:
            raise RuntimeError("Cannot create a superposition containing zero possibilities")

        self._possibilities: list[_InternalTileDeployment] = possibilities.copy()

    def has_collapsed(self) -> bool:
        return len(self._possibilities) == 1

    def is_valid(self) -> bool:
        return len(self._possibilities) > 0

    def get_possibilities(self) -> list[_InternalTileDeployment]:
        return self._possibilities

    def remove(self, possibility: _InternalTileDeployment) -> None:
        if possibility in self._possibilities:
            self._possibilities.remove(possibility)

    def propagate(self, other: "_TileSuperposition", direction: Direction) -> bool:
        """
        Given the remaining possible states for this superposition, and therefore the remaining possible sockets
        in the given direction, propagate this information to the other superposition.

        Return whether or not the other superposition was affected by this propagation.
        """

        possible_sockets: SocketSet = set()
        possible_socketsets: list[SocketSet] = [p.socket_sets[direction] for p in self._possibilities]
        for ss in possible_socketsets:
            possible_sockets = possible_sockets.union(ss)

        possibilities_to_remove: list[_InternalTileDeployment] = []
        for other_possibility in other.get_possibilities():
            other_socket_set = other_possibility.socket_sets[opposite_direction[direction]]
            if not socket_sets_are_compatible(other_socket_set, possible_sockets):
                possibilities_to_remove.append(other_possibility)

        for p in possibilities_to_remove:
            other.remove(p)

        return len(possibilities_to_remove) > 0

    def collapse(self, final_state: _InternalTileDeployment) -> None:
        """Collapse the superposition into a single known state."""

        if final_state not in self._possibilities:
            raise RuntimeError("Cannot collapse superposition into a state that is not one of its possibilities")

        self._possibilities = [final_state]

    def get_entropy(self) -> Entropy:
        return len(self._possibilities)

    def get_collapsed_state(self) -> _InternalTileDeployment:
        if not self.is_valid():
            raise RuntimeError("Cannot get collapsed state of an invalid supoerposition")

        if not self.has_collapsed():
            raise RuntimeError("Cannot get collapsed state of an uncollapsed superposition")

        return self._possibilities[0]


class Grid:
    def __init__(self, grid_size: int, tile_definitions: list[TileDefinition]) -> None:
        self._grid_size = grid_size

        self._tile_definitions = tile_definitions

        self._tiles: list[_InternalTileDeployment] = []
        for tile_def in tile_definitions:
            self._tiles.extend(self._create_tile_deployments_from_tile_definition(tile_def))

        self._tile_superpositions: list[list[_TileSuperposition]] = [
            [_TileSuperposition(self._tiles) for _ in range(grid_size)] for _ in range(grid_size)
        ]

    @staticmethod
    def _create_tile_deployments_from_tile_definition(tile_def: TileDefinition) -> list[_InternalTileDeployment]:
        tile_deployments: list[_InternalTileDeployment] = []

        for rotation in tile_def.allowed_rotations:
            tile_deployments.append(_InternalTileDeployment(
                TileDeployment(tile_def.id, rotation=rotation),
                socket_sets=rotate_socket_sets(tile_def.socket_sets, rotation),
            ))

        return tile_deployments

    def is_valid(self) -> bool:
        for row in self._tile_superpositions:
            for tile_superposition in row:
                if not tile_superposition.is_valid():
                    return False

        return True

    def has_collapsed(self) -> bool:
        for row in self._tile_superpositions:
            for tile_superposition in row:
                if not tile_superposition.has_collapsed():
                    return False

        return True

    def get_grid_size(self) -> int:
        return self._grid_size

    def get_grid(self) -> list[list[TileSuperposition]]:
        result: list[list[TileSuperposition]] = []

        for row_idx, row in enumerate(self._tile_superpositions):
            result.append([])

            for tile_superposition in row:
                if not tile_superposition.is_valid():
                    result[row_idx].append(TileSuperposition(Superposition.INVALID, None))
                elif tile_superposition.has_collapsed():
                    internal_tile = tile_superposition.get_collapsed_state()
                    result[row_idx].append(TileSuperposition(Superposition.COLLAPSED, internal_tile.tile_deployment))
                else:
                    result[row_idx].append(TileSuperposition(Superposition.SUPERPOSITION, None))

        return result

    def collapse(self) -> None:
        """Collapse the whole grid into a single known state."""

        while True:
            lowest_entropy_coordinate: Coordinate | None = self.find_lowest_entropy_tile_superposition()

            if lowest_entropy_coordinate is None:
                break

            self.collapse_tile_superposition(lowest_entropy_coordinate)

    def _get_tile_superposition(self, coordinate: Coordinate) -> _TileSuperposition:
        return self._tile_superpositions[coordinate[0]][coordinate[1]]

    def _is_coordinate_valid(self, coordinate: Coordinate) -> bool:
        return coordinate[0] >= 0 and coordinate[0] < self._grid_size and coordinate[1] >= 0 and coordinate[1] < self._grid_size

    def _get_valid_neighbours(self, coordinate: Coordinate) -> dict[tuple[Coordinate, Direction], Coordinate]:
        """
        Return all valid neighbours of a coordinate.

        Return value is a dict (C, D) --> N where
        C is the coordinate provided,
        D is the direction from C,
        N is the neighbour.
        """

        possible_neighbours = {
            (coordinate, Direction.LEFT): (coordinate[0], coordinate[1] - 1),
            (coordinate, Direction.UP): (coordinate[0] - 1, coordinate[1]),
            (coordinate, Direction.DOWN): (coordinate[0] + 1, coordinate[1]),
            (coordinate, Direction.RIGHT): (coordinate[0], coordinate[1] + 1),
        }

        neighbours: dict[tuple[Coordinate, Direction], Coordinate] = {}
        for k, n in possible_neighbours.items():
            if self._is_coordinate_valid(n):
                neighbours[k] = n

        return neighbours

    def find_lowest_entropy_tile_superposition(self) -> Coordinate | None:
        """
        Return the coordinates of a valid tile superposition that has the lowest entropy and has not yet collapsed.

        `None` is returned if the grid is fully collapsed.
        """

        lowest_entropy_indices: list[Coordinate] = []
        lowest_entropy: Entropy = 99999

        for row_idx, row in enumerate(self._tile_superpositions):
            for col_idx, tile_superposition in enumerate(row):
                if tile_superposition.is_valid() and not tile_superposition.has_collapsed():
                    if tile_superposition.get_entropy() < lowest_entropy:
                        lowest_entropy_indices.clear()
                        lowest_entropy = tile_superposition.get_entropy()
                        lowest_entropy_indices.append((row_idx, col_idx))

                    elif tile_superposition.get_entropy() == lowest_entropy:
                        lowest_entropy_indices.append((row_idx, col_idx))

        if len(lowest_entropy_indices) == 0:
            return None

        lowest_entropy_index = random.choice(lowest_entropy_indices)
        return lowest_entropy_index

    def _collapse_tile_superposition(self, coordinate: Coordinate) -> None:
        tile_superposition = self._get_tile_superposition(coordinate)

        if not tile_superposition.is_valid() or tile_superposition.has_collapsed():
            return

        current_possibilities = tile_superposition.get_possibilities()

        possible_tile_ids: set[TileID] = {p.tile_deployment.id for p in current_possibilities}
        possible_tile_definitions: list[TileDefinition] = [d for d in self._tile_definitions if d.id in possible_tile_ids]
        tile_definition_weights: list[float] = [d.prob_weight for d in self._tile_definitions if d.id in possible_tile_ids]

        final_tile_definition: TileDefinition = random.choices(possible_tile_definitions, weights=tile_definition_weights)[0]

        new_possibilities: list[_InternalTileDeployment] = [p for p in current_possibilities if p.tile_deployment.id == final_tile_definition.id]
        new_possibility = random.choice(new_possibilities)

        tile_superposition.collapse(new_possibility)

    def collapse_tile_superposition(self, coordinate: Coordinate) -> None:
        """
        Collapse a single tile superposition down to a known state, and propagate the changes to the rest of the grid.

        Returns `True` if this was completed successfully.
        Returns `False` otherwise, including when the grid is in a completely known state.
        """

        self._collapse_tile_superposition(coordinate)

        neighbours_to_propagate_to = self._get_valid_neighbours(coordinate)

        while len(neighbours_to_propagate_to) > 0:
            ((source_coords, direction), neighbour_coords) = neighbours_to_propagate_to.popitem()

            source = self._get_tile_superposition(source_coords)
            new_neighbour = self._get_tile_superposition(neighbour_coords)

            was_affected = source.propagate(new_neighbour, direction)

            if was_affected and new_neighbour.is_valid():
                more_neighbours = self._get_valid_neighbours(neighbour_coords)

                for key, new_neighbour in more_neighbours.items():
                    # Don't add the new neighbour if it's the source that has just been processed
                    # I.e. don't try and propagate back where we just came from
                    if new_neighbour != source_coords:
                        neighbours_to_propagate_to[key] = new_neighbour

    def pretty_print_grid_state(self) -> str:
        output: str = ""
        for row in self._tile_superpositions:
            for tile in row:
                output += f"{[p.tile_deployment.id for p in tile.get_possibilities()]}, "

            output += "\n"

        return output


def socket_sets_are_compatible(first: SocketSet, second: SocketSet) -> bool:
    for fs in first:
        for ss in second:
            if fs.compatible_with(ss):
                return True

    return False
