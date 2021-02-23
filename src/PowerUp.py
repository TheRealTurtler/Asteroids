import pygame

from src.SpaceObject import SpaceObject
from src.Color import Color


class PowerUp(SpaceObject):
	"""description of class"""

	size = 10
	availablePowerUps = 4
	spawnDelay = 10000

	class PowerUpIDs:
		fireRate = 0
		maxSpeed = 1
		projectileSpeed = 2
		multiShot = 3

	def __init__(self, pos, id):
		if type(id) == int:
			self.id = id
		else:
			raise TypeError

		self.collectionTime = 0
		self.duration = 10000

		super().__init__(pos, pygame.Vector2(0, 0), 0, self.size)

	def update(self):
		pass

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		color = pygame.Color(255, 255, 255)

		if self.id == PowerUp.PowerUpIDs.fireRate:					# Feuerrate
			color = Color.RED
		elif self.id == PowerUp.PowerUpIDs.maxSpeed:				# Maximalgeschwindigkeit Spieler
			color = Color.GREEN
		elif self.id == PowerUp.PowerUpIDs.projectileSpeed:		# Projektil-Geschwindigkeit
			color = Color.BLUE
		elif self.id == PowerUp.PowerUpIDs.multiShot:				# Multi-Schuss
			color = Color.ORANGE
		else:
			raise LookupError

		pygame.draw.circle(screen, color, self.pos, self.size)
