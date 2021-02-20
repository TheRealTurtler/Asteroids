import pygame
from SpaceObject import SpaceObject


class PowerUp(SpaceObject):
	"""description of class"""

	size = 10
	availablePowerUps = 3
	spawnDelay = 10000

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

		if self.id == 0:		# Feuerrate
			color = pygame.Color(255, 0, 0)
		elif self.id == 1:		# Maximalgeschwindigkeit Spieler
			color = pygame.Color(0, 255, 0)
		elif self.id == 2:		# Projektil-Geschwindigkeit
			color = pygame.Color(0, 0, 255)

		pygame.draw.circle(screen, color, self.pos, self.size, 1)
