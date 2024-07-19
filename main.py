import argparse
import random
from graphics_loaders.yaml import YamlGraphicsLoader
from gui.view import GUI, UserAction, TileAsset, Rotation
from helpers.rotation import AllRotations
from wfc import basic
from pathlib import Path
from wfc.basic_socket import BasicSocket, SocketType
from rule_loaders.yaml import YamlRulesLoader


DIR = basic.Direction


def grid_data_to_display_data(
    grid: basic.Grid, tile_graphics: dict[basic.TileID, Path], superposition_graphic: TileAsset, invalid_graphic: TileAsset
) -> list[list[TileAsset]]:
    grid_size = grid.get_grid_size()

    grid_data: list[list[TileAsset]] = [[TileAsset(Path()) for _ in range(grid_size)] for _ in range(grid_size)]

    for row_idx, row in enumerate(grid.get_grid()):
        for col_idx, tile_superposition in enumerate(row):
            if tile_superposition.superposition == basic.Superposition.INVALID:
                grid_data[row_idx][col_idx] = invalid_graphic

            elif tile_superposition.superposition == basic.Superposition.COLLAPSED:
                assert tile_superposition.tile is not None

                asset_path = tile_graphics[tile_superposition.tile.id]
                grid_data[row_idx][col_idx] = TileAsset(asset_path, rotation=tile_superposition.tile.rotation)

            elif tile_superposition.superposition == basic.Superposition.SUPERPOSITION:
                grid_data[row_idx][col_idx] = superposition_graphic

            else:
                raise RuntimeError(f"Unknown tile superposition: {tile_superposition.superposition}")

    return grid_data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rules", required=True)
    parser.add_argument("-g", "--graphics", required=True)

    args = parser.parse_args()

    random.seed()
    seed = random.randrange(1, 2**32)
    print(f"Using seed '{seed}'")
    random.seed(seed)

    tile_definitions = YamlRulesLoader(Path(args.rules)).load()

    grid_size = 32
    grid = basic.Grid(grid_size, tile_definitions)

    tile_graphics = YamlGraphicsLoader(Path(args.graphics)).load()

    superposition_graphic = TileAsset(Path("graphics/unknown.png"))
    invalid_graphic = TileAsset(Path("graphics/invalid.png"))

    (screen_width, screen_height) = (800, 800)
    gui = GUI(screen_width, screen_height)

    collapse_slowly = False

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

        display_data = grid_data_to_display_data(grid, tile_graphics, superposition_graphic, invalid_graphic)
        gui.display_grid(display_data)


if __name__ == "__main__":
    main()
