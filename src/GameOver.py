import pygame

from src.EventHandler import EventHandler
from src.Text import Text
from src.Color import Color


class GameOver:
	textSpacing = 20

	def __init__(self, screenSize, eventHandler):
		if type(screenSize) != tuple:
			raise TypeError

		if len(screenSize) != 2:
			raise IndexError

		if type(eventHandler) != EventHandler:
			raise TypeError

		self.screenSize = screenSize
		self.eventHandler = eventHandler

		self.active = False

		self.textGameOver = Text(pygame.Vector2(0, 0), "Game Over", 48)
		self.textNewHighScore = Text(pygame.Vector2(0, 0), "New Highscore Entry!", 48)
		self.textScoreNumber = Text(pygame.Vector2(0,0), "0", 48)

		self.textGameOver.pos = pygame.Vector2(
			self.screenSize[0] / 2 - self.textGameOver.width() / 2,
			self.screenSize[1] / 2 - self.textGameOver.height() / 2
		)

		self.ui = [self.textGameOver]

	def newHighscore(self, highscore):
		if type(highscore) not in (int, bool):
			raise TypeError

		if highscore > 0:
			self.textNewHighScore.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textNewHighScore.width() / 2,
				self.screenSize[1] / 2 - self.textNewHighScore.height() / 2
			)

			self.textGameOver.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textGameOver.width() / 2,
				self.textNewHighScore.pos.y - self.textGameOver.height() - self.textSpacing
			)

			self.textScoreNumber.setText(str(highscore))

			self.textScoreNumber.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textScoreNumber.width() / 2,
				self.textNewHighScore.pos.y + self.textNewHighScore.height() + self.textSpacing
			)

			self.ui = [self.textGameOver, self.textNewHighScore, self.textScoreNumber]

		else:
			self.textGameOver.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textGameOver.width() / 2,
				self.screenSize[1] / 2 - self.textGameOver.height() / 2
			)

			self.ui = [self.textGameOver]

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Spielfeld löschen
		screen.fill(Color.BLACK)

		for i in self.ui:
			i.draw(screen)
