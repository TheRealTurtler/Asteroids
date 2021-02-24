import pygame
import random

from src.EventHandler import EventHandler
from src.Player import Player
from src.Asteroid import Asteroid
from src.Projectile import Projectile
from src.Sound import Sound
from src.PowerUp import PowerUp
from src.Explosion import Explosion
from src.Color import Color
from src.Text import Text


class Game:
	def __init__(self, screenSize, eventHandler):
		if type(screenSize) != tuple:
			raise TypeError

		if len(screenSize) != 2:
			raise IndexError

		if type(eventHandler) != EventHandler:
			raise TypeError

		# Zufallszahlen initialisieren
		random.seed()

		self.screenSize = screenSize
		self.eventHandler = eventHandler

		self.active = False

		self.projectiles = []
		self.asteroids = []
		self.explosions = []
		self.ui = []

		self.collectablePowerUps = []
		self.lastPowerUpSpawnTime = pygame.time.get_ticks()
		#self.itemActiveFlag = 0
		#self.upgrade = ["firerate", "speed", "projectilspeed"]
		#self.itemDuration = 10000

		#self.projSpeedDefault = 2
		#self.projSpeed = self.projSpeedDefault

		#self.expDuration = 1000

		self.player = Player()

		self.player.pos = pygame.Vector2(self.screenSize[0] / 2, self.screenSize[1] / 2)

		pygame.display.set_caption("Asteroids")

		# Sound Einstellungen
		laser_wav = r'./resources/laser.wav'  # Laser pew sound lesen
		asteroid_wav = r'./resources/asteroid3.wav'  # asteriod explosion sound lesen
		powerup_wav = r'./resources/powerUp1.wav'  # powerUp sound lesen

		Sound.init()  # Initialisieren von pygame.mixer

		self.soundLaser = Sound(laser_wav, 0.03)  # Instanz gunSound der Klasse Sound hat nun Laser pew sound
		self.soundExplosion = Sound(asteroid_wav, 0.1)
		self.powerup = Sound(powerup_wav, 0.03)
		# Hintergrundmusik ist Tetris-Theme in pygame.music (keine Klasse da nur eine Hintergrundmusik)
		pygame.mixer.music.load('./resources/Tetris.wav')
		pygame.mixer.music.set_volume(0.03)  # leiser machen
		pygame.mixer.music.play(-1)  # Spiele Tetris-Theme als Loop (-1) ab

		textSpacing = 20
		textUpperLeft = pygame.Vector2(textSpacing, textSpacing)
		textUpperRight = pygame.Vector2(self.screenSize[0] - textSpacing, textSpacing)

		textScore = Text(pygame.Vector2(textUpperLeft), "Score:")
		self.textScoreNumber = Text(pygame.Vector2(textUpperLeft.x + textScore.width() + textSpacing, textUpperLeft.y), "0")
		textLives = Text(pygame.Vector2(textUpperLeft.x, textUpperLeft.y + textScore.height() + textSpacing), "Lives:")
		self.textLivesNumber = Text(pygame.Vector2(textUpperLeft.x + textLives.width() + textSpacing, textUpperLeft.y + textScore.height() + textSpacing), "5")

		textHighscore = Text(pygame.Vector2(0, 0), "Highscore:")
		textHighscoreNumber = Text(pygame.Vector2(0, 0), "0")
		textHighscore.pos = pygame.Vector2(textUpperRight.x - textHighscoreNumber.width() - textSpacing - textHighscore.width(), textUpperRight.y)
		textHighscoreNumber.pos = pygame.Vector2(textUpperRight.x - textHighscoreNumber.width(), textUpperRight.y)

		self.ui.append(textScore)
		self.ui.append(self.textScoreNumber)
		self.ui.append(textLives)
		self.ui.append(self.textLivesNumber)
		self.ui.append(textHighscore)
		self.ui.append(textHighscoreNumber)

	def colCircle(self, col1, col2):
		if type(col1) not in (Player, Asteroid, Projectile, PowerUp):
			raise TypeError

		if type(col2) not in (Player, Asteroid, Projectile, PowerUp):
			raise TypeError

		if (col2.pos - col1.pos).magnitude() < col1.size + col2.size:
			return True

		return False

	def resume(self):
		# Direkten PowerUp spawn verhindern, wenn das Spiel fortgesetzt wird
		# Nicht ideal, da somit der Timer verlängert wird, wenn das Spiel pausiert wird
		# TODO: better PowerUp spawn timer when resuming the game
		self.lastPowerUpSpawnTime = pygame.time.get_ticks()

	def update(self):
		# Asteroiden spawnen
		if len(self.asteroids) == 0:  # Neue Asteroiden spawnen, wenn keine mehr da sind
			for a in range(0, random.randrange(1, 5)):  # Zufällig zwischen 1 und 5 Asteroiden spawnen
				pos = self.player.pos

				# Asteroid nicht direkt auf Spieler spawnen
				while (pos - self.player.pos).magnitude() < Asteroid.sizeBig * 4:
					pos = pygame.Vector2(
						random.randrange(0, self.screenSize[0]),  # Zufällige Position auf dem Bildschirm
						random.randrange(0, self.screenSize[1])
					)

				vel = pygame.Vector2(
					(random.random() - 0.5) * 4,		# Zufällige Geschwindigkeit
					(random.random() - 0.5) * 4			# * 4, sodass maximale Geschwindigkeit 2 ist
				)

				rotSpeed = random.uniform(-2, 2)

				self.asteroids.append(Asteroid(pos, vel, rotSpeed))

		# PowerUp spawnen
		if pygame.time.get_ticks() - self.lastPowerUpSpawnTime > PowerUp.spawnDelay and len(self.collectablePowerUps) < 5:
			self.lastPowerUpSpawnTime = pygame.time.get_ticks()

			pos = self.player.pos

			# Item nicht direkt auf Spieler spawnen
			while (pos - self.player.pos).magnitude() < PowerUp.size * 4:
				pos = pygame.Vector2(
					random.randrange(0, self.screenSize[0]),  # Zufällige Position auf dem Bildschirm
					random.randrange(0, self.screenSize[1])
				)

			self.collectablePowerUps.append(PowerUp(pos, random.randrange(0, PowerUp.availablePowerUps)))
			# self.collectablePowerUps.append(PowerUp(pos, 3))

		# Beschleunigung nach gedrückten Tasten festlegen
		if self.eventHandler.pressed_W and not self.eventHandler.pressed_S:
			self.player.acc.y = -self.player.accMax
		if self.eventHandler.pressed_A and not self.eventHandler.pressed_D:
			self.player.acc.x = -self.player.accMax
		if self.eventHandler.pressed_S and not self.eventHandler.pressed_W:
			self.player.acc.y = self.player.accMax
		if self.eventHandler.pressed_D and not self.eventHandler.pressed_A:
			self.player.acc.x = self.player.accMax

		# Beschleunigung = 0, wenn entgegengesetzte Tasten gedrückt werden
		if self.eventHandler.pressed_W == self.eventHandler.pressed_S:
			self.player.acc.y = 0

		if self.eventHandler.pressed_A == self.eventHandler.pressed_D:
			self.player.acc.x = 0

		# Rotation Spieler
		if self.eventHandler.pressed_Left and not self.eventHandler.pressed_Right:
			self.player.rot -= self.player.rotPerTick
		if self.eventHandler.pressed_Right and not self.eventHandler.pressed_Left:
			self.player.rot += self.player.rotPerTick

		# Spielerposition aktualisieren
		self.player.update()

		# Spielfeldrand verlassen -> auf gegenüberliegender Seite weiter
		if self.player.pos.x < 0:
			self.player.pos.x = self.screenSize[0]
		elif self.player.pos.x > self.screenSize[0]:
			self.player.pos.x = 0

		if self.player.pos.y < 0:
			self.player.pos.y = self.screenSize[1]
		elif self.player.pos.y > self.screenSize[1]:
			self.player.pos.y = 0

		# Projektile
		if self.eventHandler.pressed_Space:
			# Feuerrate begrenzen
			if pygame.time.get_ticks() - self.player.timeLastShot > 1000 / self.player.fireRate:
				self.player.timeLastShot = pygame.time.get_ticks()

				# Laser sound
				self.soundLaser.play()

				# Neues Projektil zur Liste hinzufügen
				for sp in self.player.bulletSpawnPoints:
					self.projectiles.append(
						Projectile(
							pygame.Vector2(sp),
							pygame.Vector2(self.player.lookDir),
							self.player.projSpeed
						)
					)

		for p in self.projectiles[:]:
			# Positionen aller Projektile aktualisieren
			p.update()

			# Spielfeldrand verlassen -> auf gegenüberliegender Seite weiter
			if p.pos.x < 0:
				p.pos.x = self.screenSize[0]
				p.wrap += 1
			elif p.pos.x > self.screenSize[0]:
				p.pos.x = 0
				p.wrap += 1

			if p.pos.y < 0:
				p.pos.y = self.screenSize[1]
				p.wrap += 1
			elif p.pos.y > self.screenSize[1]:
				p.pos.y = 0
				p.wrap += 1

			# Projektile löschen, wenn sie zu oft den Bildschirmrand verlassen haben oder stehen bleiben
			if p.wrap > p.maxWrap or p.dir == pygame.Vector2(0, 0):
				self.projectiles.remove(p)

		for a in self.asteroids:
			# Positionen aller Asteroiden aktualisieren
			a.update()

			# Spielfeldrand verlassen -> auf gegenüberliegender Seite weiter
			if a.pos.x < 0:
				a.pos.x = self.screenSize[0]
			elif a.pos.x > self.screenSize[0]:
				a.pos.x = 0

			if a.pos.y < 0:
				a.pos.y = self.screenSize[1]
			elif a.pos.y > self.screenSize[1]:
				a.pos.y = 0

		for e in self.explosions:
			# Position aller Explosionen aktualisieren
			e.update()

			# Lösche Explosion
			if len(e.particles) == 0:
				self.explosions.remove(e)

		# Kollisionen
		for col1 in self.projectiles[:]:
			collision = False

			# Kugel - Spieler
			if self.colCircle(col1, self.player):
				collision = True
				self.soundExplosion.stop()  # Sound anhalten (falls bereits aktiv)
				self.soundExplosion.play()  # Sound abspielen
				self.explosions.append(Explosion(pygame.Vector2(self.player.pos)))

				# Lebenszahl aktualisieren
				self.player.lives -= 1 if self.player.lives > 0 else 0
				self.textLivesNumber.setText(str(self.player.lives))

			# Kugel - Asteroid
			for col2 in self.asteroids[:]:
				if self.colCircle(col1, col2):
					collision = True
					self.soundExplosion.stop()		# Sound anhalten (falls bereits aktiv)
					self.soundExplosion.play()		# Sound abspielen
					self.explosions.append(Explosion(pygame.Vector2(col2.pos)))

					# Punktzahl aktualisieren
					self.player.score += col2.scorePoints
					self.textScoreNumber.setText(str(self.player.score))

					# Wenn Asteroid groß genug -> kleinere Asteroiden spawnen
					if col2.size != Asteroid.sizeSmall:
						for a in range(0, random.randrange(1, 3)):  # Zufällig zwischen 1 und 3 Asteroiden spawnen
							pos = col2.pos + pygame.Vector2(
								random.randrange(-col2.size, col2.size),  # Zufälliger Abstand zum vorherigen Asteroiden
								random.randrange(-col2.size, col2.size)
							)

							vel = pygame.Vector2(
								(random.random() - 0.5) * 4,		# Zufällige Geschwindigkeit
								(random.random() - 0.5) * 4			# * 4, sodass maximale Geschwindigkeit 2 ist
							)

							size = Asteroid.sizeMedium

							rotSpeed = random.uniform(-2, 2)

							if col2.size == Asteroid.sizeMedium:
								size = Asteroid.sizeSmall

							self.asteroids.append(Asteroid(pos, vel, rotSpeed, size))

					self.asteroids.remove(col2)
					break

			# Kugel - Kugel
			# for col2 in self.projectiles[:] :
			# 	if col1 == col2 :
			# 		continue
			#
			# 	if self.colCircle(col1, col2) :
			# 		collision = True
			# 		self.projectiles.remove(col2)
			# 		break

			if collision:
				self.projectiles.remove(col1)

		# Asteroid - Spieler
		for col in self.asteroids[:]:
			if self.colCircle(col, self.player):
				self.soundExplosion.stop()  # Sound anhalten (falls bereits aktiv)
				self.soundExplosion.play()  # Sound abspielen
				self.explosions.append(Explosion(pygame.Vector2(self.player.pos)))
				self.explosions.append(Explosion(pygame.Vector2(col.pos)))
				self.asteroids.remove(col)

				# Lebenszahl aktualisieren
				self.player.lives -= 1 if self.player.lives > 0 else 0
				self.textLivesNumber.setText(str(self.player.lives))

		# PowerUp - Spieler
		for (idx, col) in enumerate(self.collectablePowerUps[:]):
			if self.colCircle(col, self.player):
				col.collectionTime = pygame.time.get_ticks()
				self.powerup.play()
				self.player.collectPowerUp(col)

				self.collectablePowerUps.remove(col)

		# Game Over
		if self.player.lives == 0:
			# TODO: Game Over
			pass

	# DEBUG
	# print(len(self.projectiles))
	# print(self.player.pos,
	# 	  self.player.vel,
	# 	  self.player.acc,
	# 	  self.pressed_W,
	# 	  self.pressed_A,
	# 	  self.pressed_S,
	# 	  self.pressed_D)

	def draw(self, screen):
		# Spielfeld löschen
		screen.fill(Color.BLACK)

		# Spieler zeichnen
		self.player.draw(screen, Color.WHITE)

		# Projektile zeichnen
		for p in self.projectiles:
			p.draw(screen, Color.WHITE)

		# Asteroiden zeichnen
		for a in self.asteroids:
			a.draw(screen, Color.WHITE)

		# PowerUps zeichnen
		for p in self.collectablePowerUps:
			p.draw(screen)

		# Explosion zeichnen
		for e in self.explosions:
			e.draw(screen)

		# Benutzeroberfläche (score etc.) zeichnen
		for i in self.ui:
			i.draw(screen)
