TileID = int
Socket = str
Sockets = tuple[Socket, Socket, Socket, Socket]  # Left, Up, Down, Right

class Tile:
    def __init__(self, id: TileID, sockets: Sockets) -> None:
        self._id: TileID = id
        self._sockets: Sockets = sockets

    def get_sockets(self) -> Sockets:
        return self._sockets

    def get_id(self) -> TileID:
        return self._id


class TileSuperposition:
    def __init__(self, possibilities: list[TileID]) -> None:
        self._possibilities: list[TileID] = possibilities

    def has_collapsed(self) -> bool:
        return len(self._possibilities) == 1

    def is_valid(self) -> bool:
        return len(self._possibilities) > 0

    def remove(self, possibility: TileID) -> None:
        if possibility in self._possibilities:
            self._possibilities.remove(possibility)

    def collapse_to(self, possibility: TileID) -> None:
        self._possibilities = [possibility]

    def get_entropy(self) -> int:
        return len(self._possibilities)


class Grid:
    def __init__(self, grid_size: int, possibilities: list[TileID]) -> None:
        self._tile_superpositions: list[list[TileSuperposition]] = [
            [TileSuperposition(possibilities) for t in range(grid_size)] for t in range(grid_size)
        ]

    def collapse(self) -> None:
        raise NotImplementedError("Haven't implemented wave function collapse yet")


tiles: list[Tile] = [
    Tile(1, ("a", "a", "a", "a")),
    Tile(2, ("c", "a", "b", "c")),
    Tile(3, ("b", "b", "b", "b")),
]

grid = Grid(8, [tile.get_id() for tile in tiles])
