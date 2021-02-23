import pygame

from EventHandler import EventHandler
from Menu import Menu
from Game import Game

pygame.init()

# ==============================================================================

screenSize = (1280, 720)

eventHandler = EventHandler()
menu = Menu(screenSize, eventHandler)
game = Game(screenSize, eventHandler)

screen = pygame.display.set_mode(screenSize)

clock = pygame.time.Clock()

# ==============================================================================

while eventHandler.windowActive:
	# Events abhandeln
	eventHandler.handleEvents()

	if eventHandler.pressed_Esc:
		game.active = False
		menu.reload()

	if menu.active:
		# Menü aktualisieren
		menu.update()

		# Menüauswahl
		if menu.selection == Menu.MenuSelection.resumeGame:
			game.active = True
			game.resume()
		elif menu.selection == Menu.MenuSelection.startNewGame:
			# Spiel neu starten
			# Nicht ideal, besser wäre das vorhandene Game Objekt auf einen Ausganszustand zurückzusetzen
			# TODO: better restart
			game = Game(screenSize, eventHandler)
			game.active = True
		elif menu.selection == Menu.MenuSelection.highscores:
			# TODO: Highscores
			pass
		elif menu.selection == Menu.MenuSelection.quit:
			eventHandler.windowActive = False

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
