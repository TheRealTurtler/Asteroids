import pygame


class SpaceObject:
	def __init__(self, pos, direction = pygame.Vector2(0, 0), speed = 0, size = 1):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(direction) != pygame.Vector2:
			raise TypeError

		if type(size) not in (int, float):
			raise TypeError

		if type(speed) not in (int, float):
			raise TypeError

		# Position
		self.pos = pos

		# Richtung (normiert)
		self.dir = direction.normalize() if direction != pygame.Vector2(0, 0) else pygame.Vector2(0, 0)

		# Geschwindigkeit
		self.speed = speed

		# Groesse
		self.size = size

	def update(self):
		# Geschwindigkeit -> Position
		self.pos += self.dir * self.speed

	def draw(self, screen, color=pygame.Color(255, 255, 255)):
		if type(screen) != pygame.Surface:
			return TypeError

		if type(color) != pygame.Color:
			return TypeError

		# SpaceObject zeichnen
		pygame.draw.circle(screen, color, self.pos, self.size)
