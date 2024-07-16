import random
from gui.view import GUI, UserAction, TileAsset, Rotation
from wfc import basic
from pathlib import Path


DIR = basic.Direction


def grid_data_to_display_data(
    grid: basic.Grid, graphics_map: dict[basic.TileID, TileAsset], superposition_graphic: TileAsset, invalid_graphic: TileAsset
) -> list[list[TileAsset]]:
    grid_size = grid.get_grid_size()

    grid_data: list[list[TileAsset]] = [[TileAsset(Path()) for _ in range(grid_size)] for _ in range(grid_size)]

    for row_idx, row in enumerate(grid.get_grid()):
        for col_idx, tile_superposition in enumerate(row):
            if tile_superposition.superposition == basic.Superposition.INVALID:
                grid_data[row_idx][col_idx] = invalid_graphic

            elif tile_superposition.superposition == basic.Superposition.COLLAPSED:
                assert tile_superposition.tile is not None

                grid_data[row_idx][col_idx] = graphics_map[tile_superposition.tile.id]

            elif tile_superposition.superposition == basic.Superposition.SUPERPOSITION:
                grid_data[row_idx][col_idx] = superposition_graphic

            else:
                raise RuntimeError(f"Unknown tile superposition: {tile_superposition.superposition}")

    return grid_data


def main() -> None:
    tiles: list[basic.TileDefinition] = [
        basic.TileDefinition("grass1", {DIR.LEFT: {"g1", "g2"}, DIR.UP: {"g1", "g2"}, DIR.DOWN: {"g1", "g2"}, DIR.RIGHT: {"g1", "g2"}}, prob_weight=15),
        basic.TileDefinition("grass2", {DIR.LEFT: {"g2", "g3"}, DIR.UP: {"g2", "g3"}, DIR.DOWN: {"g2", "g3"}, DIR.RIGHT: {"g2", "g3"}}, prob_weight=5),
        basic.TileDefinition("grass3", {DIR.LEFT: {"g3"}, DIR.UP: {"g3"}, DIR.DOWN: {"g3"}, DIR.RIGHT: {"g3"}}, prob_weight=5),
        basic.TileDefinition("end_r0", {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"g1"}}, prob_weight=0.25),
        basic.TileDefinition("end_r1", {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"g1"}}, prob_weight=0.25),
        basic.TileDefinition("end_r2", {DIR.LEFT: {"g1"}, DIR.UP: {"g1"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}, prob_weight=0.25),
        basic.TileDefinition("end_r3", {DIR.LEFT: {"g1"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}, prob_weight=0.25),
        basic.TileDefinition("straight_r0", {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}, prob_weight=10),
        basic.TileDefinition("straight_r1", {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}, prob_weight=10),
        basic.TileDefinition("corner_r0", {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"g1"}}, prob_weight=0.25),
        basic.TileDefinition("corner_r1", {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}, prob_weight=0.25),
        basic.TileDefinition("corner_r2", {DIR.LEFT: {"g1"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}, prob_weight=0.25),
        basic.TileDefinition("corner_r3", {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}, prob_weight=0.25),
        basic.TileDefinition("t-junction_r0", {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"g1"}, DIR.RIGHT: {"r"}}, prob_weight=0.25),
        basic.TileDefinition("t-junction_r1", {DIR.LEFT: {"g1"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}, prob_weight=0.25),
        basic.TileDefinition("t-junction_r2", {DIR.LEFT: {"r"}, DIR.UP: {"g1"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}, prob_weight=0.25),
        basic.TileDefinition("t-junction_r3", {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"g1"}}, prob_weight=0.25),
        basic.TileDefinition("cross", {DIR.LEFT: {"r"}, DIR.UP: {"r"}, DIR.DOWN: {"r"}, DIR.RIGHT: {"r"}}, prob_weight=1),
    ]

    graphics: dict[basic.TileID, TileAsset] = {
        "grass1": TileAsset(Path("graphics/grass-1.png")),
        "grass2": TileAsset(Path("graphics/grass-3.png")),
        "grass3": TileAsset(Path("graphics/grass-4.png")),
        "end_r0": TileAsset(Path("graphics/end.png")),
        "end_r1": TileAsset(Path("graphics/end.png"), rotation=Rotation.CLOCKWISE),
        "end_r2": TileAsset(Path("graphics/end.png"), rotation=Rotation.HALF),
        "end_r3": TileAsset(Path("graphics/end.png"), rotation=Rotation.ANTICLOCKWISE),
        "straight_r0": TileAsset(Path("graphics/straight.png")),
        "straight_r1": TileAsset(Path("graphics/straight.png"), rotation=Rotation.CLOCKWISE),
        "corner_r0": TileAsset(Path("graphics/corner.png")),
        "corner_r1": TileAsset(Path("graphics/corner.png"), rotation=Rotation.CLOCKWISE),
        "corner_r2": TileAsset(Path("graphics/corner.png"), rotation=Rotation.HALF),
        "corner_r3": TileAsset(Path("graphics/corner.png"), rotation=Rotation.ANTICLOCKWISE),
        "t-junction_r0": TileAsset(Path("graphics/t-junction.png")),
        "t-junction_r1": TileAsset(Path("graphics/t-junction.png"), rotation=Rotation.CLOCKWISE),
        "t-junction_r2": TileAsset(Path("graphics/t-junction.png"), rotation=Rotation.HALF),
        "t-junction_r3": TileAsset(Path("graphics/t-junction.png"), rotation=Rotation.ANTICLOCKWISE),
        "cross": TileAsset(Path("graphics/cross.png")),
    }

    superposition_graphic = TileAsset(Path("graphics/unknown.png"))
    invalid_graphic = TileAsset(Path("graphics/invalid.png"))

    (screen_width, screen_height) = (800, 800)
    gui = GUI(screen_width, screen_height)

    grid_size = 32
    grid = basic.Grid(grid_size, tiles)

    collapse_slowly = False

    random.seed()
    seed = random.randrange(1, 2**32)
    print(f"Using seed '{seed}'")
    random.seed(seed)

    while True:
        events = gui.handle_events()

        for event, event_data in events:
            if event == UserAction.QUIT:
                return

            elif event == UserAction.COLLAPSE_ALL_IMMEDIATELY:
                grid.collapse()

            elif event == UserAction.COLLAPSE_ONE:
                tile_coordinate = grid.find_lowest_entropy_tile_superposition()
                if tile_coordinate is not None:
                    grid.collapse_tile_superposition(tile_coordinate)

            elif event == UserAction.COLLAPSE_ALL_SLOWLY:
                collapse_slowly = not collapse_slowly

            elif event == UserAction.COLLAPSE_SPECIFIC:
                event_data: tuple[int, int]
                (click_x, click_y) = event_data

                column = int((click_x / screen_width) * grid_size)
                row = int((click_y / screen_height) * grid_size)

                grid.collapse_tile_superposition((row, column))

        if collapse_slowly:
            tile_coordinate = grid.find_lowest_entropy_tile_superposition()
            if tile_coordinate is not None:
                grid.collapse_tile_superposition(tile_coordinate)

        display_data = grid_data_to_display_data(grid, graphics, superposition_graphic, invalid_graphic)
        gui.display_grid(display_data)


if __name__ == "__main__":
    main()
