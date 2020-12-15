import pygame
import math

pygame.init()

#==============================================================================

class Vector2D :
    x = 0
    y = 0

    def magnitude(self) :
        return math.sqrt(self.x**2 + self.y**2)

class Player :
    pos = Vector2D()        # Position
    rot = 0                 # Rotation
    vel = Vector2D()        # Geschwindigkeit
    acc = Vector2D()        # Beschleunigung

class Asteroid :
    pos = Vector2D()
    rot = 0
    vel = Vector2D()

#==============================================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
accMax.x = 1
accMax.y = 1

accPerTick = 0.1

velMax = Vector2D()
velMax.x = 3
velMax.y = 3

frictionPerTick = 0.1

pressed_W = False
pressed_A = False
pressed_S = False
pressed_D = False

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

        # Mouse button pressed
        #elif event.type == pygame.MOUSEBUTTONDOWN :

##### Spiellogik
    print(player.pos.x, player.pos.y, player.vel.x, player.vel.y, player.acc.x, player.acc.y, pressed_W, pressed_A, pressed_S, pressed_D)

    # Beschleunigung erhöhen
    if pressed_W :
        if player.acc.y > -accMax.y :
            player.acc.y -= accPerTick
    if pressed_A :
        if player.acc.x > -accMax.x :
            player.acc.x -= accPerTick
    if pressed_S :
        if player.acc.y < accMax.y :
            player.acc.y += accPerTick
    if pressed_D :
        if player.acc.x < accMax.x :
            player.acc.x += accPerTick

    # Beschleunigung reduzieren
    if not pressed_W :
        if player.acc.y < 0 :
            player.acc.y += accPerTick
            if player.acc.y > 0:
                player.acc.y = 0

    if not pressed_A :
        if player.acc.x < 0 :
            player.acc.x += accPerTick
            if player.acc.x > 0:
                player.acc.x = 0

    if not pressed_S :
        if player.acc.y > 0 :
            player.acc.y -= accPerTick
            if player.acc.y < 0:
                player.acc.y = 0

    if not pressed_D :
        if player.acc.x > 0 :
            player.acc.x -= accPerTick
            if player.acc.x < 0:
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

    # Beschleunigung -> Geschwindigkeit
    player.vel.x += player.acc.x
    player.vel.y += player.acc.y

    if player.acc.y == 0 :
        if player.vel.y > 0 :
            player.vel.y -= frictionPerTick
        elif player.vel.y < 0 :
            player.vel.y += frictionPerTick
    
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
    player.pos.x += player.vel.x
    player.pos.y += player.vel.y
    
    # Spielfeldrand verlassen -> auf ggegenüberliegender Seite weiter
    if player.pos.x < 0 :
        player.pos.x = screenSize[0]
    elif player.pos.x > screenSize[0] :
        player.pos.x = 0

    if player.pos.y < 0 :
        player.pos.y = screenSize[1]
    elif player.pos.y > screenSize[1] :
        player.pos.y = 0

##### Spielfeld löschen
    screen.fill(BLACK)

##### Rendern
    pygame.draw.rect(screen, WHITE, [player.pos.x - 10, player.pos.y - 10, 20, 20], 1)

##### Fenster aktualisieren
    pygame.display.flip()

##### Refreshrate
    clock.tick(60)

# Spiel beenden
pygame.quit()