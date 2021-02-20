import pygame
import random
from SpaceObject import SpaceObject
from Particle import Particle


class Explosion(SpaceObject):

	def __init__(self, pos):

		# Definiert Ursprung der Explosion
		super().__init__(pos)

		self.explosionCreationTime = pygame.time.get_ticks()

		self.particleSize = 1
		self.particleSpeed = 1
		self.particles = []

		for x in range(random.randint(5, 20)):

			particleDir = pygame.Vector2(
				(random.random() - 0.5),		# Zufällige Richtung
				(random.random() - 0.5)
			)

			particleColor = pygame.Color(255, random.randrange(0, 256), 0)

			self.particles.append(
				Particle(pygame.Vector2(pos), particleDir, self.particleSpeed, self.particleSize, particleColor)
			)

	def update(self):
		for p in self.particles:
			p.pos += p.dir * p.speed

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		for p in self.particles:
			p.draw(screen)
