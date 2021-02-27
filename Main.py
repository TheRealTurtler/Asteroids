import pygame

from src.EventHandler import EventHandler
from src.Menu import Menu
from src.Game import Game
from src.Highscores import Highscores
from src.GameOver import GameOver

# Pygame initialisieren
pygame.init()

# ==============================================================================

screenSize = (1280, 720)
screen = pygame.display.set_mode(screenSize)

eventHandler = EventHandler()
highscores = Highscores("./resources/highscores.dat")
menu = Menu(screenSize, eventHandler)
game = Game(screenSize, eventHandler, highscores.highscore)
gameOver = GameOver(screenSize, eventHandler)

clock = pygame.time.Clock()

# ==============================================================================

while eventHandler.windowActive:
	# Events abhandeln
	eventHandler.handleEvents()

	if eventHandler.pressed_Esc:
		highscores.active = False
		gameOver.active = False
		game.state = Game.GameStates.inactive
		menu.reload()

	if menu.active:
		# Menue aktualisieren
		menu.update()

		# Menueauswahl
		if menu.selection == Menu.MenuSelection.resumeGame:
			game.resume()
		elif menu.selection == Menu.MenuSelection.startNewGame:
			# Spiel neu starten
			# Nicht ideal, besser waere das vorhandene Game Objekt auf einen Ausgangszustand zurueckzusetzen
			# TODO: better restart
			game = Game(screenSize, eventHandler, highscores.highscore)
			game.state = Game.GameStates.active
		elif menu.selection == Menu.MenuSelection.highscores:
			highscores.active = True
		elif menu.selection == Menu.MenuSelection.quit:
			eventHandler.windowActive = False

		# Menue zeichnen
		menu.draw(screen)

	elif highscores.active:
		# Highscores
		highscores.draw(screen)

	elif game.state == Game.GameStates.active:
		# Spiellogik
		game.update()

		# Rendern
		game.draw(screen)

	elif game.state == Game.GameStates.over:
		# Game Over -> Score mit Highscores vergleichen
		if highscores.addScore(game.player.score):
			gameOver.newHighscore(game.player.score)
		else:
			gameOver.newHighscore(False)

		game.state = Game.GameStates.inactive
		gameOver.active = True

	elif game.state == Game.GameStates.ended:
		# Game Over -> Score nicht mit Highscores vergleichen
		game.state = Game.GameStates.inactive
		gameOver.active = True

	elif gameOver.active:
		# Game Over Screen
		if pygame.time.get_ticks() - gameOver.timeUpdated > GameOver.displayDelay and eventHandler.pressed_Any:
			gameOver.active = False
			menu.reload()

		gameOver.draw(screen)

	# Fenster aktualisieren
	pygame.display.flip()

	# Refreshrate
	clock.tick(60)

	# FPS Anzeige
	title = "Asteroids" \
			+ f" | Frame Time: {clock.get_rawtime()} ms" \
			+ f" | FPS: {clock.get_fps() : 6.1f}"
	pygame.display.set_caption(title)

# Spiel beenden
pygame.quit()
