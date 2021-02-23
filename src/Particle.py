import pygame

from src.SpaceObject import SpaceObject


class Particle(SpaceObject):
    def __init__(self, pos, velDir = pygame.Vector2(0, 0), speed = 0, size = 1, color = pygame.Color(255, 255, 255)):
        super().__init__(pos, velDir, speed, size)

        self.color = color

        self.friction = 0.05

    def update(self):
        if self.speed < self.friction:
            self.speed = 0

        if self.speed > 0:
            self.speed -= self.friction

        super().update()

    def draw(self, screen):
        if type(screen) != pygame.Surface:
            raise TypeError

        pygame.draw.circle(screen, self.color, self.pos, self.size)
