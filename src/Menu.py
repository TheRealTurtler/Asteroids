import pygame

from Button import Button


class Menu:
	buttonSize = (200, 20)

	def __init__(self, screenSize):
		if type(screenSize) != tuple:
			raise TypeError

		if len(screenSize) != 2:
			raise IndexError

		self.active = True

		self.button_StartGame = Button(pygame.Vector2(20, 20), 200, 60, "Start Game")

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		self.button_StartGame.draw(screen)
