import pygame
import sys
import random

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

# Ghost positions and directions
ghost_positions = [[1, 1], [26, 1], [1, 23], [26, 23]]
ghost_directions = [[0, 0], [0, 0], [0, 0], [0, 0]]
ghost_pause_timer = [0, 0, 0, 0]  # Timers to control ghost pause after collision

# Intransitive and transitive verbs
intransitive_verbs = ["I cry.", "I laugh.", "I jump.", "I sleep.", "I run."]
transitive_verbs = ["I eat you.", "I catch you.", "I see you.", "I chase you.", "I find you."]

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

# Check for collisions
def check_collision(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

# Function to display text
def display_text(text, position, color=WHITE):
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Game loop
running = True
clock = pygame.time.Clock()
message = None
message_timer = 0
message_duration = 2000  # Default duration for intransitive verbs

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and map_data[pacman_pos[1]][pacman_pos[0] - 1] != '#':
        pacman_pos[0] -= 1
    if keys[pygame.K_RIGHT] and map_data[pacman_pos[1]][pacman_pos[0] + 1] != '#':
        pacman_pos[0] += 1
    if keys[pygame.K_UP] and map_data[pacman_pos[1] - 1][pacman_pos[0]] != '#':
        pacman_pos[1] -= 1
    if keys[pygame.K_DOWN] and map_data[pacman_pos[1] + 1][pacman_pos[0]] != '#':
        pacman_pos[1] += 1

    # Ghost movement
    for i in range(len(ghost_positions)):
        if ghost_pause_timer[i] < pygame.time.get_ticks():  # Check if the ghost is paused
            if random.randint(0, 1) == 0:
                direction = random.choice([-1, 1])
                if map_data[ghost_positions[i][1]][ghost_positions[i][0] + direction] != '#':
                    ghost_positions[i][0] += direction
            else:
                direction = random.choice([-1, 1])
                if map_data[ghost_positions[i][1] + direction][ghost_positions[i][0]] != '#':
                    ghost_positions[i][1] += direction

    # Check for collisions with ghosts
    collision = False
    for i, ghost in enumerate(ghost_positions):
        if check_collision(pacman_pos, ghost):
            collision = True
            ghost_pause_timer[i] = pygame.time.get_ticks() + 5000  # Pause ghost for 5 seconds
            break

    # Drawing
    screen.fill(BLACK)
    draw_grid()
    draw_pacman(pacman_pos[0], pacman_pos[1])
    draw_ghosts()

    if collision:
        # Display transitive verb sentence
        if message is None:
            message = random.choice(transitive_verbs)
            message_timer = pygame.time.get_ticks() + 4000  # Show for 4 seconds
            message_duration = 4000
        display_text(message, (10, SCREEN_HEIGHT - 30))
    else:
        # Randomly select a ghost to display an intransitive verb sentence
        if message is None or message_duration == 4000:
            random_ghost = random.choice(ghost_positions)
            message = random.choice(intransitive_verbs)
            message_timer = pygame.time.get_ticks() + 2000  # Show for 2 seconds
            message_duration = 2000
        display_text(message, (random_ghost[0] * CELL_SIZE, random_ghost[1] * CELL_SIZE - 20))

    if message and pygame.time.get_ticks() > message_timer:
        message = None

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
