from typing import Any
import pygame
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from helpers.rotation import Rotation


@dataclass(frozen=True)
class TileAsset:
    image_path: Path
    rotation: Rotation = Rotation.NONE


class UserAction(Enum):
    NONE = 0
    QUIT = 1
    COLLAPSE_ONE = 2
    COLLAPSE_ALL_SLOWLY = 3
    COLLAPSE_ALL_IMMEDIATELY = 4
    COLLAPSE_SPECIFIC = 5


class GUI:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))

        self._max_fps = 60
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
            asset: pygame.image.load(asset.image_path) for asset in all_tile_assets
        }

        for row in range(rows):
            for column in range(columns):
                asset = grid_data[row][column]
                image = loaded_tile_assets[asset]
                image = pygame.transform.rotate(image, asset.rotation)
                image = pygame.transform.scale(image, (cell_width, cell_height))

                rect = pygame.Rect(column * cell_width, row * cell_height, cell_width, cell_height)
                self._screen.blit(image, rect)

        pygame.display.flip()

    def handle_events(self) -> list[tuple[UserAction, Any]]:
        """
        Handle GUI events from the user.

        Returns a list of tuples where each tuple contains an action/event, plus any associated data.
        """

        events: list[tuple[UserAction, Any]] = []

        self._clock.tick(self._max_fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                events.append((UserAction.QUIT, None))
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    events.append((UserAction.COLLAPSE_ONE, None))

                if event.key == pygame.K_g:
                    events.append((UserAction.COLLAPSE_ALL_SLOWLY, None))

                if event.key == pygame.K_RETURN:
                    events.append((UserAction.COLLAPSE_ALL_IMMEDIATELY, None))

            if event.type == pygame.MOUSEBUTTONUP:
                (width, height) = pygame.mouse.get_pos()
                events.append((UserAction.COLLAPSE_SPECIFIC, (width, height)))

        return events
