import pygame

#from Vector2D import *

class Projectile:
	"""description of class"""

	def __init__(self, pos = pygame.Vector2(0, 0), vel = pygame.Vector2(0, 0), size = 1) :
		if type(pos) != pygame.Vector2 :
			return NotImplemented

		if type(vel) != pygame.Vector2 :
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

		pygame.draw.circle(screen, color, self.pos, self.size)
