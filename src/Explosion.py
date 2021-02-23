import pygame
import random
from src.SpaceObject import SpaceObject
from src.Particle import Particle


class Explosion(SpaceObject):

	def __init__(self, pos):

		# Definiert Ursprung der Explosion
		super().__init__(pos)

		self.particles = []

		for x in range(random.randint(5, 20)):

			particleDir = pygame.Vector2(
				(random.random() - 0.5),		# Zufällige Richtung
				(random.random() - 0.5)
			)

			particleSize = random.randrange(1, 3)		# Zufällige Größe für Partikel
			particleSpeed = random.randrange(1, 4)		# Zufällige Geschwindigkeit für Partikel
			particleColor = pygame.Color(255, random.randrange(0, 256), 0)		# Farbe zwischen rot und gelb

			self.particles.append(
				Particle(pygame.Vector2(pos), particleDir, particleSpeed, particleSize, particleColor)
			)

	def update(self):
		for p in self.particles[:]:
			p.update()

			# Partikel löschen, wenn stehen geblieben
			if p.speed == 0:
				self.particles.remove(p)


	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		for p in self.particles:
			p.draw(screen)
