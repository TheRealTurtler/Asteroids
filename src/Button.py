import pygame
from src.Text import Text
from src.Color import Color


class Button:
	textSpacing = 20

	def __init__(self, pos, width, height, text):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(width) != int:
			raise TypeError

		if type(height) != int:
			raise TypeError

		if type(text) != str:
			raise TypeError

		self.rect = pygame.Rect(pos.x, pos.y, width, height)
		self.text = Text(pos + pygame.Vector2(self.textSpacing, self.textSpacing), text)

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		pygame.draw.rect(screen, Color.WHITE, self.rect, 1)
		self.text.draw(screen)
