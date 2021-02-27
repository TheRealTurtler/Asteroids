import pygame
from src.SpaceObject import SpaceObject


class Projectile(SpaceObject):
	maxWrap = 1

	def __init__(self, pos, velDir, speed=2, size=1):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(velDir) != pygame.Vector2:
			raise TypeError

		if type(speed) not in (int, float):
			raise TypeError

		if type(size) not in (int, float):
			raise TypeError

		# SpaceObject initialisieren
		super().__init__(pos, velDir, speed, size)

		# Anzahl, wie oft das Projektil schon den Bildschirm verlassen hat
		self.wrap = 0
