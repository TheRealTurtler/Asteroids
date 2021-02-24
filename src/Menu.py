import pygame

from src.EventHandler import EventHandler
from src.Button import Button
from src.Color import Color


class Menu:
	buttonSize = (200, 20)

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

		# TODO: better positioning
		self.button_ResumeGame = Button(pygame.Vector2(20, 20), 400, 80, "Resume Game")
		self.button_StartNewGame = Button(pygame.Vector2(20, 120), 400, 80, "Start New Game")
		self.button_Highscores = Button(pygame.Vector2(20, 220), 400, 80, "Highscores")
		self.button_Quit = Button(pygame.Vector2(20, 320), 400, 80, "Quit Game")

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

	def update(self):
		# TODO: button highlighting (hover)

		if self.eventHandler.pressed_M_Left:
			# TODO: button highlighting (press)
			self.eventHandler.pressed_M_Left = False
			self.eventHandler.pressed_M_Pos = ()

		if self.eventHandler.released_M_Left:
			if self.pointInRect(self.button_ResumeGame.rect, self.eventHandler.released_M_Pos):
				self.active = False
				self.selection = Menu.MenuSelection.resumeGame
				print("Resume Game")
			elif self.pointInRect(self.button_StartNewGame.rect, self.eventHandler.released_M_Pos):
				self.active = False
				self.selection = Menu.MenuSelection.startNewGame
				print("Start New Game")
			elif self.pointInRect(self.button_Highscores.rect, self.eventHandler.released_M_Pos):
				self.active = False
				self.selection = Menu.MenuSelection.highscores
				print("Highscores")
			elif self.pointInRect(self.button_Quit.rect, self.eventHandler.released_M_Pos):
				self.active = False
				self.selection = Menu.MenuSelection.quit
				print("Quit Game")

			self.eventHandler.released_M_Left = False
			self.eventHandler.released_M_Pos = ()

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		# Clear screen
		screen.fill(Color.BLACK)

		# Buttons zeichnen
		self.button_ResumeGame.draw(screen)
		self.button_StartNewGame.draw(screen)
		self.button_Highscores.draw(screen)
		self.button_Quit.draw(screen)
