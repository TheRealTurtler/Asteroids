import pygame

from Game import *

pygame.init()

#==============================================================================

screenSize = (640, 480)

game = Game(screenSize)

screen = pygame.display.set_mode(screenSize)

clock = pygame.time.Clock()

#==============================================================================

while game.gameActive :

##### Events abhandeln
	game.handleEvents()

##### Spiellogik
	game.update()

##### Spielfeld löschen
	screen.fill(game.BLACK)

##### Rendern
	game.draw(screen)

##### Fenster aktualisieren
	pygame.display.flip()

##### Refreshrate
	clock.tick(60)
	#clock.tick()

##### FPS Anzeige
	title = "Asteroids" \
		+ f" | Frame Time: {clock.get_rawtime()} ms" \
		+ f" | FPS: {clock.get_fps() : 6.1f}"
	pygame.display.set_caption(title)

# Spiel beenden
pygame.quit()