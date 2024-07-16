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
        basic.Tile("grass",      {basic.Direction.LEFT: "g", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("end",        {basic.Direction.LEFT: "r", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("straight",   {basic.Direction.LEFT: "g", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "g"}),
        basic.Tile("straight_r", {basic.Direction.LEFT: "r", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "r"}),
        basic.Tile("corner",     {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("t-junction", {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "r"}),
        basic.Tile("cross",      {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "r"}),
    ]

    graphics: dict[basic.TileID, TileAsset] = {
        "grass":       TileAsset(Path("graphics/grass-1.png")),
        "end":         TileAsset(Path("graphics/end.png")),
        "straight":    TileAsset(Path("graphics/straight.png")),
        "straight_r":  TileAsset(Path("graphics/straight.png"), rotation=Rotation.CLOCKWISE),
        "corner":      TileAsset(Path("graphics/corner.png")),
        "t-junction":  TileAsset(Path("graphics/t-junction.png")),
        "cross":       TileAsset(Path("graphics/cross.png")),
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
