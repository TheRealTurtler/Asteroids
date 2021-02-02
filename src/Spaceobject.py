import pygame


class Spaceobject:

	def __init__(self, pos, direction, speed, size):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(direction) != pygame.Vector2:
			raise TypeError

		if type(size) not in (int, float):
			raise TypeError

		if type(speed) not in (int, float):
			raise TypeError

		self.pos = pos
		self.dir = direction.normalize() if direction != pygame.Vector2(0, 0) else pygame.Vector2(0, 0)
		self.speed = speed
		self.size = size

	def update(self):
		self.pos += self.dir * self.speed

	def drawCircle(self, screen, color=pygame.Color(0, 255, 0)):
		if type(screen) != pygame.Surface:
			return NotImplemented

		if type(color) != pygame.Color:
			return NotImplemented

		pygame.draw.circle(screen, color, self.pos, self.size, 1)
