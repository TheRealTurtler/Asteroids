import pygame
from Spaceobject import Spaceobject


class PowerUp(Spaceobject):
    """description of class"""

    size = 10

    def __init__(self, pos, effect):
        super().__init__(pos, pygame.Vector2(0, 0), 0, self.size)
        if type(effect) == str:
            self.effect = effect
        else:
            raise TypeError
