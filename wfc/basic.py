from dataclasses import dataclass
import random
from enum import Enum
from helpers.rotation import Rotation
from helpers.flipped import Flipped


class Direction(Enum):
    LEFT = 0
    UP = 1
    DOWN = 2
    RIGHT = 3

_opposite_direction = {
    Direction.LEFT: Direction.RIGHT,
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.RIGHT: Direction.LEFT,
}

TileID = int | str
Socket = int | str
SocketSet = set[Socket]
DirectionalSocketSetMap = dict[Direction, SocketSet]
Coordinate = tuple[int, int]


class Superposition(Enum):
    """Describes the state of a superposition."""

    SUPERPOSITION = 0
    COLLAPSED = 1
    INVALID = 2


@dataclass
class Tile:
    """Describes a tile in a specific position."""

    id: TileID
    rotation: Rotation
    flipped: Flipped


@dataclass
class TileSuperposition:
    """Describes a superposition of tiles."""

    superposition: Superposition

    tile: Tile | None
    """
    If the `superposition` field is `SUPERPOSITION` or `INVALID`, this field will be `None`.
    Otherwise, this field will contain a valid `Tile` instance.
    """


@dataclass
class TileDefinition:
    id: TileID
    socket_sets: DirectionalSocketSetMap
    rotatable: bool = False
    flippable: bool = False


class _InternalTile:
    def __init__(self, id: TileID, socketsets: DirectionalSocketSetMap) -> None:
        self._id: TileID = id
        self._socketsets: DirectionalSocketSetMap = socketsets

    def get_socketsets(self) -> DirectionalSocketSetMap:
        return self._socketsets

    def get_socketset(self, direction: Direction) -> SocketSet:
        return self._socketsets[direction]

    def get_id(self) -> TileID:
        return self._id


def _create_internal_tiles_from_tile_definition(tile_definition: TileDefinition) -> list[_InternalTile]:
    if tile_definition.rotatable:
        raise NotImplementedError("Rotatable tiles are currently unsupported")  # TODO

    if tile_definition.flippable:
        raise NotImplementedError("Flipped tiles are currently unsupported")  # TODO

    return [_InternalTile(tile_definition.id, tile_definition.socket_sets)]


class _TileSuperposition:
    def __init__(self, possibilities: list[_InternalTile], weights: list[float] | None = None) -> None:
        if len(possibilities) == 0:
            raise RuntimeError("Cannot create a superposition containing zero possibilities")

        if weights is not None:
            if len(possibilities) != len(weights):
                raise RuntimeError("Number of weights provided does not match number of possibilities")
        else:
            weights = [1.0] * len(possibilities)

        self._possibilities_and_weights: list[tuple[_InternalTile, float]] = list(zip(possibilities.copy(), weights))

    def has_collapsed(self) -> bool:
        return len(self._possibilities_and_weights) == 1

    def is_valid(self) -> bool:
        return len(self._possibilities_and_weights) > 0

    def get_possibilities(self) -> list[_InternalTile]:
        return [pw[0] for pw in self._possibilities_and_weights]

    def remove(self, possibility: _InternalTile) -> None:
        for pw in self._possibilities_and_weights:
            match pw:
                case (p, w) if p == possibility:
                    self._possibilities_and_weights.remove((p, w))
                    break

    def propagate(self, other: "_TileSuperposition", direction: Direction) -> bool:
        """
        Given the remaining possible states for this superposition, and therefore the remaining possible sockets
        in the given direction, propagate this information to the other superposition.

        Return whether or not the other superposition was affected by this propagation.
        """

        possible_sockets: SocketSet = set()
        possible_socketsets: list[SocketSet] = [p.get_socketset(direction) for (p, _) in self._possibilities_and_weights]
        for ss in possible_socketsets:
            possible_sockets = possible_sockets.union(ss)

        possibilities_to_remove: list[_InternalTile] = []
        for other_possibility in other.get_possibilities():
            if other_possibility.get_socketset(_opposite_direction[direction]).isdisjoint(possible_sockets):
                possibilities_to_remove.append(other_possibility)

        for p in possibilities_to_remove:
            other.remove(p)

        return len(possibilities_to_remove) > 0

    def collapse(self) -> None:
        """Collapse the superposition into a single known state."""

        if not self.is_valid() or self.has_collapsed():
            return

        weights = [w for (_, w) in self._possibilities_and_weights]

        self._possibilities_and_weights = random.choices(self._possibilities_and_weights, weights=weights)

    def get_entropy(self) -> int:
        return len(self._possibilities_and_weights)

    def get_collapsed_state(self) -> _InternalTile:
        if not self.is_valid():
            raise RuntimeError("Cannot get collapsed state of an invalid supoerposition")

        if not self.has_collapsed():
            raise RuntimeError("Cannot get collapsed state of an uncollapsed superposition")

        return self._possibilities_and_weights[0][0]


class Grid:
    def __init__(self, grid_size: int, tile_definitions: list[TileDefinition], weights: list[float] | None = None) -> None:
        self._grid_size = grid_size

        self._tiles: list[_InternalTile] = []
        for tile_def in tile_definitions:
            self._tiles.extend(_create_internal_tiles_from_tile_definition(tile_def))

        self._tile_superpositions: list[list[_TileSuperposition]] = [
            [_TileSuperposition(self._tiles, weights) for _ in range(grid_size)] for _ in range(grid_size)
        ]

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
                    tile = tile_superposition.get_collapsed_state()
                    result[row_idx].append(TileSuperposition(Superposition.COLLAPSED, Tile(tile.get_id(), rotation=Rotation.NONE, flipped=Flipped.NONE)))
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
            (coordinate, Direction.LEFT): (coordinate[0], coordinate[1]-1),
            (coordinate, Direction.UP): (coordinate[0]-1, coordinate[1]),
            (coordinate, Direction.DOWN): (coordinate[0]+1, coordinate[1]),
            (coordinate, Direction.RIGHT): (coordinate[0], coordinate[1]+1),
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
        lowest_entropy: int = 99999

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

    def collapse_tile_superposition(self, coordinate: Coordinate) -> bool:
        """
        Collapse a single tile superposition down to a known state, and propagate the changes to the rest of the grid.

        Returns `True` if this was completed successfully.
        Returns `False` otherwise, including when the grid is in a completely known state.
        """

        self._get_tile_superposition(coordinate).collapse()
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

        return True



    def pretty_print_grid_state(self) -> str:
        output: str = ""
        for row in self._tile_superpositions:
            for tile in row:
                output += f"{[p.get_id() for p in tile.get_possibilities()]}, "

            output += "\n"

        return output
