import pygame
from pathlib import Path
from enum import IntEnum


class Rotation(IntEnum):
    NONE = 0
    CLOCKWISE = 90
    HALF = 180
    ANTICLOCKWISE = 270


class TileAsset:
    def __init__(self, image_path: Path, rotation: Rotation = Rotation.NONE) -> None:
        self._filepath = image_path
        self._rotation = rotation

    def get_image_path(self) -> Path:
        return self._filepath

    def get_rotation(self) -> Rotation:
        return self._rotation


def display_grid(rows: int, columns: int, grid_data: list[list[TileAsset]]) -> None:
    width = 800
    height = 800
    resolution = (width, height)
    screen = pygame.display.set_mode(resolution)

    max_fps = 1

    cell_height = height / rows
    cell_width = width / columns

    clock = pygame.time.Clock()  # to set max FPS

    screen.fill((0, 0, 0))  # Fill screen with black

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
            screen.blit(image, rect)

    while True:
        pygame.display.flip()  # Update the screen.
        clock.tick(max_fps)  # max FPS = 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
