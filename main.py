from gui.view import display_grid, TileAsset, Rotation
from wfc import basic
from pathlib import Path


def display_wfc_grid(grid: basic.Grid, graphics: dict[basic.TileID, TileAsset]) -> None:
    grid_size = grid.get_grid_size()

    grid_data: list[list[TileAsset]] = [[TileAsset(Path()) for _ in range(grid_size)] for _ in range(grid_size)]

    for row_idx, row in enumerate(grid.get_grid()):
        for col_idx, tile in enumerate(row):
            grid_data[row_idx][col_idx] = graphics[tile.get_collapsed_state().get_id()]

    display_grid(grid_size, grid_size, grid_data)


def main() -> None:
    tiles: list[basic.Tile] = [
        basic.Tile("grass",         {basic.Direction.LEFT: "g", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("end_r0",        {basic.Direction.LEFT: "r", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("end_r1",        {basic.Direction.LEFT: "g", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("end_r2",        {basic.Direction.LEFT: "g", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "r"}),
        basic.Tile("end_r3",        {basic.Direction.LEFT: "g", basic.Direction.UP: "g", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "g"}),
        basic.Tile("straight_r0",   {basic.Direction.LEFT: "g", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "g"}),
        basic.Tile("straight_r1",   {basic.Direction.LEFT: "r", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "r"}),
        basic.Tile("corner_r0",     {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("corner_r1",     {basic.Direction.LEFT: "g", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "r"}),
        basic.Tile("corner_r2",     {basic.Direction.LEFT: "g", basic.Direction.UP: "g", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "r"}),
        basic.Tile("corner_r3",     {basic.Direction.LEFT: "r", basic.Direction.UP: "g", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "g"}),
        basic.Tile("t-junction_r0", {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "r"}),
        basic.Tile("t-junction_r1", {basic.Direction.LEFT: "g", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "r"}),
        basic.Tile("t-junction_r2", {basic.Direction.LEFT: "r", basic.Direction.UP: "g", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "r"}),
        basic.Tile("t-junction_r3", {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "g"}),
        basic.Tile("cross",         {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "r"}),
    ]

    graphics: dict[basic.TileID, TileAsset] = {
        "grass":         TileAsset(Path("graphics/grass-1.png")),
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
    grid = basic.Grid(grid_size, tiles)

    print("Collapsing grid... ", end="", flush=True)
    grid.collapse()
    print("Done:")

    print(grid.pretty_print_grid_state())

    print("Displaying grid... ", end="", flush=True)
    display_wfc_grid(grid, graphics)
    print("Done.")


if __name__ == "__main__":
    main()
