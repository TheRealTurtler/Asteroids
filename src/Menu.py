import pygame

from src.EventHandler import EventHandler
from src.Button import Button
from src.Color import Color


class Menu:
	buttonSize = (300, 60)
	buttonColor = Color.WHITE
	buttonColorHover = Color.LIGHT_GREY
	buttonColorClick = Color.DARK_GREY

	class MenuSelection:
		resumeGame = 0
		startNewGame = 1
		highscores = 2
		quit = 3

	def __init__(self, screenSize, eventHandler):
		if type(screenSize) != tuple:
			raise TypeError

		if len(screenSize) != 2:
			raise IndexError

		if type(eventHandler) != EventHandler:
			raise TypeError

		self.eventHandler = eventHandler

		self.active = True
		self.selection = -1

		self.backgroundImg = pygame.image.load("./resources/menu_background.png")
		self.backgroundImg = pygame.transform.scale(self.backgroundImg, screenSize)
		self.backgroundImg = self.backgroundImg.convert()

		buttonSpacing = 20
		upperLeft = pygame.Vector2(buttonSpacing, buttonSpacing)

		self.button_ResumeGame = Button(pygame.Rect(upperLeft, self.buttonSize), "Resume Game", Menu.buttonColor)

		self.button_NewGame = Button(
			pygame.Rect((upperLeft.x, self.button_ResumeGame.rect.y + self.button_ResumeGame.rect.height + buttonSpacing), self.buttonSize),
			"New Game",
			Menu.buttonColor
		)

		self.button_Highscores = Button(
			pygame.Rect((upperLeft.x, self.button_NewGame.rect.y + self.button_NewGame.rect.height + buttonSpacing), self.buttonSize),
			"Highscores",
			Menu.buttonColor
		)

		self.button_Quit = Button(
			pygame.Rect((upperLeft.x, self.button_Highscores.rect.y + self.button_Highscores.rect.height + buttonSpacing), self.buttonSize),
			"Quit Game",
			Menu.buttonColor
		)

		self.buttons = [self.button_ResumeGame, self.button_NewGame, self.button_Highscores, self.button_Quit]

	def pointInRect(self, rect, point):
		if type(rect) != pygame.Rect:
			raise TypeError

		if type(point) not in (tuple, list, pygame.Vector2):
			raise TypeError

		if rect.x < point[0] < rect.x + rect.width:
			if rect.y < point[1] < rect.y + rect.height:
				return True

		return False

	def reload(self):
		self.active = True
		self.selection = -1
		self.eventHandler.pressed_M_Left = False
		self.eventHandler.pressed_M_Pos = ()
		self.eventHandler.released_M_Left = False
		self.eventHandler.released_M_Pos = ()

		for b in self.buttons:
			b.setColor(Menu.buttonColor)

	def update(self):
		# Buttons hervorheben (Hover)
		if not self.eventHandler.pressed_M_Left:
			for b in self.buttons:
				if self.pointInRect(b.rect, pygame.mouse.get_pos()):
					if b.color != Menu.buttonColorHover:
						b.setColor(Menu.buttonColorHover)
				elif b.color != Menu.buttonColor:
					b.setColor(Menu.buttonColor)

		# Buttons hervorheben (Klick)
		else:
			for b in self.buttons:
				if self.pointInRect(b.rect, self.eventHandler.pressed_M_Pos):
					if b.color != Menu.buttonColorClick:
						b.setColor(Color.DARK_GREY)

		if self.eventHandler.released_M_Left:
			# Spiel fortsetzen
			if self.pointInRect(self.button_ResumeGame.rect, self.eventHandler.released_M_Pos):
				if self.pointInRect(self.button_ResumeGame.rect, self.eventHandler.pressed_M_Pos):
					self.active = False
					self.selection = Menu.MenuSelection.resumeGame

			# Neues Spiel
			elif self.pointInRect(self.button_NewGame.rect, self.eventHandler.released_M_Pos):
				if self.pointInRect(self.button_NewGame.rect, self.eventHandler.pressed_M_Pos):
					self.active = False
					self.selection = Menu.MenuSelection.startNewGame

			# Highscores
			elif self.pointInRect(self.button_Highscores.rect, self.eventHandler.released_M_Pos):
				if self.pointInRect(self.button_Highscores.rect, self.eventHandler.pressed_M_Pos):
					self.active = False
					self.selection = Menu.MenuSelection.highscores

			# Spiel beenden
			elif self.pointInRect(self.button_Quit.rect, self.eventHandler.released_M_Pos):
				if self.pointInRect(self.button_Quit.rect, self.eventHandler.pressed_M_Pos):
					self.active = False
					self.selection = Menu.MenuSelection.quit

			# Reset Maus-Events
			self.eventHandler.pressed_M_Left = False
			self.eventHandler.pressed_M_Pos = ()
			self.eventHandler.released_M_Left = False
			self.eventHandler.released_M_Pos = ()

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Clear screen
		screen.fill(Color.BLACK)

		# Hintergrund
		screen.blit(self.backgroundImg, (0, 0))

		# Buttons zeichnen
		self.button_ResumeGame.draw(screen)
		self.button_NewGame.draw(screen)
		self.button_Highscores.draw(screen)
		self.button_Quit.draw(screen)
