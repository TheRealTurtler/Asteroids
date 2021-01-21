import pygame
import math

from Vector2D import Vector2D
from Player import Player
from Asteroid import Asteroid
from Projectile import Projectile

pygame.init()

#==============================================================================

WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

#==============================================================================

player = Player()

player.pos.x = 100
player.pos.y = 100

screenSize = (640, 480)

screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Asteroids")

clock = pygame.time.Clock()

gameActive = True

accMax = Vector2D()
accMax.x = 0.5
accMax.y = 0.5

accPerTick = 0.1

velMax = Vector2D()
velMax.x = 3
velMax.y = 3

frictionPerTick = 0.02

pressed_W = False
pressed_A = False
pressed_S = False
pressed_D = False
pressed_Space = False

projectiles = []

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
		player.acc.y = -accMax.y
	if pressed_A and not pressed_D :
		player.acc.x = -accMax.x
	if pressed_S and not pressed_W :
		player.acc.y = accMax.y
	if pressed_D and not pressed_A :
		player.acc.x = accMax.x

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

	# Beschleunigung limitieren
	if player.acc.x > accMax.x :
		player.acc.x = accMax.x
	elif player.acc.x < -accMax.x :
		player.acc.x = -accMax.x
	elif abs(player.acc.x) < 1e-10 :
		player.acc.x = 0

	if player.acc.y > accMax.y :
		player.acc.y = accMax.y
	elif player.acc.y < -accMax.y :
		player.acc.y = -accMax.y
	elif abs(player.acc.y) < 1e-10 :
		player.acc.y = 0

	# Reibung
	if player.acc.x == 0 :
		if player.vel.x > 0 :
			player.acc.x = -frictionPerTick
		elif player.vel.x < 0 :
			player.acc.x = frictionPerTick

	if player.acc.y == 0 :
		if player.vel.y > 0 :
			player.vel.y -= frictionPerTick
		elif player.vel.y < 0 :
			player.vel.y += frictionPerTick

	# Beschleunigung -> Geschwindigkeit
	player.vel += player.acc
	
	# Geschwindigkeit limitieren
	if player.vel.x > velMax.x :
		player.vel.x = velMax.x
	elif player.vel.x < -velMax.x :
		player.vel.x = -velMax.x
	elif abs(player.vel.x) < 1e-10 :
		player.vel.x = 0

	if player.vel.y > velMax.y :
		player.vel.y = velMax.y
	elif player.vel.y < -velMax.y :
		player.vel.y = -velMax.y
	elif abs(player.vel.y) < 1e-10 :
		player.vel.y = 0

	# Geschwindigkeit -> Position
	player.pos += player.vel
	
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
	pygame.draw.rect(screen, WHITE, [player.pos.x - 10, player.pos.y - 10, 20, 20], 1)
	
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