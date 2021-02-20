import pygame

from PowerUp import PowerUp

class Player:		# TODO make player a Spaceobject
	"""description of class"""
	accMax = 0.4

	# accPerTick = 0.1
	frictionPerTick = 0.02
	rotPerTick = 5

	speedMaxDefault = 2
	fireRateDefault = 10
	projSpeedDefault = 2

	bulletSpawnOffset = 5

	def __init__(self):
		self.pos = pygame.Vector2(0, 0)  # Position
		self.vel = pygame.Vector2(0, 0)  # Geschwindigkeit
		self.acc = pygame.Vector2(0, 0)  # Beschleunigung
		self.rot = 0					 # Rotation
		self.size = 10

		self.speedMax = self.speedMaxDefault
		self.fireRate = self.fireRateDefault
		self.timeLastShot = 0
		self.projSpeed = self.projSpeedDefault

		self.activePowerUps = []

		self.pointOffsets = [
			pygame.Vector2(0, 5),
			pygame.Vector2(-5, -10),
			pygame.Vector2(0, -5),
			pygame.Vector2(5, -10)
		]

		self.points = [pygame.Vector2(self.pos + offset) for offset in self.pointOffsets]

		self.bulletSpawn = pygame.Vector2(
			(self.points[0] - self.pos).normalize() * self.bulletSpawnOffset + self.points[0])

	def update(self):
		# Beschleunigung limitieren
		if self.acc.magnitude() > self.accMax:
			self.acc = self.accMax * self.acc.normalize()

		# "Reibung"
		if self.acc.x == 0:
			if self.vel.x > 0:
				self.acc.x = -self.frictionPerTick
			elif self.vel.x < 0:
				self.acc.x = self.frictionPerTick

		if self.acc.y == 0:
			if self.vel.y > 0:
				self.acc.y -= self.frictionPerTick
			elif self.vel.y < 0:
				self.acc.y += self.frictionPerTick

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
		if abs(self.vel.x) < self.frictionPerTick:
			self.vel.x = 0
		if abs(self.vel.y) < self.frictionPerTick:
			self.vel.y = 0

		# Geschwindigkeit -> Position
		self.pos += self.vel

		# Rotation
		self.rot %= 360

		for (idx, offset) in enumerate(self.pointOffsets):
			self.points[idx] = self.pos + offset.rotate(self.rot)

		self.bulletSpawn = pygame.Vector2(
			(self.points[0] - self.pos).normalize() * self.bulletSpawnOffset + self.points[0])

		# PowerUp-Effekte
		for p in self.activePowerUps[:]:
			# PowerUps nach Ablauf löschen
			if pygame.time.get_ticks() - p.collectionTime > p.duration:
				if p.id == 0:			# Feuerrate
					self.fireRate -= Player.fireRateDefault
				elif p.id == 1:			# Maximalgeschwindigkeit Spieler	# TODO: fix Bug: player faster than projectiles
					self.speedMax -= Player.speedMaxDefault
				elif p.id == 2:			# Projektil-Geschwindigkeit
					self.projSpeed -= Player.projSpeedDefault
				else:
					raise LookupError

				self.activePowerUps.remove(p)

	def draw(self, screen, color=pygame.Color(255, 255, 255)):
		if type(screen) != pygame.Surface:
			raise TypeError

		if type(color) != pygame.Color:
			raise TypeError

		pygame.draw.polygon(screen, color, self.points, 1)
		pygame.draw.circle(screen, pygame.Color(255, 0, 0), self.pos, self.size, 1)

	def collectPowerUp(self, powerUp):
		if type(powerUp) != PowerUp:
			raise TypeError

		self.activePowerUps.append(powerUp)

		if powerUp.id == 0:			# Feuerrate
			self.fireRate += Player.fireRateDefault
		elif powerUp.id == 1:		# Maximalgeschwindigkeit Spieler	# TODO: fix Bug: player faster than projectiles
			self.speedMax += Player.speedMaxDefault
		elif powerUp.id == 2:		# Projektil-Geschwindigkeit
			self.projSpeed += Player.projSpeedDefault
		else:
			raise LookupError

		print("PowerUp collected!")
		print(powerUp.collectionTime)