import pygame

from Vector2D import Vector2D

class Projectile:
	"""description of class"""

	def __init__(self, pos = Vector2D(0, 0), vel = Vector2D(0, 0), size = 1) :
		if type(pos) != Vector2D :
			return NotImplemented

		if type(vel) != Vector2D :
			return NotImplemented

		if type(size) not in (int, float) :
			return NotImplemented

		self.pos = pos
		self.vel = vel
		self.size = size
		self.wrap = 0
		self.maxWrap = 1

	def update(self) :
		self.pos += self.vel

	def draw(self, screen, color = pygame.Color(255, 255, 255)) :
		if type(screen) != pygame.Surface :
			return NotImplemented
		
		if type(color) != pygame.Color :
			return NotImplemented

		pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), self.size)
