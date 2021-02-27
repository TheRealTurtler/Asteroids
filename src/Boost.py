import pygame
import random

from src.Particle import Particle


class Boost:
	# Partikeleinstellungen
	particleCooldown = 100
	particleSpread = 1

	particleMaxSpawnCount = 2
	particleMaxSize = 2
	particleMaxSpeed = 2

	def __init__(self):
		self.particles = []

		self.timeLastParticle = pygame.time.get_ticks()

	def boost(self, pos, direction):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(direction) != pygame.Vector2:
			raise TypeError

		# Neue Partikel, wenn particleCooldown vergangen
		if pygame.time.get_ticks() - self.timeLastParticle > Boost.particleCooldown:
			self.timeLastParticle = pygame.time.get_ticks()

			# Zufaellige Anzahl an Partikel spawnen
			for x in range(random.randint(1, Boost.particleMaxSpawnCount)):
				# Zufaellige Richtung
				particleDir = direction + pygame.Vector2(
					(random.random() - 0.5) * Boost.particleSpread,
					(random.random() - 0.5) * Boost.particleSpread
				)

				# Zufaellige Groesse fuer Partikel
				particleSize = random.randint(1, Boost.particleMaxSize)

				# Zufaellige Geschwindigkeit fuer Partikel
				particleSpeed = random.randint(1, Boost.particleMaxSpeed)

				# Zufaelige Farbe zwischen rot und gelb
				particleColor = pygame.Color(255, random.randint(0, 255), 0)

				# Partikel erzeugen
				self.particles.append(Particle(pygame.Vector2(pos), particleDir, particleSpeed, particleSize, particleColor))

	def update(self):
		for p in self.particles[:]:
			# Partikel aktualisieren
			p.update()

			# Partikel loeschen, wenn stehen geblieben
			if p.speed == 0:		# Partikel setzt speed = 0, also ist float comparison Ok
				self.particles.remove(p)

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Partikel zeichnen
		for p in self.particles:
			p.draw(screen)
