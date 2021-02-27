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
	# Spieleinstellungen
	maxCountAsteroids = 8
	maxCountSmallerAsteroids = 4
	maxCountPowerUps = 5

	# Spielzustaende
	class GameStates:
		inactive = 0		# Spiel pausiert (Menue)
		active = 1			# Spiel aktiv
		over = 2			# Spiel vorbei (Highscore noch nicht ueberprueft)
		ended = 3			# Spiel vorbei (Highscore bereits ueberprueft)

	def __init__(self, screenSize, eventHandler, highscore):
		if type(screenSize) != tuple:
			raise TypeError

		if len(screenSize) != 2:
			raise IndexError

		if type(eventHandler) != EventHandler:
			raise TypeError

		if type(highscore) != int:
			raise TypeError

		# Zufallszahlen initialisieren
		random.seed()

		self.screenSize = screenSize
		self.eventHandler = eventHandler
		self.highscore = highscore

		self.state = Game.GameStates.inactive

		self.projectiles = []
		self.asteroids = []
		self.explosions = []
		self.ui = []
		self.collectablePowerUps = []

		self.lastPowerUpSpawnTime = pygame.time.get_ticks()

		self.player = Player(pygame.Vector2(self.screenSize[0] / 2, self.screenSize[1] / 2))

		pygame.display.set_caption("Asteroids")

		# Sounddateien
		laser_wav = r'./resources/laser.wav'  			# Sound Laser
		asteroid_wav = r'./resources/asteroid3.wav'  	# Sound Explosion
		powerup_wav = r'./resources/powerUp1.wav'  		# Sound PowerUp

		Sound.init()  # Initialisieren von pygame.mixer

		# Sounds laden
		self.soundLaser = Sound(laser_wav, 0.03)
		self.soundExplosion = Sound(asteroid_wav, 0.1)
		self.soundPowerUp = Sound(powerup_wav, 0.1)
		# Hintergrundmusik ist Tetris-Theme in pygame.music (keine Klasse da nur eine Hintergrundmusik)
		pygame.mixer.music.load('./resources/Tetris.wav')
		pygame.mixer.music.set_volume(0.03)
		pygame.mixer.music.play(-1)		# Spiele Tetris-Theme als Loop (-1) ab

		# UI-Einstellungen
		textSpacing = 20
		textUpperLeft = pygame.Vector2(textSpacing, textSpacing)
		textUpperRight = pygame.Vector2(self.screenSize[0] - textSpacing, textSpacing)

		# UI (links oben)
		textScore = Text(pygame.Vector2(textUpperLeft), "Score:")
		self.textScoreNumber = Text(pygame.Vector2(textUpperLeft.x + textScore.width() + textSpacing, textUpperLeft.y), "0")
		textLives = Text(pygame.Vector2(textUpperLeft.x, textUpperLeft.y + textScore.height() + textSpacing), "Lives:")
		self.textLivesNumber = Text(pygame.Vector2(textUpperLeft.x + textLives.width() + textSpacing, textUpperLeft.y + textScore.height() + textSpacing), "5")

		# UI (rechts oben)
		textHighscore = Text(pygame.Vector2(0, 0), "Highscore:")
		textHighscoreNumber = Text(pygame.Vector2(0, 0), str(self.highscore))
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

		# Kreis - Kreis Kollision
		if (col2.pos - col1.pos).magnitude() < col1.size + col2.size:
			return True

		return False

	def resume(self):
		if self.player.lives > 0:
			self.state = Game.GameStates.active
		else:
			self.state = Game.GameStates.ended

		# Direkten PowerUp spawn verhindern, wenn das Spiel fortgesetzt wird
		# Nicht ideal, da somit der Timer verlängert wird, wenn das Spiel pausiert wird
		# TODO: better PowerUp spawn timer when resuming the game
		self.lastPowerUpSpawnTime = pygame.time.get_ticks()

	def update(self):
		# Asteroiden spawnen
		if len(self.asteroids) == 0:  # Neue Asteroiden spawnen, wenn keine mehr da sind
			for a in range(0, random.randint(1, Game.maxCountAsteroids)):  # Zufaellige Anzahl an Asteroiden spawnen
				pos = self.player.pos

				# Asteroid nicht direkt auf Spieler spawnen
				while (pos - self.player.pos).magnitude() < Asteroid.sizeBig * 4:
					# Zufaellige Position auf dem Bildschirm
					pos = pygame.Vector2(
						random.randint(0, self.screenSize[0]),
						random.randint(0, self.screenSize[1])
					)

				# Zufaellige Geschwindigkeit
				vel = pygame.Vector2(
					(random.random() - 0.5) * 2 * Asteroid.maxSpeed,
					(random.random() - 0.5) * 2 * Asteroid.maxSpeed
				)

				# Zufaellige Rotationsgeschwindigkeit (normalverteilt, weil schoener)
				rotSpeed = random.uniform(-Asteroid.maxRotSpeed, Asteroid.maxRotSpeed)

				# Asteroid erzeugen
				self.asteroids.append(Asteroid(pos, vel, rotSpeed))

		# PowerUp spawnen
		# Timer Reset so nicht ideal, da man die maximale Anzahl spawnen lassen kann und es spawnt beim einsammeln
		# evtl. direkt ein neues PowerUp
		# TODO: better PowerUP timer
		if pygame.time.get_ticks() - self.lastPowerUpSpawnTime > PowerUp.spawnDelay:
			self.lastPowerUpSpawnTime = pygame.time.get_ticks()

			# Maximale PowerUp Anzahl limitieren
			if len(self.collectablePowerUps) < Game.maxCountPowerUps:
				pos = self.player.pos

				# Item nicht direkt auf Spieler spawnen
				while (pos - self.player.pos).magnitude() < PowerUp.size * 4:
					pos = pygame.Vector2(
						random.randrange(0, self.screenSize[0]),  # Zufällige Position auf dem Bildschirm
						random.randrange(0, self.screenSize[1])
					)

				# PowerUp erzeugen
				self.collectablePowerUps.append(PowerUp(pos, random.randrange(0, PowerUp.availablePowerUps)))

		# Beschleunigung und Rotation nach gedrückten Tasten festlegen
		if self.eventHandler.pressed_W and not self.eventHandler.pressed_S:
			self.player.acc = self.player.lookDir * Player.accMax
			self.player.boostActive = True
		if self.eventHandler.pressed_A and not self.eventHandler.pressed_D:
			self.player.rot -= Player.rotPerTick
		if self.eventHandler.pressed_S or not self.eventHandler.pressed_W:
			self.player.acc = pygame.Vector2(0, 0)
			self.player.boostActive = False
		if self.eventHandler.pressed_D and not self.eventHandler.pressed_A:
			self.player.rot += Player.rotPerTick

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

				# Sound Laser
				self.soundLaser.play()

				# Projektil erzeugen
				for sp in self.player.bulletSpawnPoints:
					self.projectiles.append(
						Projectile(
							pygame.Vector2(sp),
							pygame.Vector2(self.player.lookDir),
							self.player.projSpeed
						)
					)

		for p in self.projectiles[:]:
			# Projektil aktualisieren
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

			# Projektile entfernen, wenn sie zu oft den Bildschirmrand verlassen haben oder stehen bleiben
			if p.wrap > Projectile.maxWrap or p.dir == pygame.Vector2(0, 0):
				self.projectiles.remove(p)

		for a in self.asteroids:
			# Asteroid aktualisieren
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
			# Explosion aktualisieren
			e.update()

			# Explosion entfernen, wenn keine Partikel mehr da
			if len(e.particles) == 0:
				self.explosions.remove(e)

		# Kollisionen
		for col1 in self.projectiles[:]:
			collision = False

			# Projektil - Spieler
			if self.colCircle(col1, self.player):
				collision = True
				# Explosion
				self.soundExplosion.stop()  # Sound anhalten (falls bereits aktiv)
				self.soundExplosion.play()  # Sound abspielen
				self.explosions.append(Explosion(pygame.Vector2(self.player.pos)))

				# Lebenszahl aktualisieren
				self.player.lives -= 1 if self.player.lives > 0 else 0
				self.textLivesNumber.setText(str(self.player.lives))

			# Projektil - Asteroid
			for col2 in self.asteroids[:]:
				if self.colCircle(col1, col2):
					collision = True
					# Explosion
					self.soundExplosion.stop()		# Sound anhalten (falls bereits aktiv)
					self.soundExplosion.play()		# Sound abspielen
					self.explosions.append(Explosion(pygame.Vector2(col2.pos)))

					# Punktzahl aktualisieren
					self.player.score += col2.scorePoints
					self.textScoreNumber.setText(str(self.player.score))

					# Wenn Asteroid groß genug -> kleinere Asteroiden spawnen
					if col2.size != Asteroid.sizeSmall:
						if col2.size == Asteroid.sizeMedium:
							size = Asteroid.sizeSmall
						else:
							size = Asteroid.sizeMedium

						# Zufaellige Anzahl kleinerer Asteroiden spawnen
						for a in range(0, random.randint(1, Game.maxCountSmallerAsteroids)):
							# Zufaelliger Abstand zum vorherigen Asteroiden
							pos = col2.pos + pygame.Vector2(
								random.randrange(-col2.size, col2.size),
								random.randrange(-col2.size, col2.size)
							)

							# Zufaellige Geschwindigkeit
							vel = pygame.Vector2(
								(random.random() - 0.5) * 2 * Asteroid.maxSpeed,
								(random.random() - 0.5) * 2 * Asteroid.maxSpeed
							)

							# Zufaellige Rotationsgeschwindigkeit (normalverteilt, weil schoener)
							rotSpeed = random.uniform(-Asteroid.maxRotSpeed, Asteroid.maxRotSpeed)

							# Asteroid erzeugen
							self.asteroids.append(Asteroid(pos, vel, rotSpeed, size))

					# Asteroid entfernen
					self.asteroids.remove(col2)
					break

			if collision:
				# Projektil entfernen
				self.projectiles.remove(col1)

		# Asteroid - Spieler
		for col in self.asteroids[:]:
			if self.colCircle(col, self.player):
				# Explosion
				self.soundExplosion.stop()  # Sound anhalten (falls bereits aktiv)
				self.soundExplosion.play()  # Sound abspielen
				self.explosions.append(Explosion(pygame.Vector2(self.player.pos)))
				self.explosions.append(Explosion(pygame.Vector2(col.pos)))

				# Asteroid entfernen
				self.asteroids.remove(col)

				# Lebenszahl aktualisieren
				self.player.lives -= 1 if self.player.lives > 0 else 0
				self.textLivesNumber.setText(str(self.player.lives))

		# PowerUp - Spieler
		for (idx, col) in enumerate(self.collectablePowerUps[:]):
			if self.colCircle(col, self.player):
				# PowerUp zu spieler hinzufügen
				col.collectionTime = pygame.time.get_ticks()
				self.soundPowerUp.play()
				self.player.collectPowerUp(col)

				# PowerUp entfernen
				self.collectablePowerUps.remove(col)

		# Game Over
		if self.player.lives == 0:
			self.state = Game.GameStates.over

	def draw(self, screen):
		# Spielfeld schwarz zeichnen
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

		# UI (Score etc.) zeichnen
		for i in self.ui:
			i.draw(screen)
