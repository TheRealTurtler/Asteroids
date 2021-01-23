import pygame


class Asteroid:
    """description of class"""

    sizeBig = 60
    sizeMedium = 40
    sizeSmall = 20

    speedMultiplierBig = 1
    speedMultiplierMedium = 1.5
    speedMultiplierSmall = 2

    def __init__(self, pos, vel = pygame.Vector2(0, 0), size = sizeBig, speedMultiplier = speedMultiplierBig):
        self.pos = pos
        self.vel = vel * speedMultiplier
        self.size = size
        self.rot = 0

    def update(self):
        self.pos += self.vel

    def draw(self, screen, color=pygame.Color(255, 255, 255)):
        if type(screen) != pygame.Surface:
            return NotImplemented

        if type(color) != pygame.Color:
            return NotImplemented

        pygame.draw.circle(screen, color, self.pos, self.size, 1)
