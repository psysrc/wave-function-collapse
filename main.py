from gui.view import display_grid, Colour
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

    black = (0, 0, 0)
    red = (150, 0, 0)
    green = (0, 150, 0)
    blue = (0, 0, 150)

    mapping: dict[basic.TileID, Colour] = {
        1: blue,
        2: red,
        3: green,
    }

    grid_data: list[list[Colour]] = [[black for _ in range(grid_size)] for _ in range(grid_size)]

    for row_idx, row in enumerate(grid.get_grid()):
        for col_idx, tile in enumerate(row):
            grid_data[row_idx][col_idx] = mapping[tile.get_collapsed_state().get_id()]

    display_grid(grid_size, grid_size, grid_data)


if __name__ == "__main__":
    main()
