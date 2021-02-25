import pygame

from src.SpaceObject import SpaceObject


class Particle(SpaceObject):
    friction = 0.05

    def __init__(self, pos, velDir = pygame.Vector2(0, 0), speed = 0, size = 1, color = pygame.Color(255, 255, 255)):
        super().__init__(pos, velDir, speed, size)

        self.color = color

    def update(self):
        if self.speed < Particle.friction:
            self.speed = 0

        if self.speed > 0:
            self.speed -= Particle.friction

        super().update()

    def draw(self, screen):
        if type(screen) != pygame.Surface:
            raise TypeError

        pygame.draw.circle(screen, self.color, self.pos, self.size)
