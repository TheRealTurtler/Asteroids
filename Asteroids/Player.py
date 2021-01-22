import pygame

#from Vector2D import *

class Player :
	"""description of class"""

	accMax = pygame.Vector2(0.5, 0.5)
	
	#accPerTick = 0.1
	frictionPerTick = 0.02
	rotPerTick = 5

	velMax = pygame.Vector2(3, 3)

	bulletSpawnOffset = 5
	

	def __init__(self) :
		self.pos = pygame.Vector2(0, 0)		    # Position
		self.vel = pygame.Vector2(0, 0)			# Geschwindigkeit
		self.acc = pygame.Vector2(0, 0)			# Beschleunigung
		self.rot = 0							# Rotation

		self.fireRate = 10
		self.timeLastShot = 0

		self.pointOffsets = [
			pygame.Vector2(0, 5),
			pygame.Vector2(-5, -10), 
			pygame.Vector2(0, -5), 
			pygame.Vector2(5, -10)
			]

		self.points = [pygame.Vector2(self.pos + offset) for offset in self.pointOffsets]

		self.bulletSpawn = pygame.Vector2((self.points[0] - self.pos).normalize() * self.bulletSpawnOffset + self.points[0])
		

	def update(self) :
		# Beschleunigung limitieren
		if self.acc.x > self.accMax.x :
			self.acc.x = self.accMax.x
		elif self.acc.x < -self.accMax.x :
			self.acc.x = -self.accMax.x
		elif abs(self.acc.x) < 1e-10 :
			self.acc.x = 0

		if self.acc.y > self.accMax.y :
			self.acc.y = self.accMax.y
		elif self.acc.y < -self.accMax.y :
			self.acc.y = -self.accMax.y
		elif abs(self.acc.y) < 1e-10 :
			self.acc.y = 0

		# Reibung
		if self.acc.x == 0 :
			if self.vel.x > 0 :
				self.acc.x = -self.frictionPerTick
			elif self.vel.x < 0 :
				self.acc.x = self.frictionPerTick

		if self.acc.y == 0 :
			if self.vel.y > 0 :
				self.vel.y -= self.frictionPerTick
			elif self.vel.y < 0 :
				self.vel.y += self.frictionPerTick

		# Beschleunigung -> Geschwindigkeit
		self.vel += self.acc
	
		# Geschwindigkeit limitieren
		if self.vel.x > self.velMax.x :
			self.vel.x = self.velMax.x
		elif self.vel.x < -self.velMax.x :
			self.vel.x = -self.velMax.x
		elif abs(self.vel.x) < 1e-10 :
			self.vel.x = 0

		if self.vel.y > self.velMax.y :
			self.vel.y = self.velMax.y
		elif self.vel.y < -self.velMax.y :
			self.vel.y = -self.velMax.y
		elif abs(self.vel.y) < 1e-10 :
			self.vel.y = 0

		# Geschwindigkeit -> Position
		self.pos += self.vel

		# Rotation
		self.rot %= 360

		for (idx, offset) in enumerate(self.pointOffsets) :
			self.points[idx] = self.pos + offset.rotate(self.rot)

		self.bulletSpawn = pygame.Vector2((self.points[0] - self.pos).normalize() * self.bulletSpawnOffset + self.points[0])


	def draw(self, screen, color = pygame.Color(255, 255, 255)) :
		if type(screen) != pygame.Surface :
			return NotImplemented	# raise TypeError

		if type(color) != pygame.Color :
			return NotImplemented

		pygame.draw.polygon(screen, color, self.points, 1)