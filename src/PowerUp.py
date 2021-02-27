import pygame

from src.SpaceObject import SpaceObject
from src.Color import Color


class PowerUp(SpaceObject):
	# PowerUp-Einstellungen
	size = 10
	availablePowerUps = 4
	spawnDelay = 10000		# Einheit: ms

	class PowerUpIDs:
		fireRate = 0
		maxSpeed = 1
		projectileSpeed = 2
		multiShot = 3

	def __init__(self, pos, powerUpID):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(powerUpID) != int:
			raise TypeError

		self.id = powerUpID

		self.collectionTime = 0
		self.duration = 10000

		# Farbe festlegen
		if self.id == PowerUp.PowerUpIDs.fireRate:				# Feuerrate
			self.color = Color.RED
		elif self.id == PowerUp.PowerUpIDs.maxSpeed:			# Maximalgeschwindigkeit Spieler
			self.color = Color.GREEN
		elif self.id == PowerUp.PowerUpIDs.projectileSpeed:		# Projektil-Geschwindigkeit
			self.color = Color.BLUE
		elif self.id == PowerUp.PowerUpIDs.multiShot:			# Multi-Schuss
			self.color = Color.ORANGE
		else:
			raise LookupError

		# SpaceObject initialisieren
		super().__init__(pos, pygame.Vector2(0, 0), 0, self.size)

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# PowerUp zeichnen
		pygame.draw.circle(screen, self.color, self.pos, self.size)
