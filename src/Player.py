import pygame

from src.PowerUp import PowerUp


class Player:
	accMax = 0.25

	# accPerTick = 0.1
	frictionPerTick = 0.02
	rotPerTick = 5

	speedMaxDefault = 1.5
	fireRateDefault = 5
	projSpeedDefault = 2.5

	bulletSpawnOffset = 5

	def __init__(self):
		self.pos = pygame.Vector2(0, 0)  # Position
		self.vel = pygame.Vector2(0, 0)  # Geschwindigkeit
		self.acc = pygame.Vector2(0, 0)  # Beschleunigung
		self.rot = 0					 # Rotation
		self.size = 12
		self.lookDir = pygame.Vector2(0, -1)		# Blickrichtung

		self.speedMax = self.speedMaxDefault
		self.fireRate = self.fireRateDefault
		self.timeLastShot = 0
		self.projSpeed = self.projSpeedDefault

		self.activePowerUps = []

		self.pointOffsets = [
			pygame.Vector2(0, -15),
			pygame.Vector2(-9, 12),
			pygame.Vector2(0, 6),
			pygame.Vector2(9, 12)
		]

		# TODO: center player in hit-circle
		self.polygonPoints = [pygame.Vector2(self.pos + offset) for offset in self.pointOffsets]

		self.bulletSpawnPoints = [self.lookDir * self.bulletSpawnOffset + self.polygonPoints[0]]
		self.bulletAmount = 1

		self.score = 0
		self.lives = 5

	def update(self):
		# Beschleunigung limitieren
		if self.acc.magnitude() > Player.accMax:
			self.acc = Player.accMax * self.acc.normalize()

		# "Reibung"
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

		for (idx, offset) in enumerate(self.pointOffsets):
			self.polygonPoints[idx] = self.pos + offset.rotate(self.rot)

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

		# PowerUp-Effekte
		for p in self.activePowerUps[:]:

			# PowerUps nach Ablauf löschen
			if pygame.time.get_ticks() - p.collectionTime > p.duration:
				if p.id == PowerUp.PowerUpIDs.fireRate:					# Feuerrate
					self.fireRate -= Player.fireRateDefault
				elif p.id == PowerUp.PowerUpIDs.maxSpeed:				# Maximalgeschwindigkeit Spieler	# TODO: fix Bug: player faster than projectiles
					self.speedMax -= Player.speedMaxDefault
				elif p.id == PowerUp.PowerUpIDs.projectileSpeed:		# Projektil-Geschwindigkeit
					self.projSpeed -= Player.projSpeedDefault
				elif p.id == PowerUp.PowerUpIDs.multiShot:				# Multi-Schuss
					self.bulletAmount -= 1

				self.activePowerUps.remove(p)

	def draw(self, screen, color=pygame.Color(255, 255, 255)):
		if type(screen) != pygame.Surface:
			raise TypeError

		if type(color) != pygame.Color:
			raise TypeError

		pygame.draw.polygon(screen, color, self.polygonPoints, 2)
		# pygame.draw.circle(screen, pygame.Color(255, 0, 0), self.pos, self.size, 1)

	def collectPowerUp(self, powerUp):
		if type(powerUp) != PowerUp:
			raise TypeError

		self.activePowerUps.append(powerUp)

		if powerUp.id == PowerUp.PowerUpIDs.fireRate:				# Feuerrate
			self.fireRate += Player.fireRateDefault
		elif powerUp.id == PowerUp.PowerUpIDs.maxSpeed:				# Maximalgeschwindigkeit Spieler	# TODO: fix Bug: player faster than projectiles
			self.speedMax += Player.speedMaxDefault
		elif powerUp.id == PowerUp.PowerUpIDs.projectileSpeed:		# Projektil-Geschwindigkeit
			self.projSpeed += Player.projSpeedDefault
		elif powerUp.id == PowerUp.PowerUpIDs.multiShot:			# Multi-Schuss
			self.bulletAmount += 1
