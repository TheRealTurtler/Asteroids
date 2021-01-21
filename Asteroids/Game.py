import pygame

from Player import *
from Projectile import *
from Vector2D import *
from Sound import *

class Game :
	"""description of class"""

	WHITE = pygame.Color(255, 255, 255)
	BLACK = pygame.Color(0, 0, 0)

	def __init__(self, screenSize) :
		if type(screenSize) != tuple :
			return NotImplemented

		if len(screenSize) != 2 :
			raise IndexError

		self.screenSize = screenSize

		self.gameActive = True

		self.pressed_W = False
		self.pressed_A = False
		self.pressed_S = False
		self.pressed_D = False
		self.pressed_Space = False

		self.projectiles = []

		self.player = Player()

		self.player.pos = Vector2D(100, 100)

		pygame.display.set_caption("Asteroids")

		# Sound Einstellungen
		lasergun_wav = r'lasergun.wav'			# Laser pew sound lesen

		Sound.init()							# Initialisieren von pygame.mixer

		self.gunsound = Sound(lasergun_wav)		# Instanz gunsound der Klasse Sound hat nun Laser pew sound

		pygame.mixer.music.load('Tetris.wav')	# Hintergrundmusik ist Tetristheme in pygame.music (keine Klasse da nur eine Hmusik)
		pygame.mixer.music.set_volume(0.03)		# leiser machen

		pygame.mixer.music.play(-1)		# Spiele tetris theme ab auf loop (-1)
		

	def handleEvents(self) :
		for event in pygame.event.get() :

			# Game quit
			if event.type == pygame.QUIT :
				self.gameActive = False

			# Key pressed
			elif event.type == pygame.KEYDOWN :
				if event.key == pygame.K_w :
					self.pressed_W = True
				elif event.key == pygame.K_a :
					self.pressed_A = True
				elif event.key == pygame.K_s :
					self.pressed_S = True
				elif event.key == pygame.K_d :
					self.pressed_D = True
				elif event.key == pygame.K_SPACE :
					self.pressed_Space = True

			# Key released
			elif event.type == pygame.KEYUP :
				if event.key == pygame.K_w :
					self.pressed_W = False
				elif event.key == pygame.K_a :
					self.pressed_A = False
				elif event.key == pygame.K_s :
					self.pressed_S = False
				elif event.key == pygame.K_d :
					self.pressed_D = False
				elif event.key == pygame.K_SPACE :
					self.pressed_Space = False

			# Mouse button pressed
			#elif event.type == pygame.MOUSEBUTTONDOWN :


	def update(self) :
		# Beschleunigung nach gedrückten Tasten festlegen
		if self.pressed_W and not self.pressed_S :
			self.player.acc.y = -self.player.accMax.y
		if self.pressed_A and not self.pressed_D :
			self.player.acc.x = -self.player.accMax.x
		if self.pressed_S and not self.pressed_W :
			self.player.acc.y = self.player.accMax.y
		if self.pressed_D and not self.pressed_A :
			self.player.acc.x = self.player.accMax.x

		# Beschleunigung = 0, wenn entgegengesetzte Tasten gedrückt werden
		if self.pressed_W == self.pressed_S :
			self.player.acc.y = 0

		if self.pressed_A == self.pressed_D :
			self.player.acc.x = 0

		# Spielerposition aktualisieren
		self.player.update()

		# Spielfeldrand verlassen -> auf ggegenüberliegender Seite weiter
		if self.player.pos.x < 0 :
			self.player.pos.x = self.screenSize[0]
		elif self.player.pos.x > self.screenSize[0] :
			self.player.pos.x = 0

		if self.player.pos.y < 0 :
			self.player.pos.y = self.screenSize[1]
		elif self.player.pos.y > self.screenSize[1] :
			self.player.pos.y = 0

		# Projektile
		if self.pressed_Space :
			if pygame.time.get_ticks() - self.player.timeLastShot > 1000 / self.player.fireRate :
				self.player.timeLastShot = pygame.time.get_ticks()
			
				# Lasergun pew sound
				self.gunsound.play()	
		
				# Neues Projektil zur Liste hinzufügen
				self.projectiles.append(Projectile(self.player.pos, Vector2D(0, 2)))

		for p in self.projectiles[:] :
			# Positionen aller Projektile aktualisieren
			p.update()
		
			# Spielfeldrand verlassen -> auf ggegenüberliegender Seite weiter
			if p.pos.x < 0 :
				p.pos.x = self.screenSize[0]
				p.wrap += 1
			elif p.pos.x > self.screenSize[0] :
				p.pos.x = 0
				p.wrap += 1

			if p.pos.y < 0 :
				p.pos.y = self.screenSize[1]
				p.wrap += 1
			elif p.pos.y > self.screenSize[1] :
				p.pos.y = 0
				p.wrap += 1

			# Projektile löschen, wenn sie zu oft den Bildschirmrandverlassen haben
			if p.wrap > p.maxWrap :
				self.projectiles.remove(p)


	def draw(self, screen) :
		# Spieler zeichnen
		self.player.draw(screen, self.WHITE)

		#Projektile zeichnen
		for p in self.projectiles :
			p.draw(screen, self.WHITE)