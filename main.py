from gui.view import display_grid, TileAsset
from wfc import basic


def main() -> None:
    tiles: list[basic.Tile] = [
        basic.Tile("grass",      {basic.Direction.LEFT: "g", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("end",        {basic.Direction.LEFT: "r", basic.Direction.UP: "g", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("straight",   {basic.Direction.LEFT: "g", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "g"}),
        basic.Tile("corner",     {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "g"}),
        basic.Tile("t-junction", {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "g", basic.Direction.RIGHT: "r"}),
        basic.Tile("cross",      {basic.Direction.LEFT: "r", basic.Direction.UP: "r", basic.Direction.DOWN: "r", basic.Direction.RIGHT: "r"}),
    ]

    graphics: dict[basic.TileID, TileAsset] = {
        "grass":      TileAsset("graphics/grass-1.png"),
        "end":        TileAsset("graphics/end.png"),
        "straight":   TileAsset("graphics/straight.png"),
        "corner":     TileAsset("graphics/corner.png"),
        "t-junction": TileAsset("graphics/t-junction.png"),
        "cross":      TileAsset("graphics/cross.png"),
    }

    grid_size = 4
    grid = basic.Grid(grid_size, tiles)

    grid.collapse()

    print(grid.pretty_print_grid_state())

    grid_data: list[list[TileAsset]] = [[TileAsset() for _ in range(grid_size)] for _ in range(grid_size)]

    for row_idx, row in enumerate(grid.get_grid()):
        for col_idx, tile in enumerate(row):
            grid_data[row_idx][col_idx] = graphics[tile.get_collapsed_state().get_id()]

    display_grid(grid_size, grid_size, grid_data)


if __name__ == "__main__":
    main()
