import pygame
import math
import random

from src.SpaceObject import SpaceObject
from src.Color import Color


class Asteroid(SpaceObject):
    # Asteroidgroessen
    sizeBig = 60
    sizeMedium = 40
    sizeSmall = 20

    # Geschwindigkeitsmultiplokator
    speedMultiplierBig = 1
    speedMultiplierMedium = 1.5
    speedMultiplierSmall = 2

    # Asteroidenaufloesung
    polygonPointsCount = 20

    # Punkte pro zerstoerten Asteroid
    scorePointsBig = 20
    scorePointsMedium = 50
    scorePointsSmall = 100

    # Maximale Rotationsgeschwindigkeit [Grad pro Sekunde]
    maxRotSpeed = 2

    # Maximalgeschwindigkeit
    maxSpeed = 2

    def __init__(self, pos, vel=pygame.Vector2(0, 0), rotSpeed = 1, size = sizeBig):
        # Eigenschaften anhand von Groesse setzen
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

        # SpaceObject initialisieren
        super().__init__(pos, vel, speedMultiplier, size)

        self.rot = 0
        self.rotSpeed = rotSpeed

        # Polygonpunkte relativ zur Asteroidenposition (Mitte)
        self.polygonPointOffsets = [pygame.Vector2(
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.cos((2 * math.pi * x) / Asteroid.polygonPointsCount),
            (self.size + self.size * random.uniform(-0.2, 0.2)) * math.sin((2 * math.pi * x) / Asteroid.polygonPointsCount)
        ) for x in range(self.polygonPointsCount)]

        # Polygonpunkte absolut
        self.polygonPoints = [pygame.Vector2(0, 0) + offset for offset in self.polygonPointOffsets]

    def update(self):
        # Update SpaceObject
        super().update()

        # Rotation
        self.rot += self.rotSpeed
        self.rot %= 360

        # Position der Polygonpunkte neu berechnen
        for (idx, offset) in enumerate(self.polygonPointOffsets):
            self.polygonPoints[idx] = self.pos + offset.rotate(self.rot)

    def draw(self, screen, color = Color.WHITE):
        if type(screen) != pygame.Surface:
            raise TypeError

        if type(color) != pygame.Color:
            raise TypeError

        # Asteroid zeichnen
        pygame.draw.polygon(screen, color, self.polygonPoints, 1)
