import pygame
import math
import random
from SpaceObject import SpaceObject


class Asteroid(SpaceObject):
    """description of class"""

    sizeBig = 60
    sizeMedium = 40
    sizeSmall = 20

    speedMultiplierBig = 1
    speedMultiplierMedium = 1.5
    speedMultiplierSmall = 2

    polygonPointsCount = 20

    scorePointsBig = 20
    scorePointsMedium = 50
    scorePointsSmall = 100

    def __init__(self, pos, vel=pygame.Vector2(0, 0), rotSpeed = 1, size = sizeBig):
        self.scorePoints = 0
        speedMultiplier = 1

        if size == Asteroid.sizeBig:
            self.scorePoints = Asteroid.scorePointsBig
            speedMultiplier = Asteroid.speedMultiplierBig
        elif size == Asteroid.sizeMedium:
            self.scorePoints = Asteroid.scorePointsMedium
            speedMultiplier = Asteroid.speedMultiplierMedium
        elif size == Asteroid.sizeSmall:
            self.scorePoints = Asteroid.scorePointsSmall
            speedMultiplier = Asteroid.speedMultiplierSmall
        else:
            raise LookupError

        super().__init__(pos, vel, speedMultiplier, size)

        self.rot = 0
        self.rotSpeed = rotSpeed
        self.polygonPointsOffsets = [pygame.Vector2(
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.cos((2 * math.pi * x) / Asteroid.polygonPointsCount),
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.sin((2 * math.pi * x) / Asteroid.polygonPointsCount)
        ) for x in range(self.polygonPointsCount)]

        self.polygonPoints = [pygame.Vector2(0, 0) for offset in self.polygonPointsOffsets]

    def update(self):
        super().update()

        self.rot += self.rotSpeed

        # Rotation
        self.rot %= 360

        for (idx, offset) in enumerate(self.polygonPointsOffsets):
            self.polygonPoints[idx] = self.pos + offset.rotate(self.rot)

    def draw(self, screen, color = pygame.Color(255, 255, 255)):
        if type(screen) != pygame.Surface:
            raise TypeError

        if type(color) != pygame.Color:
            raise TypeError

        pygame.draw.polygon(screen, color, self.polygonPoints, 1)
