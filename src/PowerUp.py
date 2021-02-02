import pygame


class PowerUp:
    """description of class"""

    size = 10

    def __init__(self, pos, effect):
        self.pos = pos

        if type(effect) == str:
            self.effect = effect
        else:
            raise TypeError

    def draw(self, screen, color=pygame.Color(0, 255, 0)):
        if type(screen) != pygame.Surface:
            return NotImplemented

        if type(color) != pygame.Color:
            return NotImplemented

        pygame.draw.circle(screen, color, self.pos, self.size, 1)
