# Erstellt mit Hilfe von:
# https://github.com/Walabot-Projects/Cookie-Guard/blob/c4cffcd49066df540a6981c4d67795b6b6e1c571/sound.py

import pygame


class Sound:
	@staticmethod
	def init(quality = 'low'):
		pygame.mixer.init()		# Initialisierung mit Standardwerten (frequency=44100, size=-16, channels=2, buffer=512)

	def __init__(self, wav_file, volume):
		if type(wav_file) != str:
			raise TypeError

		if type(volume) not in (int, float):
			raise TypeError

		if volume < 0 or volume > 1:
			raise ValueError

		# Sounddatei laden
		self.wav_file = wav_file
		self.sound = pygame.mixer.Sound(self.wav_file)
		self.sound.set_volume(volume)		# Lautstärke [0..1]

	def play(self):
		# Sound abspielen
		self.sound.play()

	def stop(self):
		# Sound anhalten
		self.sound.stop()

	def shutdown(self):
		# Sound nicht mehr verwenden
		self.sound.stop()
		pygame.mixer.quit()
		print('Sound Shutdown')
