from gui.view import display_grid, Colour
from wfc import basic


def main() -> None:
    tiles: list[basic.Tile] = [
        basic.Tile(1, {basic.Direction.LEFT: "a", basic.Direction.UP: "a", basic.Direction.DOWN: "a", basic.Direction.RIGHT: "a"}),
        basic.Tile(2, {basic.Direction.LEFT: "c", basic.Direction.UP: "a", basic.Direction.DOWN: "b", basic.Direction.RIGHT: "c"}),
        basic.Tile(3, {basic.Direction.LEFT: "b", basic.Direction.UP: "b", basic.Direction.DOWN: "b", basic.Direction.RIGHT: "b"}),
    ]

    grid = basic.Grid(4, tiles)

    grid.collapse()

    print(grid.pretty_print_grid_state())

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    grid_data: list[list[Colour]] = [
        [red, green, blue],
        [blue, green, red],
    ]
    display_grid(2, 3, grid_data)


if __name__ == "__main__":
    main()
