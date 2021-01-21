import pygame

from Game import *

pygame.init()

#==============================================================================

screenSize = (640, 480)

game = Game(screenSize)

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

pygame.mixer.music.play(-1)		# Spiele tetris theme ab auf loop (-1)

#==============================================================================

while game.gameActive :

##### Events abhandeln
	game.handleEvents()

##### Spiellogik
	print(game.player.pos, game.player.vel, game.player.acc, game.pressed_W, game.pressed_A, game.pressed_S, game.pressed_D)
	#print(len(projectiles))

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