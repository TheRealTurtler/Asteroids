import pygame

from Vector2D import *

class Player :
	"""description of class"""

	accMax = Vector2D(0.5, 0.5)
	
	#accPerTick = 0.1
	frictionPerTick = 0.02

	velMax = Vector2D(3, 3)
	

	def __init__(self) :
		self.pos = Vector2D()        # Position
		self.rot = 0                 # Rotation
		self.vel = Vector2D()        # Geschwindigkeit
		self.acc = Vector2D()        # Beschleunigung

		self.fireRate = 10
		self.timeLastShot = 0

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

	def draw(self, screen, color = pygame.Color(255, 255, 255)) :
		if type(screen) != pygame.Surface :
			return NotImplemented

		if type(color) != pygame.Color :
			return NotImplemented

		pygame.draw.polygon(
			screen, 
			color, 
			[
			(self.pos.x + 0, self.pos.y + 0),
			(self.pos.x - 5, self.pos.y - 15), 
			(self.pos.x + 0, self.pos.y - 10), 
			(self.pos.x + 5, self.pos.y - 15)
			],
			1)