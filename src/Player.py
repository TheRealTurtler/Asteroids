import pygame

from src.PowerUp import PowerUp
from src.Color import Color
from src.Boost import Boost


# Spieler ist mit Absicht kein Space Object, da dies die Beschleunigungs- und Reibungsrechnung unnoetig
# verkomplizieren wuerde
class Player:
	# Maximalbeschleunigung
	accMax = 0.25

	# Reibung
	frictionPerTick = 0.02

	# Rotationsgeschwindigkeit
	rotPerTick = 5

	# Standardwerte
	speedMaxDefault = 1.5
	fireRateDefault = 5
	projSpeedDefault = 2.5

	# Projektil- und Boost-Offsets
	bulletSpawnOffset = 5
	boostPointOffset = 5

	def __init__(self, pos = pygame.Vector2(0, 0)):
		if type(pos) != pygame.Vector2:
			raise TypeError

		self.pos = pos								# Position
		self.vel = pygame.Vector2(0, 0)				# Geschwindigkeit
		self.acc = pygame.Vector2(0, 0)				# Beschleunigung
		self.rot = 0								# Rotation
		self.size = 12								# Groesse der Hit-"box" (Kreis)
		self.lookDir = pygame.Vector2(0, -1)		# Blickrichtung

		self.speedMax = self.speedMaxDefault		# Maximalgeschwindigkeit
		self.fireRate = self.fireRateDefault		# Feuerrate
		self.timeLastShot = 0						# Zeit des letzten Schusses
		self.projSpeed = self.projSpeedDefault		# Projektilgeschwindigkeit

		# Eingesammelte PowerUps
		self.activePowerUps = []

		# Polygonpunkte relativ zur Spielerposition (Mitte)
		self.polygonPointOffsets = [
			pygame.Vector2(0, -15),
			pygame.Vector2(-9, 12),
			pygame.Vector2(0, 6),
			pygame.Vector2(9, 12)
		]

		# Polygonpunkte absolut
		self.polygonPoints = [pygame.Vector2(self.pos + offset) for offset in self.polygonPointOffsets]

		# Spawnpunkte der Projektile
		self.bulletSpawnPoints = [self.lookDir * Player.bulletSpawnOffset + self.polygonPoints[0]]
		self.bulletAmount = 1

		# Boost
		self.boostActive = False
		self.boost = Boost()
		self.boostPoint = -1 * self.lookDir * Player.boostPointOffset + self.polygonPoints[2]

		# Punkte und Leben
		self.score = 0
		self.lives = 5

	def collectPowerUp(self, powerUp):
		if type(powerUp) != PowerUp:
			raise TypeError

		self.activePowerUps.append(powerUp)

		if powerUp.id == PowerUp.PowerUpIDs.fireRate:				# Feuerrate
			self.fireRate += Player.fireRateDefault
		elif powerUp.id == PowerUp.PowerUpIDs.maxSpeed:				# Maximalgeschwindigkeit Spieler
			self.speedMax += Player.speedMaxDefault					# (Spieler kann schneller werden als Projektile -> Feature? :) )
		elif powerUp.id == PowerUp.PowerUpIDs.projectileSpeed:		# Projektil-Geschwindigkeit
			self.projSpeed += Player.projSpeedDefault
		elif powerUp.id == PowerUp.PowerUpIDs.multiShot:			# Multi-Schuss
			self.bulletAmount += 1

	def update(self):
		# Beschleunigung limitieren
		if self.acc.magnitude() > Player.accMax:
			self.acc = Player.accMax * self.acc.normalize()

		# "Reibung"
		# (ja, uns ist bewusst dass es im Vakuum keine Reibung gibt, aber die Steuerung ist so schoener :) )
		if self.acc.x == 0:
			if self.vel.x > 0:
				self.acc.x = -Player.frictionPerTick
			elif self.vel.x < 0:
				self.acc.x = Player.frictionPerTick

		if self.acc.y == 0:
			if self.vel.y > 0:
				self.acc.y -= Player.frictionPerTick
			elif self.vel.y < 0:
				self.acc.y += Player.frictionPerTick

		# Untergrenze Beschleunigung
		# (damit float Werte mit == 0 verglichen werden koennen;
		# ausserdem ist eine Bewegung von 1e-6 Pixel pro Bild unsinnig)
		if abs(self.acc.x) < 1e-6:
			self.acc.x = 0
		if abs(self.acc.y) < 1e-6:
			self.acc.y = 0

		# Beschleunigung -> Geschwindigkeit
		self.vel += self.acc

		# Geschwindigkeit limitieren
		if self.vel.magnitude() > self.speedMax:
			self.vel = self.speedMax * self.vel.normalize()

		# Untergrenze Geschwindigleit
		if abs(self.vel.x) < Player.frictionPerTick:
			self.vel.x = 0
		if abs(self.vel.y) < Player.frictionPerTick:
			self.vel.y = 0

		# Geschwindigkeit -> Position
		self.pos += self.vel

		# Rotation
		self.rot %= 360

		# Position der Polygonpunkte neu berechnen
		for (idx, offset) in enumerate(self.polygonPointOffsets):
			self.polygonPoints[idx] = self.pos + offset.rotate(self.rot)

		# Position der Projektil-Spawnpunkte neu berechnen
		self.bulletSpawnPoints = []
		self.lookDir = (self.polygonPoints[0] - self.pos).normalize()

		bulletStartPos = 1

		# ungerade Anzahl Kugeln
		if self.bulletAmount % 2:
			bulletStartPos = 0

		for b in range(bulletStartPos, self.bulletAmount, 2):
			self.bulletSpawnPoints.append(
				self.lookDir * Player.bulletSpawnOffset
				+ self.polygonPoints[0]
				+ pygame.Vector2(self.lookDir.y, -self.lookDir.x) * Player.bulletSpawnOffset * b
			)

			if b > 0:
				self.bulletSpawnPoints.append(
					self.lookDir * Player.bulletSpawnOffset
					+ self.polygonPoints[0]
					+ pygame.Vector2(-self.lookDir.y, self.lookDir.x) * Player.bulletSpawnOffset * b
				)

		# Boost Position neu berechnen
		self.boostPoint = -1 * self.lookDir * Player.boostPointOffset + self.polygonPoints[2]

		# PowerUp-Effekte
		for p in self.activePowerUps[:]:
			# PowerUps nach Ablauf entfernen
			if pygame.time.get_ticks() - p.collectionTime > p.duration:
				if p.id == PowerUp.PowerUpIDs.fireRate:					# Feuerrate
					self.fireRate -= Player.fireRateDefault
				elif p.id == PowerUp.PowerUpIDs.maxSpeed:				# Maximalgeschwindigkeit Spieler
					self.speedMax -= Player.speedMaxDefault
				elif p.id == PowerUp.PowerUpIDs.projectileSpeed:		# Projektil-Geschwindigkeit
					self.projSpeed -= Player.projSpeedDefault
				elif p.id == PowerUp.PowerUpIDs.multiShot:				# Multi-Schuss
					self.bulletAmount -= 1

				self.activePowerUps.remove(p)

		# Boost Partikel
		if self.boostActive:
			self.boost.boost(self.boostPoint, -1 * self.lookDir)

		# Boost aktualisieren
		self.boost.update()

	def draw(self, screen, color = Color.WHITE):
		if type(screen) != pygame.Surface:
			raise TypeError

		if type(color) != pygame.Color:
			raise TypeError

		# Spieler zeichnen
		pygame.draw.polygon(screen, color, self.polygonPoints, 2)

		# Boost zeichnen
		self.boost.draw(screen)
