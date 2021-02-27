import pygame

from src.Color import Color


class Text:
	def __init__(self, pos = pygame.Vector2(0, 0), text = "", size = 32, color = Color.WHITE):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(text) != str:
			raise TypeError

		if type(size) != int:
			raise TypeError

		if type(color) != pygame.Color:
			raise TypeError

		# Test, ob das Schriftmodul von pygame initialisiert wurde
		# sollte durch pygame.init() geschehen, aber sicher ist sicher
		if pygame.font.get_init() == 0:
			print("Font module not initialized!")
			print("Initializing now...")
			pygame.font.init()

		self.pos = pos			# Position
		self.text = text		# Text
		self.size = size		# Groesse
		self.color = color		# Schriftfarbe

		# Schriftart
		# https://www.dafont.com/retro-gaming.font
		self.font = pygame.font.Font("./resources/Retro_Gaming.ttf", self.size)

		# Text als Bild (pygame zeichnet nur Texturen, keinen Text direkt)
		self.img = self.font.render(self.text, True, self.color)

	def width(self):
		# Rueckgabe: Breite des Textes auf dem Bildschirm
		return self.img.get_width()

	def height(self):
		# Rueckgabe: Hoehe des Textes auf dem Bildschirm
		return self.img.get_height()

	def setText(self, text):
		if type(text) != str:
			raise TypeError

		# Bild neu aus Text erzeugen
		self.img = self.font.render(text, True, self.color)

	def setColor(self, color):
		if type(color) != pygame.Color:
			raise TypeError

		# Bild des Textes mit anderer Schriftfarbe erzeugen
		self.color = color
		self.img = self.font.render(self.text, True, self.color)

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Text zeichnen
		screen.blit(self.img, self.pos)
