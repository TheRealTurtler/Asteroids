import pygame
import random

from SpaceObject import SpaceObject


class Particle(SpaceObject):
    def __init__(self, pos, direction = pygame.Vector2(0, 0), speed = 0, size = 1, color = pygame.Color(255, 255, 255)):
        super().__init__(pos, direction, speed, size)

        self.color = color

        self.particleCreationTime = pygame.time.get_ticks()

    def draw(self, screen):
        if type(screen) != pygame.Surface:
            raise TypeError

        pygame.draw.circle(screen, self.color, self.pos, self.size, 1)
