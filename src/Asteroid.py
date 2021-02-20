import pygame
import math
import random
from Spaceobject import Spaceobject


class Asteroid(Spaceobject):
    """description of class"""

    sizeBig = 60
    sizeMedium = 40
    sizeSmall = 20

    speedMultiplierBig = 1
    speedMultiplierMedium = 1.5
    speedMultiplierSmall = 2

    numPoints = 20

    def __init__(self, pos, vel=pygame.Vector2(0, 0), rotSpeed=1, size=sizeBig, speedMultiplier=speedMultiplierBig):
        super().__init__(pos, vel, speedMultiplier, size)
        self.rot = 0
        self.rotSpeed = rotSpeed
        self.pointOffsets = [pygame.Vector2(
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.cos((2 * math.pi * x) / self.numPoints),
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.sin((2 * math.pi * x) / self.numPoints)
        ) for x in range(self.numPoints)]

        self.points = [pygame.Vector2(0,0) for offset in self.pointOffsets]

    def update(self):
        super().update()

        self.rot += self.rotSpeed

        # Rotation
        self.rot %= 360

        for (idx, offset) in enumerate(self.pointOffsets):
            self.points[idx] = self.pos + offset.rotate(self.rot)

    def drawPoly(self, screen, color=pygame.Color(255, 255, 255)):
        if type(screen) != pygame.Surface:
            return NotImplemented

        if type(color) != pygame.Color:
            return NotImplemented

        pygame.draw.polygon(screen, color, self.points, 1)
