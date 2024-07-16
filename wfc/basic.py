import random
from enum import Enum


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

TileID = int
Socket = str
Coordinate = tuple[int, int]
Sockets = dict[Direction, Socket]


class Tile:
    def __init__(self, id: TileID, sockets: Sockets) -> None:
        self._id: TileID = id
        self._sockets: Sockets = sockets

    def get_sockets(self) -> Sockets:
        return self._sockets

    def get_socket(self, direction: Direction) -> Socket:
        return self._sockets[direction]

    def get_id(self) -> TileID:
        return self._id


class TileSuperposition:
    def __init__(self, possibilities: list[Tile]) -> None:
        assert len(possibilities) > 0
        self._possibilities: list[Tile] = possibilities.copy()

    def has_collapsed(self) -> bool:
        return len(self._possibilities) == 1

    def is_valid(self) -> bool:
        return len(self._possibilities) > 0

    def get_possibilities(self) -> list[Tile]:
        return self._possibilities

    def remove(self, possibility: Tile) -> None:
        if possibility in self._possibilities:
            self._possibilities.remove(possibility)

    def propagate(self, other: "TileSuperposition", direction: Direction) -> bool:
        """
        Given the remaining possible states for this superposition, and therefore the remaining possible sockets
        in the given direction, propagate this information to the other superposition.

        Return whether or not the other superposition was affected by this propagation.
        """

        possible_sockets: list[Socket] = [p.get_socket(direction) for p in self._possibilities]

        possibilities_to_remove: list[Tile] = []
        for other_possibility in other.get_possibilities():
            if other_possibility.get_socket(_opposite_direction[direction]) not in possible_sockets:
                possibilities_to_remove.append(other_possibility)

        for p in possibilities_to_remove:
            other.remove(p)


        return len(possibilities_to_remove) > 0

    def collapse(self) -> None:
        """Collapse the superposition into a single known state."""

        assert self.is_valid()

        # TODO: Support arbitrary weights for each possibility
        # Collapse the possibilities into a single state
        self._possibilities = [random.choice(self._possibilities)]

    def get_entropy(self) -> int:
        return len(self._possibilities)

    def get_collapsed_state(self) -> Tile:
        assert self.has_collapsed()
        return self._possibilities[0]


class Grid:
    def __init__(self, grid_size: int, tiles: list[Tile]) -> None:
        self._grid_size = grid_size
        self._tiles = tiles
        self._tile_superpositions: list[list[TileSuperposition]] = [
            [TileSuperposition(self._tiles) for _ in range(grid_size)] for _ in range(grid_size)
        ]

    def get_grid(self) -> list[list[TileSuperposition]]:
        return self._tile_superpositions

    def collapse(self) -> None:
        still_collapsing = True

        while still_collapsing:
            still_collapsing = self._collapse_lowest_entropy_tile_superposition()

    def _get_tile_superposition(self, coordinate: Coordinate) -> TileSuperposition:
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

    def _collapse_lowest_entropy_tile_superposition(self) -> bool:
        """
        Collapse a single tile superposition down to a known state, and propagate the changes to the rest of the grid.

        Returns `True` if this was completed successfully.
        Returns `False` otherwise, including when the grid is in a completely known state.
        """
        lowest_entropy_indices: list[Coordinate] = []
        lowest_entropy: int = 99999

        for row_idx, row in enumerate(self._tile_superpositions):
            for col_idx, tile_superposition in enumerate(row):
                assert tile_superposition.is_valid()

                if not tile_superposition.has_collapsed():
                    if tile_superposition.get_entropy() < lowest_entropy:
                        lowest_entropy_indices.clear()
                        lowest_entropy = tile_superposition.get_entropy()
                        lowest_entropy_indices.append((row_idx, col_idx))

                    elif tile_superposition.get_entropy() == lowest_entropy:
                        lowest_entropy_indices.append((row_idx, col_idx))

        if len(lowest_entropy_indices) == 0:
            return False

        lowest_entropy_index = random.choice(lowest_entropy_indices)

        self._get_tile_superposition(lowest_entropy_index).collapse()
        neighbours_to_propagate_to = self._get_valid_neighbours(lowest_entropy_index)

        while len(neighbours_to_propagate_to) > 0:
            ((source_coords, direction), neighbour_coords) = neighbours_to_propagate_to.popitem()

            source = self._get_tile_superposition(source_coords)
            new_neighbour = self._get_tile_superposition(neighbour_coords)

            was_affected = source.propagate(new_neighbour, direction)

            if was_affected:
                more_neighbours = self._get_valid_neighbours(neighbour_coords)

                for key, new_neighbour in more_neighbours.items():
                    # Don't add the new neighbour if it's the source that has just been processed
                    # I.e. don't try and propagate back where we just came from
                    if new_neighbour != source_coords:
                        neighbours_to_propagate_to[key] = new_neighbour

        return True


    def pretty_print_grid_state(self) -> str:
        output: str = ""
        for row in self.get_grid():
            for tile in row:
                output += f"{[p.get_id() for p in tile.get_possibilities()]}, "

            output += "\n"

        return output
