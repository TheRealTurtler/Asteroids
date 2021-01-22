import pygame

from Player import *
from Asteroid import *
from Projectile import *
#from Vector2D import *
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
		self.pressed_Up = False
		self.pressed_Down = False
		self.pressed_Left = False
		self.pressed_Right = False

		self.projectiles = []
		self.asteroids = [Asteroid(pygame.Vector2(a*50, a*50)) for a in range(1, 5)]

		self.player = Player()

		self.player.pos = pygame.Vector2(100, 100)

		pygame.display.set_caption("Asteroids")

		# Sound Einstellungen
		lasergun_wav = r'lasergun.wav'			# Laser pew sound lesen

		Sound.init()							# Initialisieren von pygame.mixer

		self.gunsound = Sound(lasergun_wav)		# Instanz gunsound der Klasse Sound hat nun Laser pew sound

		pygame.mixer.music.load('Tetris.wav')	# Hintergrundmusik ist Tetris-Theme in pygame.music (keine Klasse da nur eine Hmusik)
		pygame.mixer.music.set_volume(0.03)		# leiser machen

		pygame.mixer.music.play(-1)				# Spiele Tetris-Theme als Loop (-1) ab
		

	def colCircle(self, col1, col2) :
		if type(col1) not in (Player, Asteroid, Projectile) :
			raise TypeError

		if type(col2) not in (Player, Asteroid, Projectile) :
			raise TypeError

		if (col2.pos - col1.pos).magnitude() < col1.size + col2.size :
			return True

		return False


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
				elif event.key == pygame.K_UP :
					self.pressed_Up = True
				elif event.key == pygame.K_DOWN :
					self.pressed_Down = True
				elif event.key == pygame.K_LEFT :
					self.pressed_Left = True
				elif event.key == pygame.K_RIGHT :
					self.pressed_Right = True

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
				elif event.key == pygame.K_UP :
					self.pressed_Up = False
				elif event.key == pygame.K_DOWN :
					self.pressed_Down = False
				elif event.key == pygame.K_LEFT :
					self.pressed_Left = False
				elif event.key == pygame.K_RIGHT :
					self.pressed_Right = False

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

		# Rotation Spieler
		if self.pressed_Left and not self.pressed_Right :
			self.player.rot -= self.player.rotPerTick
		if self.pressed_Right and not self.pressed_Left :
			self.player.rot += self.player.rotPerTick

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
				self.projectiles.append(
					Projectile(
						pygame.Vector2(self.player.bulletSpawn),
						pygame.Vector2(self.player.bulletSpawn - self.player.pos)
						)
					)

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

			# Projektile löschen, wenn sie zu oft den Bildschirmrandverlassen haben oder stehen bleiben
			if p.wrap > p.maxWrap or p.dir == pygame.Vector2(0, 0) :
				self.projectiles.remove(p)

		for a in self.asteroids :
			# Positionen aller Asteroiden aktualisieren
			a.update()

			# Spielfeldrand verlassen -> auf ggegenüberliegender Seite weiter
			if a.pos.x < 0 :
				a.pos.x = self.screenSize[0]
			elif a.pos.x > self.screenSize[0] :
				a.pos.x = 0

			if a.pos.y < 0 :
				a.pos.y = self.screenSize[1]
			elif a.pos.y > self.screenSize[1] :
				a.pos.y = 0

		# Kollision
		for col1 in self.projectiles[:] :
			collision = False

			if self.colCircle(col1, self.player) :
				collision = True
				print("GAME OVER")				# TODO

			for col2 in self.asteroids[:] :
				if self.colCircle(col1, col2) :
					collision = True
					self.asteroids.remove(col2)
					break

			#for col2 in self.projectiles[:] :
			#	if col1 == col2 :
			#		continue

			#	if self.colCircle(col1, col2) :
			#		collision = True
			#		self.projectiles.remove(col2)
			#		break

			if collision :
				self.projectiles.remove(col1)
				continue

		for col1 in self.asteroids[:] :
			if self.colCircle(col1, self.player) :
				self.asteroids.remove(col1)
				print("GAME OVER")				# TODO

		print(len(self.projectiles))


	def draw(self, screen) :
		# Spieler zeichnen
		self.player.draw(screen, self.WHITE)

		# Projektile zeichnen
		for p in self.projectiles :
			p.draw(screen, self.WHITE)

		# Asteroiden zeichnen
		for a in self.asteroids :
			a.draw(screen, self.WHITE)
