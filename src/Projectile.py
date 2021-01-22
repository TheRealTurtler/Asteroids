import pygame


# from Vector2D import *

class Projectile:
	"""description of class"""

	def __init__(self, pos, dir, speed = 2, size = 1):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(dir) != pygame.Vector2:
			raise TypeError

		if type(size) not in (int, float):
			raise TypeError

		self.pos = pos
		self.dir = dir.normalize() if dir != pygame.Vector2(0, 0) else pygame.Vector2(0, 0)
		self.speed = speed
		self.size = size
		self.wrap = 0
		self.maxWrap = 1

	def update(self):
		self.pos += self.dir * self.speed

	def draw(self, screen, color = pygame.Color(255, 255, 255)):
		if type(screen) != pygame.Surface:
			raise TypeError

		if type(color) != pygame.Color:
			raise TypeError

		pygame.draw.circle(screen, color, self.pos, self.size)
