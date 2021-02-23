import pygame


class EventHandler:
	def __init__(self):
		# Fenster aktiv
		self.windowActive = True

		# Tastatur
		self.pressed_W = False
		self.pressed_A = False
		self.pressed_S = False
		self.pressed_D = False
		self.pressed_Space = False
		self.pressed_Up = False
		self.pressed_Down = False
		self.pressed_Left = False
		self.pressed_Right = False
		self.pressed_Esc = False

		# Maus
		self.pressed_M_Left = False
		self.released_M_Left = False
		self.pressed_M_Pos = ()
		self.released_M_Pos = ()

	def handleEvents(self):
		for event in pygame.event.get():

			# Game quit
			if event.type == pygame.QUIT:
				self.windowActive = False

			# Key pressed
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					self.pressed_W = True
				elif event.key == pygame.K_a:
					self.pressed_A = True
				elif event.key == pygame.K_s:
					self.pressed_S = True
				elif event.key == pygame.K_d:
					self.pressed_D = True
				elif event.key == pygame.K_SPACE:
					self.pressed_Space = True
				elif event.key == pygame.K_UP:
					self.pressed_Up = True
				elif event.key == pygame.K_DOWN:
					self.pressed_Down = True
				elif event.key == pygame.K_LEFT:
					self.pressed_Left = True
				elif event.key == pygame.K_RIGHT:
					self.pressed_Right = True
				elif event.key == pygame.K_ESCAPE:
					self.pressed_Esc = True

			# Key released
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					self.pressed_W = False
				elif event.key == pygame.K_a:
					self.pressed_A = False
				elif event.key == pygame.K_s:
					self.pressed_S = False
				elif event.key == pygame.K_d:
					self.pressed_D = False
				elif event.key == pygame.K_SPACE:
					self.pressed_Space = False
				elif event.key == pygame.K_UP:
					self.pressed_Up = False
				elif event.key == pygame.K_DOWN:
					self.pressed_Down = False
				elif event.key == pygame.K_LEFT:
					self.pressed_Left = False
				elif event.key == pygame.K_RIGHT:
					self.pressed_Right = False
				elif event.key == pygame.K_ESCAPE:
					self.pressed_Esc = False

			# Mouse button pressed
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					self.pressed_M_Left = True
					self.pressed_M_Pos = event.pos

			# Mouse button released
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.released_M_Left = True
					self.released_M_Pos = event.pos
