import pygame

Colour = tuple[int, int, int]

def display_grid(rows: int, columns: int, grid_data: list[list[Colour]]) -> None:
    width = 800
    height = 800
    resolution = (width, height)
    screen = pygame.display.set_mode(resolution)

    max_fps = 5

    cell_height = height / rows
    cell_width = width / columns

    clock = pygame.time.Clock()  # to set max FPS

    screen.fill((0, 0, 0))  # Fill screen with black

    for row in range(rows):
        for column in range(columns):
            color: Colour = grid_data[row][column]

            rect = pygame.Rect(column*cell_width, row*cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, color, rect)

    while True:
        pygame.display.flip()  # Update the screen.
        clock.tick(max_fps)  # max FPS = 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
