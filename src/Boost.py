import pygame
import random

from src.Particle import Particle


class Boost:
	particleCooldown = 100
	particleSpread = 1

	def __init__(self):
		self.particles = []

		self.timeLastParticle = pygame.time.get_ticks()

	def boost(self, pos, direction):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(direction) != pygame.Vector2:
			raise TypeError

		if pygame.time.get_ticks() - self.timeLastParticle > Boost.particleCooldown:
			self.timeLastParticle = pygame.time.get_ticks()
			for x in range(random.randint(1, 2)):
				particleDir = direction + pygame.Vector2(
					(random.random() - 0.5) * Boost.particleSpread,  # Zufällige Richtung
					(random.random() - 0.5) * Boost.particleSpread
				)

				particleSize = random.randrange(1, 3)  # Zufällige Größe für Partikel
				particleSpeed = random.randrange(1, 3)  # Zufällige Geschwindigkeit für Partikel
				particleColor = pygame.Color(255, random.randrange(0, 256), 0)  # Farbe zwischen rot und gelb

				self.particles.append(Particle(pygame.Vector2(pos), particleDir, particleSpeed, particleSize, particleColor))

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
