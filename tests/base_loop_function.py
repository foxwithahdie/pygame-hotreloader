"""
Base loop.
"""

import pygame


def game_loop(
    screen: pygame.Surface, time_since_start: float, delta_time: float
) -> bool:
    """
    Main game loop function.
    """
    # Events - Controller
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    # State updating - Model

    # Drawing - View
    screen.fill((0, 0, 0))
    screen.fill((255, 255, 255))

    return True


def main() -> None:
    """
    Main function.
    """

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((800, 600))

    running: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()

    while running:
        time_since_start: float = pygame.time.get_ticks() / 1000.0
        delta_time: float = clock.tick(60)
        running = game_loop(screen, time_since_start, delta_time)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
