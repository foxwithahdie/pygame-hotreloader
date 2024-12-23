"""
Base loop.
"""

import pygame


def main() -> None:
    """
    Main function.
    """

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((800, 600))

    running: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()

    while running:
        delta_time = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        screen.fill((255, 255, 255))

        clock.tick(60)  # time per frame may be used for time per frame calculations
        # second setup may be necessary
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
