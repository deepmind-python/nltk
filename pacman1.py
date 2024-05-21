import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
CELL_SIZE = 20
GRID_WIDTH = 28
GRID_HEIGHT = 31
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pac-Man')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Map
map_data = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#@####.#####.##.#####.####@#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "######.##### ## #####.######",
    "######.##          ##.######",
    "######.## ######## ##.######",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#@..##................##..@#",
    "###.##.##.########.##.##.###",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#.##########.##.##########.#",
    "#..........................#",
    "############################"
]

# Pac-Man initial position
pacman_pos = [14, 23]

# Ghost positions
ghost_positions = [[1, 1], [26, 1], [1, 23], [26, 23]]

# Functions to draw the grid and characters
def draw_grid():
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == '@':
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == '.':
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 3)

def draw_pacman(x, y):
    pygame.draw.circle(screen, YELLOW, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

def draw_ghosts():
    for ghost in ghost_positions:
        pygame.draw.circle(screen, RED, (ghost[0] * CELL_SIZE + CELL_SIZE // 2, ghost[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pacman_pos[0] -= 1
    if keys[pygame.K_RIGHT]:
        pacman_pos[0] += 1
    if keys[pygame.K_UP]:
        pacman_pos[1] -= 1
    if keys[pygame.K_DOWN]:
        pacman_pos[1] += 1

    # Ensure Pac-Man stays within the grid
    pacman_pos[0] = max(0, min(GRID_WIDTH - 1, pacman_pos[0]))
    pacman_pos[1] = max(0, min(GRID_HEIGHT - 1, pacman_pos[1]))

    # Drawing
    screen.fill(BLACK)
    draw_grid()
    draw_pacman(pacman_pos[0], pacman_pos[1])
    draw_ghosts()
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
