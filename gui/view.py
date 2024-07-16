import pygame
from pathlib import Path
from enum import IntEnum


class Rotation(IntEnum):
    NONE = 0
    ANTICLOCKWISE = 90
    HALF = 180
    CLOCKWISE = 270


class TileAsset:
    def __init__(self, image_path: Path, rotation: Rotation = Rotation.NONE) -> None:
        self._filepath = image_path
        self._rotation = rotation

    def get_image_path(self) -> Path:
        return self._filepath

    def get_rotation(self) -> Rotation:
        return self._rotation


class GUI:
    def __init__(self) -> None:
        self._screen_width = 800
        self._screen_height = 800
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))

        self._max_fps = 5

        self._clock = pygame.time.Clock()

    def display_grid(self, grid_data: list[list[TileAsset]]) -> None:
        """Displays the grid data and waits for the user to press a button."""

        black = (0, 0, 0)
        self._screen.fill(black)

        rows = len(grid_data)
        columns = len(grid_data[0])

        cell_height = self._screen_height / rows
        cell_width = self._screen_width / columns

        all_tile_assets: set[TileAsset] = set()
        for g in grid_data:
            for gg in g:
                all_tile_assets.add(gg)

        loaded_tile_assets: dict[TileAsset, pygame.Surface] = {
            asset: pygame.image.load(asset.get_image_path()) for asset in all_tile_assets
        }

        for row in range(rows):
            for column in range(columns):
                asset = grid_data[row][column]
                image = loaded_tile_assets[asset]
                image = pygame.transform.rotate(image, asset.get_rotation())
                image = pygame.transform.scale(image, (cell_width, cell_height))

                rect = pygame.Rect(column*cell_width, row*cell_height, cell_width, cell_height)
                self._screen.blit(image, rect)

        while True:
            pygame.display.flip()  # Update the screen.
            self._clock.tick(self._max_fps)  # max FPS = 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
