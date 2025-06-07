import pygame
import random
from character import Character

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set window title
pygame.display.set_caption("Propositional RPG")

# Game loop variables
running = True
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create player
player = Character(x=50, y=50, size=30, color=GREEN, id='player')

# Create NPCs
npcs = []
npcs.append(Character(x=random.randint(0, SCREEN_WIDTH - 30), y=random.randint(0, SCREEN_HEIGHT - 30), size=30, color=RED, id='npc1'))
npcs.append(Character(x=random.randint(0, SCREEN_WIDTH - 30), y=random.randint(0, SCREEN_HEIGHT - 30), size=30, color=BLUE, id='npc2'))
npcs.append(Character(x=random.randint(0, SCREEN_WIDTH - 30), y=random.randint(0, SCREEN_HEIGHT - 30), size=30, color=YELLOW, id='npc3'))

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x -= player.speed
            if event.key == pygame.K_RIGHT:
                player.x += player.speed
            if event.key == pygame.K_UP:
                player.y -= player.speed
            if event.key == pygame.K_DOWN:
                player.y += player.speed

    # Update player rect
    player.update_rect()

    # Player Boundary checks
    if player.x < 0:
        player.x = 0
    elif player.x > SCREEN_WIDTH - player.size:
        player.x = SCREEN_WIDTH - player.size

    if player.y < 0:
        player.y = 0
    elif player.y > SCREEN_HEIGHT - player.size:
        player.y = SCREEN_HEIGHT - player.size

    player.update_rect() # Update rect again after boundary adjustments

    # NPC movement and boundary checks
    for npc in npcs:
        direction = random.randint(0, 3)
        if direction == 0: # Move left
            npc.x -= npc.speed
        elif direction == 1: # Move right
            npc.x += npc.speed
        elif direction == 2: # Move up
            npc.y -= npc.speed
        elif direction == 3: # Move down
            npc.y += npc.speed

        npc.update_rect()

        # NPC Boundary checks
        if npc.x < 0:
            npc.x = 0
        elif npc.x > SCREEN_WIDTH - npc.size:
            npc.x = SCREEN_WIDTH - npc.size

        if npc.y < 0:
            npc.y = 0
        elif npc.y > SCREEN_HEIGHT - npc.size:
            npc.y = SCREEN_HEIGHT - npc.size

        npc.update_rect() # Update rect again after boundary adjustments

    # Collision detection
    # Player-NPC collisions
    for npc in npcs:
        if player.rect.colliderect(npc.rect):
            print(f"Player met {npc.id}")

    # NPC-NPC collisions
    for i in range(len(npcs)):
        for j in range(i + 1, len(npcs)):
            npc1 = npcs[i]
            npc2 = npcs[j]
            if npc1.rect.colliderect(npc2.rect):
                print(f"{npc1.id} met {npc2.id}")

    # Fill the screen
    screen.fill(BLACK)

    # Draw the player
    player.draw(screen)

    # Draw NPCs
    for npc in npcs:
        npc.draw(screen)

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
