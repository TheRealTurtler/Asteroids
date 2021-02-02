import pygame
import math
import random

class Asteroid:
    """description of class"""

    sizeBig = 60
    sizeMedium = 40
    sizeSmall = 20

    speedMultiplierBig = 1
    speedMultiplierMedium = 1.5
    speedMultiplierSmall = 2

    numPoints = 20

    def __init__(self, pos, vel = pygame.Vector2(0, 0), size = sizeBig, speedMultiplier = speedMultiplierBig):
        self.pos = pos
        self.vel = vel * speedMultiplier
        self.size = size
        self.rot = 0

        self.pointOffsets = [pygame.Vector2(
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.cos((2 * math.pi * x) / self.numPoints),
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.sin((2 * math.pi * x) / self.numPoints)
        ) for x in range(self.numPoints)]

        self.points = [pygame.Vector2(0,0) for offset in self.pointOffsets]

    def update(self):
        self.pos += self.vel
        self.points = [pygame.Vector2(self.pos + offset) for offset in self.pointOffsets]

    def draw(self, screen, color=pygame.Color(255, 255, 255)):
        if type(screen) != pygame.Surface:
            return NotImplemented

        if type(color) != pygame.Color:
            return NotImplemented

        pygame.draw.polygon(screen, color, self.points, 1)
