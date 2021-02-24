import pygame
from src.Text import Text
from src.Color import Color


class Button:
	textSpacing = 20

	def __init__(self, rect, text, color = Color.WHITE):
		if type(rect) != pygame.Rect:
			raise TypeError

		if type(text) != str:
			raise TypeError

		self.rect = rect
		self.text = Text(pygame.Vector2(0, 0), text)
		self.text.pos = pygame.Vector2(
			self.rect.x + self.rect.width / 2 - self.text.width() / 2,
			self.rect.y + self.rect.height / 2 - self.text.height() / 2,
		)

		self.color = color

	def setColor(self, color):
		if type(color) != pygame.Color:
			raise TypeError

		self.color = color
		self.text.setColor(self.color)

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		pygame.draw.rect(screen, self.color, self.rect, 2)
		self.text.draw(screen)
