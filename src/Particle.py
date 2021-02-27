import pygame

from src.SpaceObject import SpaceObject
from src.Color import Color


# Partikel so zu berechnen ist eigentlich viel zu rechenaufwendig, aber fuer einen Anfaengerkurs gut genug :)
class Particle(SpaceObject):
    # Reibung
    friction = 0.05

    def __init__(self, pos, velDir = pygame.Vector2(0, 0), speed = 0, size = 1, color = Color.WHITE):
        # SpaceObject initialisieren
        super().__init__(pos, velDir, speed, size)

        self.color = color

    def update(self):
        # Geschwindigkeit = 0, wenn derzeitige Geschwindigkeit kleiner ist als Reibung
        # ansonsten wird Richtung geaendert
        if self.speed < Particle.friction:
            self.speed = 0

        # Reibung von Geschwindigkeit abziehen
        if self.speed > 0:
            self.speed -= Particle.friction

        # SpaceObject aktualisieren
        super().update()

    def draw(self, screen):
        if type(screen) != pygame.Surface:
            raise TypeError

        # Partikel zeichnen
        pygame.draw.circle(screen, self.color, self.pos, self.size)
