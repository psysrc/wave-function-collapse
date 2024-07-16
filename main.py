from gui.view import display_grid, TileAsset
from wfc import basic


def main() -> None:
    tiles: list[basic.Tile] = [
        basic.Tile(1, {basic.Direction.LEFT: "a", basic.Direction.UP: "a", basic.Direction.DOWN: "a", basic.Direction.RIGHT: "a"}),
        basic.Tile(2, {basic.Direction.LEFT: "c", basic.Direction.UP: "a", basic.Direction.DOWN: "b", basic.Direction.RIGHT: "c"}),
        basic.Tile(3, {basic.Direction.LEFT: "b", basic.Direction.UP: "b", basic.Direction.DOWN: "b", basic.Direction.RIGHT: "b"}),
    ]

    grid_size = 4
    grid = basic.Grid(grid_size, tiles)

    grid.collapse()

    print(grid.pretty_print_grid_state())

    mapping: dict[basic.TileID, TileAsset] = {
        1: TileAsset("/home/samuel/Desktop/My_Files/Projects/Pixel Art/Mage Arena/air.png"),
        2: TileAsset("/home/samuel/Desktop/My_Files/Projects/Pixel Art/Mage Arena/water.png"),
        3: TileAsset("/home/samuel/Desktop/My_Files/Projects/Pixel Art/Mage Arena/earth.png"),
    }

    grid_data: list[list[TileAsset]] = [[TileAsset() for _ in range(grid_size)] for _ in range(grid_size)]

    for row_idx, row in enumerate(grid.get_grid()):
        for col_idx, tile in enumerate(row):
            grid_data[row_idx][col_idx] = mapping[tile.get_collapsed_state().get_id()]

    display_grid(grid_size, grid_size, grid_data)


if __name__ == "__main__":
    main()
