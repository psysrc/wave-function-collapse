from gui.view import GUI, TileAsset, Rotation
from wfc import basic
from pathlib import Path


DIR = basic.Direction


def display_wfc_grid(grid: basic.Grid, graphics: dict[basic.TileID, TileAsset]) -> None:
    grid_size = grid.get_grid_size()

    grid_data: list[list[TileAsset]] = [[TileAsset(Path()) for _ in range(grid_size)] for _ in range(grid_size)]

    for row_idx, row in enumerate(grid.get_grid()):
        for col_idx, tile in enumerate(row):
            grid_data[row_idx][col_idx] = graphics[tile.get_collapsed_state().get_id()]

    GUI().display_grid(grid_data)


def main() -> None:
    tiles: list[basic.Tile] = [
        basic.Tile("grass1",        {DIR.LEFT: {"g1", "g2"}, DIR.UP: {"g1", "g2"}, DIR.DOWN: {"g1", "g2"}, DIR.RIGHT: {"g1", "g2"}}),
        basic.Tile("grass2",        {DIR.LEFT: {"g2", "g3"}, DIR.UP: {"g2", "g3"}, DIR.DOWN: {"g2", "g3"}, DIR.RIGHT: {"g2", "g3"}}),
        basic.Tile("grass3",        {DIR.LEFT: {"g3"}, DIR.UP: {"g3"}, DIR.DOWN: {"g3"}, DIR.RIGHT: {"g3"}}),
        basic.Tile("end_r0",        {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"g1"}}),
        basic.Tile("end_r1",        {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"g1"}}),
        basic.Tile("end_r2",        {DIR.LEFT: {"g1"}, DIR.UP: {"g1"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}),
        basic.Tile("end_r3",        {DIR.LEFT: {"g1"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}),
        basic.Tile("straight_r0",   {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}),
        basic.Tile("straight_r1",   {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}),
        basic.Tile("corner_r0",     {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"g1"}}),
        basic.Tile("corner_r1",     {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}),
        basic.Tile("corner_r2",     {DIR.LEFT: {"g1"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}),
        basic.Tile("corner_r3",     {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}),
        basic.Tile("t-junction_r0", {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}),
        basic.Tile("t-junction_r1", {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}),
        basic.Tile("t-junction_r2", {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}),
        basic.Tile("t-junction_r3", {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}),
        basic.Tile("cross",         {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}),
    ]

    weights: list[float] = [
        15,  # grass1
        1,  # grass2
        1,  # grass3
        0.25,  # end_r0
        0.25,  # end_r1
        0.25,  # end_r2
        0.25,  # end_r3
        10,  # straight_r0
        10,  # straight_r1
        0.25,  # corner_r0
        0.25,  # corner_r1
        0.25,  # corner_r2
        0.25,  # corner_r3
        0.25,  # t-junction_r0
        0.25,  # t-junction_r1
        0.25,  # t-junction_r2
        0.25,  # t-junction_r3
        1,     # cross
    ]

    graphics: dict[basic.TileID, TileAsset] = {
        "grass1":        TileAsset(Path("graphics/grass-1.png")),
        "grass2":        TileAsset(Path("graphics/grass-3.png")),
        "grass3":        TileAsset(Path("graphics/grass-4.png")),
        "end_r0":        TileAsset(Path("graphics/end.png")),
        "end_r1":        TileAsset(Path("graphics/end.png"), rotation=Rotation.CLOCKWISE),
        "end_r2":        TileAsset(Path("graphics/end.png"), rotation=Rotation.HALF),
        "end_r3":        TileAsset(Path("graphics/end.png"), rotation=Rotation.ANTICLOCKWISE),
        "straight_r0":   TileAsset(Path("graphics/straight.png")),
        "straight_r1":   TileAsset(Path("graphics/straight.png"), rotation=Rotation.CLOCKWISE),
        "corner_r0":     TileAsset(Path("graphics/corner.png")),
        "corner_r1":     TileAsset(Path("graphics/corner.png"), rotation=Rotation.CLOCKWISE),
        "corner_r2":     TileAsset(Path("graphics/corner.png"), rotation=Rotation.HALF),
        "corner_r3":     TileAsset(Path("graphics/corner.png"), rotation=Rotation.ANTICLOCKWISE),
        "t-junction_r0": TileAsset(Path("graphics/t-junction.png")),
        "t-junction_r1": TileAsset(Path("graphics/t-junction.png"), rotation=Rotation.CLOCKWISE),
        "t-junction_r2": TileAsset(Path("graphics/t-junction.png"), rotation=Rotation.HALF),
        "t-junction_r3": TileAsset(Path("graphics/t-junction.png"), rotation=Rotation.ANTICLOCKWISE),
        "cross":         TileAsset(Path("graphics/cross.png")),
    }

    grid_size = 16
    grid = basic.Grid(grid_size, tiles, weights)

    print("Collapsing grid... ", end="", flush=True)
    grid.collapse()
    print("Done:")

    print(grid.pretty_print_grid_state())

    print("Displaying grid... ", end="", flush=True)
    display_wfc_grid(grid, graphics)
    print("Done.")


if __name__ == "__main__":
    main()
