import pygame
from pathlib import Path

TileAsset = Path

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
        asset: pygame.image.load(asset) for asset in all_tile_assets
    }

    for row in range(rows):
        for column in range(columns):
            image_path = grid_data[row][column]
            image = loaded_tile_assets[image_path]
            rect = pygame.Rect(column*cell_width, row*cell_height, cell_width, cell_height)
            image = pygame.transform.scale(image, (cell_width, cell_height))

            screen.blit(image, rect)

    while True:
        pygame.display.flip()  # Update the screen.
        clock.tick(max_fps)  # max FPS = 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
