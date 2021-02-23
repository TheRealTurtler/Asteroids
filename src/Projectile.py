import pygame
from src.SpaceObject import SpaceObject


class Projectile(SpaceObject):
	"""description of class"""

	def __init__(self, pos, velDir, speed=2, size=1):

		super().__init__(pos, velDir, speed, size)

		self.wrap = 0
		self.maxWrap = 1
