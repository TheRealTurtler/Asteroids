import pygame
import math

from Vector2D import Vector2D
from Player import Player
from Asteroid import Asteroid
from Projectile import Projectile
from Sound import Sound

pygame.init()

#==============================================================================

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

#==============================================================================
#Sound Einstellungen
lasergun_wav = r'lasergun.wav'	#Laser pew sound lesen

Sound.init()					#initialisieren von pygame.mixer

gunsound=Sound(lasergun_wav)	#Instanz gunsound der Klasse Sound hat nun Laser pew sound

pygame.mixer.music.load('Tetris.wav')	#Hintergrundmusik ist Tetristheme in pygame.music (keine Klasse da nur eine Hmusik)
pygame.mixer.music.set_volume(0.03)		#leiser machen
#==============================================================================

player = Player()

player.pos.x = 100
player.pos.y = 100

screenSize = (640, 480)

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

gameActive = True

pressed_W = False
pressed_A = False
pressed_S = False
pressed_D = False
pressed_Space = False

projectiles = []

pygame.mixer.music.play(-1)		#Spiele tetris theme ab auf loop (-1)

while gameActive :

##### Events abhandeln
	for event in pygame.event.get() :

		# Game quit
		if event.type == pygame.QUIT :
			gameActive = False

		# Key pressed
		elif event.type == pygame.KEYDOWN :
			if event.key == pygame.K_w :
				pressed_W = True
			elif event.key == pygame.K_a :
				pressed_A = True
			elif event.key == pygame.K_s :
				pressed_S = True
			elif event.key == pygame.K_d :
				pressed_D = True
			elif event.key == pygame.K_SPACE :
				pressed_Space = True

		# Key released
		elif event.type == pygame.KEYUP :
			if event.key == pygame.K_w :
				pressed_W = False
			elif event.key == pygame.K_a :
				pressed_A = False
			elif event.key == pygame.K_s :
				pressed_S = False
			elif event.key == pygame.K_d :
				pressed_D = False
			elif event.key == pygame.K_SPACE :
				pressed_Space = False

		# Mouse button pressed
		#elif event.type == pygame.MOUSEBUTTONDOWN :

##### Spiellogik
	print(player.pos, player.vel, player.acc, pressed_W, pressed_A, pressed_S, pressed_D)
	#print(len(projectiles))

	# Beschleunigung erhöhen
	#if pressed_W :
	#    if player.acc.y > -accMax.y :
	#        player.acc.y -= accPerTick
	#if pressed_A :
	#    if player.acc.x > -accMax.x :
	#        player.acc.x -= accPerTick
	#if pressed_S :
	#    if player.acc.y < accMax.y :
	#        player.acc.y += accPerTick
	#if pressed_D :
	#    if player.acc.x < accMax.x :
	#        player.acc.x += accPerTick

	if pressed_W and not pressed_S :
		player.acc.y = -player.accMax.y
	if pressed_A and not pressed_D :
		player.acc.x = -player.accMax.x
	if pressed_S and not pressed_W :
		player.acc.y = player.accMax.y
	if pressed_D and not pressed_A :
		player.acc.x = player.accMax.x

	# Beschleunigung reduzieren
	#if not pressed_W :
	#    if player.acc.y < 0 :
	#        player.acc.y += accPerTick
	#        if player.acc.y > 0:
	#            player.acc.y = 0

	#if not pressed_A :
	#    if player.acc.x < 0 :
	#        player.acc.x += accPerTick
	#        if player.acc.x > 0:
	#            player.acc.x = 0

	#if not pressed_S :
	#    if player.acc.y > 0 :
	#        player.acc.y -= accPerTick
	#        if player.acc.y < 0:
	#            player.acc.y = 0

	#if not pressed_D :
	#    if player.acc.x > 0 :
	#        player.acc.x -= accPerTick
	#        if player.acc.x < 0:
	#            player.acc.x = 0

	if pressed_W == pressed_S :
		player.acc.y = 0

	if pressed_A == pressed_D :
		player.acc.x = 0

	player.update()
	
	# Spielfeldrand verlassen -> auf ggegenüberliegender Seite weiter
	if player.pos.x < 0 :
		player.pos.x = screenSize[0]
	elif player.pos.x > screenSize[0] :
		player.pos.x = 0

	if player.pos.y < 0 :
		player.pos.y = screenSize[1]
	elif player.pos.y > screenSize[1] :
		player.pos.y = 0

	# Projektile
	if pressed_Space :
		#lasergun pew sound
		gunsound.play()	
		
		projectiles.append(Projectile(player.pos, Vector2D(0, 2)))


	for p in projectiles[:] :
		p.update()
		
		if p.pos.x < 0 :
			p.pos.x = screenSize[0]
			p.wrap += 1
		elif p.pos.x > screenSize[0] :
			p.pos.x = 0
			p.wrap += 1

		if p.pos.y < 0 :
			p.pos.y = screenSize[1]
			p.wrap += 1
		elif p.pos.y > screenSize[1] :
			p.pos.y = 0
			p.wrap += 1

		if p.wrap > p.maxWrap :
			projectiles.remove(p)
			

##### Spielfeld löschen
	screen.fill(BLACK)

##### Rendern
	#pygame.draw.rect(screen, WHITE, [player.pos.x - 10, player.pos.y - 10, 20, 20], 1)
	pygame.draw.polygon(screen, WHITE, [(player.pos.x+10,player.pos.y+10),(player.pos.x+10,player.pos.y-10),(player.pos.x-10,player.pos.y-10),(player.pos.x-10,player.pos.y+10)],1)

	for p in projectiles :
		p.draw(screen, WHITE)

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