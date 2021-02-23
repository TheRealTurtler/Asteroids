import pygame


class Text:
	def __init__(self, pos = pygame.Vector2(0, 0), text = "", size = 32, color = pygame.Color(255, 255, 255)):
		if type(pos) != pygame.Vector2:
			raise TypeError

		if type(text) != str:
			raise TypeError

		if type(size) != int:
			raise TypeError

		if type(color) != pygame.Color:
			raise TypeError

		if pygame.font.get_init() == 0:
			print("Font module not initialized!")
			print("Initializing now...")
			pygame.font.init()

		self.pos = pos
		self.size = size
		self.color = color

		# https://www.dafont.com/retro-gaming.font
		self.font = pygame.font.Font("./resources/Retro_Gaming.ttf", self.size)
		self.img = self.font.render(text, True, self.color)

	def width(self):
		return self.img.get_width()

	def height(self):
		return self.img.get_height()

	def setText(self, text):
		if type(text) != str:
			raise TypeError

		self.img = self.font.render(text, True, self.color)

	def update(self):
		pass

	def draw(self, screen):
		if type(screen) != pygame.Surface:
			raise TypeError

		screen.blit(self.img, self.pos)
