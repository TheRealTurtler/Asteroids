# https://github.com/Walabot-Projects/Cookie-Guard/blob/c4cffcd49066df540a6981c4d67795b6b6e1c571/sound.py

import pygame


class Sound:

	@staticmethod
	def init(quality = 'low'):
		pygame.mixer.init()  # initialisieren mit Standardwerten (frequency=44100, size=-16, channels=2, buffer=512)

		# pygame.mixer.set_reserved(4)       #soundchannel reservieren vllt. dann wichtig bei mehrerern SFX

	def __init__(self, wav_file):
		# load the sound file
		self.wav_file = wav_file
		self.sound = pygame.mixer.Sound(self.wav_file)
		self.sound.set_volume(0.03)  # Lautstärke [0..1]

	def play(self):
		# play the sound file for 10 seconds and then stop it
		self.sound.play()

	# print(self.wav_file)

	def shutdown(self):
		# Sound nicht mehr verwenden
		self.sound.stop()
		pygame.mixer.quit()
		print('Sound Shutdown')
