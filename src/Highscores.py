import pygame

from src.Text import Text
from src.Color import Color


class Highscores:
	def __init__(self, highscoreFile):
		if type(highscoreFile) != str:
			raise TypeError

		self.highscoreFile = highscoreFile

		self.active = False
		self.data = []
		self.ui = []

		with open(self.highscoreFile, 'r') as handle:
			self.data = handle.readlines()

		self.highscore = int(self.data[0][:-1])

		textSpacing = 20
		upperLeft = pygame.Vector2(textSpacing, textSpacing)

		textHighscores = Text(upperLeft, "Highscores")
		self.ui.append(textHighscores)

		for (idx, d) in enumerate(self.data):
			self.ui.append(Text(pygame.Vector2(upperLeft.x,	self.ui[idx].pos.y + self.ui[idx].height() + textSpacing), d[:-1]))

	def addScore(self, score):
		if type(score) != int:
			raise TypeError

		if score > int(self.data[-1][:-1]):
			self.data[-1] = str(score) + "\n"
			self.data.sort(key = lambda element: int(element[:-1]), reverse = True)
			self.highscore = int(self.data[0][:-1])

			with open(self.highscoreFile, 'w') as handle:
				handle.writelines(self.data)

			for (idx, d) in enumerate(self.data):
				self.ui[idx + 1].setText(d[:-1])

			return True

		return False

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Spielfeld löschen
		screen.fill(Color.BLACK)

		for i in self.ui:
			i.draw(screen)
