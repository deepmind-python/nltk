import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Centipede"

# Create the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(SCREEN_TITLE)

import pygame
import random
from player import Player
from laser import Laser
from mushroom import Mushroom
from centipede import CentipedeSegment # Import CentipedeSegment

# Screen dimensions (already defined)
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# SCREEN_TITLE = "Centipede"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0) # For Game Over background or text

# Mushroom Constants
MUSHROOM_HEALTH = 3
NUM_MUSHROOMS = 25
MUSHROOM_SIZE = 30 # Diameter, should match Mushroom class if using for grid spacing
GRID_SIZE = MUSHROOM_SIZE # Place mushrooms on a grid of their size - IMPORTANT for centipede

# Centipede Constants
CENTIPEDE_LENGTH = 10
CENTIPEDE_SPEED_VALUE = GRID_SIZE # Move one grid cell per frame
CENTIPEDE_START_Y = GRID_SIZE * 2 # Start a couple of rows down

# Player Area Boundary
PLAYER_AREA_Y_BOUNDARY = SCREEN_HEIGHT * 0.75

# Score
score = 0
POINTS_PER_SEGMENT = 10
# POINTS_PER_MUSHROOM_HIT and POINTS_PER_MUSHROOM_DESTROYED are handled in mushroom.py

# Game State
game_over = False

# Font for Score
pygame.font.init() # Ensure font module is initialized
score_font = pygame.font.Font(None, 36)

# Function to display score
def display_score(surface, current_score, font, color, position):
    score_text_render = font.render(f"Score: {current_score}", True, color)
    surface.blit(score_text_render, position)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Create player instance
player = Player()

# Sprite groups
all_sprites = pygame.sprite.Group()
lasers = pygame.sprite.Group()
mushrooms = pygame.sprite.Group()
centipede_segments_group = pygame.sprite.Group() # For all centipede segments
all_sprites.add(player)

# List to hold centipede segments in order (for head logic)
centipede_segments_list = []

# Function to place mushrooms
def place_mushrooms():
    # Define player area (e.g., bottom 20% of screen)
    player_area_height = SCREEN_HEIGHT * 0.25
    # Define top boundary (e.g. don't place in very top row, if desired)
    top_spawn_boundary = GRID_SIZE # e.g. one mushroom height from top
    
    # Calculate grid cells
    # Ensure mushrooms are not placed directly on the edge if GRID_SIZE is a factor of SCREEN_WIDTH
    # For simplicity, we'll place them centered within grid cells.
    # Max grid cells for x and y
    grid_x_max = SCREEN_WIDTH // GRID_SIZE
    grid_y_max = (SCREEN_HEIGHT - int(player_area_height)) // GRID_SIZE
    
    occupied_cells = set()

    for _ in range(NUM_MUSHROOMS):
        placed = False
        attempts = 0
        while not placed and attempts < NUM_MUSHROOMS * 2: # Limit attempts to avoid infinite loop
            # Random grid cell
            rand_grid_x = random.randint(0, grid_x_max - 1)
            # Ensure y is above player area and below top boundary
            rand_grid_y = random.randint(top_spawn_boundary // GRID_SIZE, grid_y_max -1)

            if (rand_grid_x, rand_grid_y) not in occupied_cells:
                # Calculate actual pixel coordinates (center of the grid cell)
                pos_x = rand_grid_x * GRID_SIZE + GRID_SIZE // 2
                pos_y = rand_grid_y * GRID_SIZE + GRID_SIZE // 2
                
                # Ensure not in very first column or last column (optional, for centipede pathing)
                # if pos_x < GRID_SIZE or pos_x > SCREEN_WIDTH - GRID_SIZE:
                #     attempts +=1
                #     continue

                mushroom = Mushroom(pos_x, pos_y, MUSHROOM_HEALTH)
                mushrooms.add(mushroom)
                all_sprites.add(mushroom)
                occupied_cells.add((rand_grid_x, rand_grid_y))
                placed = True
            attempts += 1

place_mushrooms()

# Create initial Centipede
for i in range(CENTIPEDE_LENGTH):
    # Spawn segments in a line, starting left, moving right
    # Each segment is offset by its width (GRID_SIZE) from the previous
    # A slight gap can be added if desired, but for now, they are adjacent
    x = GRID_SIZE * i 
    y = CENTIPEDE_START_Y
    color = (0, 200 - i * 15, 0) # Make segments progressively darker
    segment = CentipedeSegment(x, y, CENTIPEDE_SPEED_VALUE, GRID_SIZE, color=color)
    centipede_segments_list.append(segment)
    centipede_segments_group.add(segment)
    all_sprites.add(segment)


# Game loop
# running = True # Replaced by game_over logic
# Frame counter for slowing down centipede if needed.
# A better approach is time-based movement or adjusting FPS and CENTIPEDE_SPEED_VALUE.
# For now, let's assume CENTIPEDE_SPEED_VALUE = GRID_SIZE and FPS is okay.
# game_tick_counter = 0

while not game_over: # Main game loop condition changed
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True # Set game_over to True to exit the main loop
            # If we want to immediately quit Pygame without showing game over screen:
            # running = False 
            # pygame.quit()
            # exit() # or sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser = player.shoot()
                if laser:
                    all_sprites.add(laser)
                    lasers.add(laser)

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Update Player
    player.update(keys, mushrooms) # Pass keys and mushrooms group

    # Update Lasers
    lasers.update() 

    # Laser-Mushroom Collision
    lasers_that_hit_mushrooms = pygame.sprite.groupcollide(lasers, mushrooms, True, False) # Laser killed, mushroom not
    for laser, hit_mushrooms_list in lasers_that_hit_mushrooms.items():
        for mushroom_hit in hit_mushrooms_list:
            points_from_mushroom = mushroom_hit.hit() # Mushroom handles its own health and kill, returns points
            score += points_from_mushroom

    # Centipede Update Logic
    if centipede_segments_list: # Check if centipede still exists
        # 1. Call update on all segments to check for collisions
        for segment in centipede_segments_list:
            segment.update(mushrooms, SCREEN_WIDTH)

        # 2. Check the head segment's flag
        head_segment = centipede_segments_list[0]
        head_collided = head_segment.collision_detected_flag

        # 3. Apply movement to all segments based on head's decision
        for segment in centipede_segments_list:
            if head_collided:
                segment.apply_descent_and_reverse()
            else:
                segment.apply_horizontal_move()
            
            # Check if centipede reached player area AFTER moving
            if segment.rect.bottom >= PLAYER_AREA_Y_BOUNDARY:
                game_over = True
                break # One segment is enough to trigger game over
        if game_over: # If inner loop broke due to game over, continue to next frame (exit main loop)
            continue
    
    # Collision Detection: Lasers vs Centipede
    # pygame.sprite.collide_rect is a common collision type
    collided_lasers_dict = pygame.sprite.groupcollide(lasers, centipede_segments_group, True, False, pygame.sprite.collide_rect)

    if collided_lasers_dict:
        segments_to_remove_from_list = [] # To avoid modifying list while iterating
        
        for laser_that_hit, list_of_segments_hit in collided_lasers_dict.items():
            for segment_hit in list_of_segments_hit:
                if segment_hit in centipede_segments_list: # Ensure segment hasn't been processed already by another laser in same frame
                    
                    # Spawn Mushroom at segment's location
                    # Ensure mushroom health and grid size are available or use defaults
                    new_mushroom = Mushroom(segment_hit.rect.x, segment_hit.rect.y, MUSHROOM_HEALTH)
                    new_mushroom.rect.x = segment_hit.grid_x * GRID_SIZE # Align to grid
                    new_mushroom.rect.y = segment_hit.grid_y * GRID_SIZE # Align to grid
                    mushrooms.add(new_mushroom)
                    all_sprites.add(new_mushroom)

                    # Simplified Splitting Logic: Remove hit segment and all subsequent segments
                    try:
                        hit_index = centipede_segments_list.index(segment_hit)
                        score += POINTS_PER_SEGMENT # Award points for hitting a segment
                        
                        # Mark all segments from hit_index onwards for removal
                        segments_to_destroy_in_list = centipede_segments_list[hit_index:]
                        
                        for seg_to_destroy in segments_to_destroy_in_list:
                            seg_to_destroy.kill() # Remove from Pygame groups (all_sprites, centipede_segments_group)
                            if seg_to_destroy not in segments_to_remove_from_list: # Avoid duplicates if multiple lasers hit
                                segments_to_remove_from_list.append(seg_to_destroy)
                        
                        # Update centipede_segments_list by removing the marked segments
                        # This effectively discards the tail end of the centipede from the hit point.
                        centipede_segments_list = centipede_segments_list[:hit_index]
                        
                        # Break from inner loop (segments_hit) as this laser's job is done with this centipede part
                        break 
                        
                    except ValueError:
                        # Segment already removed from list (e.g. by a previous laser hit in same frame)
                        pass 
            # After processing one laser, if the centipede_segments_list became empty, stop processing more lasers.
            if not centipede_segments_list:
                break
    
    # Clear any segments that were marked for removal from the main list if above logic changed
    # This step is actually handled by `centipede_segments_list = centipede_segments_list[:hit_index]`

    # Collision Detection: Player vs Centipede
    if centipede_segments_group: # Only check if there are centipedes
        if not game_over: # Don't check player collision if game is already over from centipede reaching bottom
            hit_player_list = pygame.sprite.spritecollide(player, centipede_segments_group, False)
            if hit_player_list:
                game_over = True
                # player.kill() # Optional: remove player from screen immediately

    # Draw / render
    screen.fill(BLACK)  # Use defined BLACK color
    all_sprites.draw(screen) # Draws player, mushrooms, centipede, lasers
    display_score(screen, score, score_font, WHITE, (10, 10)) # Display score

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Game Over Sequence
if game_over: # This check ensures this runs only if game_over was set to True somewhere
    screen.fill(RED) # Dark red or black background for game over
    # Display final score on Game Over screen
    final_score_text = score_font.render(f"Score: {score}", True, WHITE) # Use score_font
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40))
    
    game_over_font = pygame.font.Font(None, 74) # Default Pygame font, size 74
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20))
    
    screen.blit(game_over_text, game_over_text_rect)
    screen.blit(final_score_text, final_score_rect)
    
    pygame.display.flip()
    pygame.time.wait(3000) # Show Game Over message for 3 seconds

# Quit Pygame
pygame.quit()
