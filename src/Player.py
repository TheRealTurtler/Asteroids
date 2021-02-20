import pygame


class Player:		# TODo make player a Spaceobject
	"""description of class"""
	accMax = 0.4

	# accPerTick = 0.1
	frictionPerTick = 0.02
	rotPerTick = 5

	speedMaxDefault = 2
	speedMax = speedMaxDefault

	bulletSpawnOffset = 5

	def __init__(self):
		self.pos = pygame.Vector2(0, 0)  # Position
		self.vel = pygame.Vector2(0, 0)  # Geschwindigkeit
		self.acc = pygame.Vector2(0, 0)  # Beschleunigung
		self.rot = 0					 # Rotation
		self.size = 10


		self.fireRateDefault = 10
		self.fireRate = self.fireRateDefault
		self.timeLastShot = 0

		self.timeItemStart = 0

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

		# Reibung
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

		# Beschleunigung -> Geschwindigkeit
		self.vel += self.acc

		# Untergrenze Beschleunigung
		if abs(self.acc.x) < 1e-5:
			self.acc.x = 0
		if abs(self.acc.y) < 1e-5:
			self.acc.y = 0

		# Geschwindigkeit limitieren
		if self.vel.magnitude() > self.speedMax:
			self.vel = self.speedMax * self.vel.normalize()

		# Geschwindigkeit -> Position
		self.pos += self.vel

		# Untergrenze Geschwindigleit
		if abs(self.vel.x) < self.frictionPerTick:
			self.vel.x = 0
		if abs(self.vel.y) < self.frictionPerTick:
			self.vel.y = 0

		# Rotation
		self.rot %= 360

		for (idx, offset) in enumerate(self.pointOffsets):
			self.points[idx] = self.pos + offset.rotate(self.rot)

		self.bulletSpawn = pygame.Vector2(
			(self.points[0] - self.pos).normalize() * self.bulletSpawnOffset + self.points[0])

	def drawPoly(self, screen, color=pygame.Color(255, 255, 255)):
		if type(screen) != pygame.Surface:
			raise TypeError

		if type(color) != pygame.Color:
			raise TypeError

		pygame.draw.polygon(screen, color, self.points, 1)
		pygame.draw.circle(screen, pygame.Color(255, 0, 0), self.pos, self.size, 1)
