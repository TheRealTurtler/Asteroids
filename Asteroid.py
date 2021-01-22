import pygame

#from Vector2D import *

class Asteroid :
	"""description of class"""

	def __init__(self, pos = pygame.Vector2(0, 0), vel = pygame.Vector2(0, 0), size = 30) :
		self.pos = pos
		self.vel = vel
		self.size = size
		self.rot = 0

	def update(self) :
		self.pos += self.vel
	
	def draw(self, screen, color = pygame.Color(255, 255, 255)) :
		if type(screen) != pygame.Surface :
			return NotImplemented
		
		if type(color) != pygame.Color :
			return NotImplemented

		pygame.draw.circle(screen, color, self.pos, self.size, 1)
