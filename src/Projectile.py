import pygame
from SpaceObject import SpaceObject


class Projectile(SpaceObject):
	"""description of class"""

	def __init__(self, pos, direction, speed=2, size=1):

		super().__init__(pos, direction, speed, size)

		self.wrap = 0
		self.maxWrap = 1
