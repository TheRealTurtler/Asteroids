import pygame

from src.Text import Text
from src.Color import Color


class Highscores:
	# Einstellungen
	maxCountScores = 10

	def __init__(self, highscoreFile):
		if type(highscoreFile) != str:
			raise TypeError

		self.highscoreFile = highscoreFile

		self.active = False

		self.data = []
		self.ui = []

		try:
			# Datei oeffnen
			with open(self.highscoreFile, 'r') as handle:
				# Highscores auslesen
				self.data = handle.readlines()
		except OSError:
			# Datei nicht vorhanden
			with open(self.highscoreFile, 'w') as handle:
				# Datei mit Nullen fuellen
				for i in range(0, 10):
					self.data.append("0\n")

				handle.writelines(self.data)

		# Highscore auslesen (Datei ist sortiert, also ersten Score)
		self.highscore = int(self.data[0][:-1])

		# UI
		textSpacing = 20
		upperLeft = pygame.Vector2(textSpacing, textSpacing)

		textHighscores = Text(upperLeft, "Highscores")
		self.ui.append(textHighscores)

		for (idx, d) in enumerate(self.data):
			self.ui.append(Text(pygame.Vector2(upperLeft.x,	self.ui[idx].pos.y + self.ui[idx].height() + textSpacing), d[:-1]))

	def addScore(self, score):
		if type(score) != int:
			raise TypeError

		# Neuer Highscore-Eintrag, wenn Score groesser als letzter Highscore (Liste ist sortiert)
		if score > int(self.data[-1][:-1]):
			self.data[-1] = str(score) + "\n"

			# Liste sortieren (absteigend)
			self.data.sort(key = lambda element: int(element[:-1]), reverse = True)

			# Top-Highscore aktualisieren
			self.highscore = int(self.data[0][:-1])

			# Liste in Datei speichern
			with open(self.highscoreFile, 'w') as handle:
				handle.writelines(self.data)

			# UI aktualisieren
			for (idx, d) in enumerate(self.data):
				self.ui[idx + 1].setText(d[:-1])

			# Rueckgabe: neuer Highscore
			return True

		# Rueckgabe: kein neuer Highscore
		return False

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Bildschirm schwarz zeichnen
		screen.fill(Color.BLACK)

		# UI zeichnen
		for i in self.ui:
			i.draw(screen)
