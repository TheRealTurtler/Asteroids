import pygame
import random

from src.SpaceObject import SpaceObject
from src.Particle import Particle


class Explosion(SpaceObject):
	# Partikeleinstellungen
	particleMinSpawnCount = 5
	particleMaxSpawnCount = 20
	particleMaxSize = 3
	particleMaxSpeed = 3

	def __init__(self, pos):
		# Definiert Ursprung der Explosion
		super().__init__(pos)

		self.particles = []

		for x in range(random.randint(Explosion.particleMinSpawnCount, Explosion.particleMaxSpawnCount)):
			# Zufaellige Richtung
			particleDir = pygame.Vector2(
				(random.random() - 0.5),
				(random.random() - 0.5)
			)

			# Zufaellige Groesse fuer Partikel
			particleSize = random.randint(1, Explosion.particleMaxSize)

			# Zufaellige Geschwindigkeit fuer Partikel
			particleSpeed = random.randint(1, Explosion.particleMaxSpeed)

			# Farbe zwischen rot und gelb
			particleColor = pygame.Color(255, random.randint(0, 255), 0)

			# Partikel erzeugen
			self.particles.append(Particle(pygame.Vector2(pos), particleDir, particleSpeed, particleSize, particleColor))

	def update(self):
		for p in self.particles[:]:
			# Partikel aktualisieren
			p.update()

			# Partikel loeschen, wenn stehen geblieben
			if p.speed == 0:
				self.particles.remove(p)


	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		for p in self.particles:
			# Partikel zeichnen
			p.draw(screen)
