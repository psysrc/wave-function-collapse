import pygame

def display() -> None:
    resolution = (800, 800)
    screen = pygame.display.set_mode(resolution)

    height = 8
    width = 8
    block_size = 100

    clock = pygame.time.Clock()  # to set max FPS

    screen.fill((0, 0, 0))  # Fill screen with black color.

    for y in range(height):
        for x in range(width):
            color = (x*25, y*25, 0)

            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(screen, color, rect)

    while True:
        pygame.display.flip()  # Update the screen.
        clock.tick(10)  # max FPS = 10

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
