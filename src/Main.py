import pygame

from Game import Game
from Color import Color
from Menu import Menu

pygame.init()

# ==============================================================================

screenSize = (1280, 720)

menu = Menu(screenSize)
game = Game(screenSize)

screen = pygame.display.set_mode(screenSize)

clock = pygame.time.Clock()

windowActive = True

# ==============================================================================

while windowActive:
	# Events abhandeln
	game.handleEvents()

	if menu.active:
		# Menü zeichnen
		menu.draw(screen)
	elif game.active:
		# Spiellogik
		game.update()

		# Rendern
		game.draw(screen)

	# Fenster aktualisieren
	pygame.display.flip()

	# Refreshrate
	clock.tick(60)
	# clock.tick()

	# FPS Anzeige
	title = "Asteroids" \
			+ f" | Frame Time: {clock.get_rawtime()} ms" \
			+ f" | FPS: {clock.get_fps() : 6.1f}"
	pygame.display.set_caption(title)

# Spiel beenden
pygame.quit()
