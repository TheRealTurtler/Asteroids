import pygame

from src.EventHandler import EventHandler
from src.Text import Text
from src.Color import Color


class GameOver:
	# UI-Einstellungen
	textSpacing = 20

	# Zeit, fuer die Tastendruecke ignoriert werden
	displayDelay = 1000

	def __init__(self, screenSize, eventHandler):
		if type(screenSize) != tuple:
			raise TypeError

		if len(screenSize) != 2:
			raise IndexError

		if type(eventHandler) != EventHandler:
			raise TypeError

		self.screenSize = screenSize
		self.eventHandler = eventHandler

		self.timeUpdated = 0

		self.active = False

		# UI
		self.textGameOver = Text(pygame.Vector2(0, 0), "Game Over", 48)
		self.textNewHighScore = Text(pygame.Vector2(0, 0), "New Highscore Entry!", 48)
		self.textScoreNumber = Text(pygame.Vector2(0, 0), "0", 48)
		self.textPressAnyKey = Text(pygame.Vector2(0, 0), "Press any Key to continue...", 20)

		self.textGameOver.pos = pygame.Vector2(
			self.screenSize[0] / 2 - self.textGameOver.width() / 2,
			self.screenSize[1] / 2 - self.textGameOver.height() / 2
		)

		self.textPressAnyKey.pos = pygame.Vector2(
			self.screenSize[0] / 2 - self.textPressAnyKey.width() / 2,
			self.screenSize[1] - self.textPressAnyKey.height() - GameOver.textSpacing
		)

		self.ui = [self.textGameOver]

	def newHighscore(self, highscore):
		if type(highscore) not in (int, bool):
			raise TypeError

		self.timeUpdated = pygame.time.get_ticks()

		if highscore > 0:
			# Game Over Screen mit Highscore
			self.textNewHighScore.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textNewHighScore.width() / 2,
				self.screenSize[1] / 2 - self.textNewHighScore.height() / 2
			)

			self.textGameOver.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textGameOver.width() / 2,
				self.textNewHighScore.pos.y - self.textGameOver.height() - GameOver.textSpacing
			)

			self.textScoreNumber.setText(str(highscore))

			self.textScoreNumber.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textScoreNumber.width() / 2,
				self.textNewHighScore.pos.y + self.textNewHighScore.height() + GameOver.textSpacing
			)

			self.ui = [self.textGameOver, self.textNewHighScore, self.textScoreNumber]

		else:
			# Game Over Screen ohne Highscore
			self.textGameOver.pos = pygame.Vector2(
				self.screenSize[0] / 2 - self.textGameOver.width() / 2,
				self.screenSize[1] / 2 - self.textGameOver.height() / 2
			)

			self.ui = [self.textGameOver]

		self.ui.append(self.textPressAnyKey)

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Bildschirm schwarz zeichnen
		screen.fill(Color.BLACK)

		# UI zeichnen
		for i in self.ui:
			i.draw(screen)
