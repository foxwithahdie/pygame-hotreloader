"""
This module holds the class for the visual when a hotreload occurs.


Dependencies:
    - typing: Annotations for types. Optional[Type] == Type | None == Union[Type, None]
    - importlib.resources: Used for getting static files in a subpackage.
    - pygame: Provides important functions, classes and types to create the overrided sprite.


Classes:
    HotReloadVisual(pygame.sprite.Sprite):
        The sprite class overrided to include state for when a hotreload occurs.
        Makes a small visual on the screen to do so.
"""

from importlib.resources import files
from typing import Optional

import pygame


class HotReloadVisual(pygame.sprite.Sprite):
    """
    A custom sprite meant to be a visual for if your game has hotreloaded.

    Inheritance Use:
        pygame.sprite.Sprite.draw(surface: pygame.Surface) -> None:
            Draws a Sprite object to a given surface.

        pygame.sprite.Sprite.update(*args, **kwargs) -> None:
            Updates a Sprite object on a given surface.
            My version takes in a delta_time parameter to account for time
            since the game started running.

    Attributes (Public):
        MAXIMUM_ALPHA_VALUE (class, int): The maximum value alpha can be.
        FADE_DURATION (class, float): The fade duration for a particular refresh.
        ALPHA_THRESHOLD (class, float): The threshold at which an object is considered "gone".

        x (instance, int): The x position of the given sprite.
        y (instance, int): The y position of the given sprite.
        image (instance, pygame.Surface): The image that the sprite holds.
                                          It is a small refresh image in the
                                          resources/images folder.
        rect (instance, pygame.Rect): The bounding rectangle of the image.

    Attributes (Private):
        refresh_occurred (bool): A state attribute for knowing that a refresh has occurred.
        current_alpha (int | float): A state attribute that tracks the sprite's current alpha value.
        starting_time (float): A state attribute for knowing when a refresh has occurred.

    Methods (Instance):
        visual_refresh ((float) -> None): Event method for triggering the visual refresh.

    Methods (Static):
        set_alpha ((pygame.Surface, int) -> None): Sets the alpha value per pixel for a surface.
    """

    MAXIMUM_ALPHA_VALUE: int = 255
    FADE_DURATION: float = 1.5
    ALPHA_THRESHOLD: float = 1.0

    def __init__(self, *groups, screen_hint: Optional[pygame.Surface] = None) -> None:
        """
        Args:
            *groups (pygame.sprite.Group): Any groups that the sprite instance gets added to.
            A parameter from the parent class pygame.sprite.Sprite.
            screen_hint (Optional[pygame.Surface], optional): The surface that it ties itself to.
                                                              Defaults to None.
        """
        super().__init__(*groups)

        self.x: int = 5
        self.y: int = 5
        self._refresh_occurred: bool = False
        self._current_alpha: int | float = -1.0
        self._starting_time: float = 0.0

        if screen_hint is not None:
            self.image: pygame.Surface = pygame.image.load(
                str(
                    files("pygame_hotreloader.resources.images").joinpath("refresh.png")
                )
            ).convert_alpha(screen_hint)
        else:
            self.image: pygame.Surface = pygame.image.load(
                str(
                    files("pygame_hotreloader.resources.images").joinpath("refresh.png")
                )
            ).convert_alpha()

        self.rect: pygame.Rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the object onto a given surface.
        """
        if self._current_alpha > 0:
            surface.blit(self.image, self.rect)

    def update(self, delta_time: float) -> None:
        """Updates the object based on a given delta_time value.
        If a reload has occurred, then an image will be drawn and will slowly fade.

        Args:
            delta_time (float): Time since the beginning of the program.
        """

        if self._refresh_occurred:
            elapsed_time: float = delta_time - self._starting_time
            fade_ratio: float = elapsed_time / HotReloadVisual.FADE_DURATION
            self._current_alpha = max(
                0.0, HotReloadVisual.MAXIMUM_ALPHA_VALUE * (1 - fade_ratio)
            )
            if self._current_alpha <= HotReloadVisual.ALPHA_THRESHOLD:
                self._current_alpha = 0
            else:
                HotReloadVisual.set_alpha(self.image, int(self._current_alpha))
        else:
            return

        if self._current_alpha == 0:
            self._refresh_occurred = False

    # Event Method
    def visual_refresh(self, delta_time: float) -> None:
        """Is run when a refresh has occurred.

        Args:
            delta_time (float): Time since the game has started.
                                The initial starting time is set to this.
        """

        if not self._refresh_occurred:
            self._refresh_occurred = True
            self._current_alpha = HotReloadVisual.MAXIMUM_ALPHA_VALUE
            self._starting_time = delta_time

    @staticmethod
    def set_alpha(image: pygame.Surface, alpha_value: int) -> None:
        """Sets the alpha value for each pixel in an image.

        Args:
            image (pygame.Surface): The image, as a surface.
            alpha_value (int): The alpha value you want to set it to.
        """

        with pygame.PixelArray(image) as image_pixelarray:
            for y in range(image.get_height()):
                for x in range(image.get_width()):
                    pixel_rgba: pygame.Color = image.unmap_rgb(image_pixelarray[x, y])

                    edited_pixel_rgba: pygame.Color = pygame.Color(
                        pixel_rgba.r,
                        pixel_rgba.g,
                        pixel_rgba.b,
                        alpha_value if pixel_rgba.a > 0 else pixel_rgba.a,
                    )

                    image_pixelarray[x, y] = image.map_rgb(edited_pixel_rgba)
