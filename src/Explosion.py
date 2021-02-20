import pygame
import random
from Spaceobject import Spaceobject
from Projectile import Projectile


class Explosion(Spaceobject):

	def __init__(self, pos):

		# Definiert Ursprung der Explosion
		super().__init__(pos,  pygame.Vector2(0, 0), 0, 1)

		self.timeExpStart = pygame.time.get_ticks()

		self.sizeTeilchen = 1
		self.speedTeilchen = 1
		self.teilchen = []

		for x in range(random.randint(5, 20)):

			directionTeilchen = pygame.Vector2(
				(random.random() - 0.5),		# Zufällige Richtung
				(random.random() - 0.5)
			)

			self.teilchen.append(
				Spaceobject(pygame.Vector2(pos), directionTeilchen, self.speedTeilchen, self.sizeTeilchen)
			)

	def update(self):
		for t in self.teilchen:
			t.pos += t.dir * t.speed

	def drawExp(self, screen, color=pygame.Color(255, 255, 255)):
		if type(screen) != pygame.Surface:
			raise TypeError

		if type(color) != pygame.Color:
			return TypeError

		for t in self.teilchen:
			pygame.draw.circle(screen, color, t.pos, t.size, 1)
