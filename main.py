import pygame


def main() -> None:
    resolution = (800, 800)
    screen = pygame.display.set_mode(resolution)

    height = 8
    width = 8
    block_size = 100

    clock = pygame.time.Clock()  # to set max FPS

    screen.fill((0, 0, 0))  # Fill screen with black color.

    for y in range(height):
        for x in range(width):
            color = (x*25, y*25, 2*x*y)  # (R, G, B)

            rect = pygame.Rect(x*block_size, y*block_size, block_size, block_size)
            pygame.draw.rect(screen, color, rect)

    while True:
        clock.tick(60)  # max FPS = 60
        pygame.display.flip()  # Update the screen.

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()



if __name__ == "__main__":
    main()
