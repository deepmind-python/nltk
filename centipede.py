import pygame

class CentipedeSegment(pygame.sprite.Sprite):
    def __init__(self, x, y, initial_speed_x, grid_size, color=(0, 255, 0)):
        super().__init__()
        self.grid_size = grid_size
        self.image = pygame.Surface([self.grid_size, self.grid_size])
        self.image.set_colorkey((0,0,0)) # Black is transparent
        pygame.draw.circle(self.image, color, (self.grid_size // 2, self.grid_size // 2), self.grid_size // 2)
        self.rect = self.image.get_rect()
        
        # Snap to grid for initial placement
        self.grid_x = round(x / self.grid_size)
        self.grid_y = round(y / self.grid_size)
        self.rect.x = self.grid_x * self.grid_size
        self.rect.y = self.grid_y * self.grid_size
        
        self.speed_x = initial_speed_x # Horizontal speed, includes direction (+/-)
        self.collision_detected_flag = False # True if collision detected in update

    def update(self, mushrooms_group, screen_width):
        """
        Calculates next position and checks for collisions.
        Sets collision_detected_flag if a wall or mushroom is hit.
        Does NOT change position or speed directly.
        """
        self.collision_detected_flag = False # Reset at the start of each update cycle

        # Determine next potential grid x position
        # The speed_x determines direction: +1 for right, -1 for left
        next_grid_x = self.grid_x + (1 if self.speed_x > 0 else -1 if self.speed_x < 0 else 0)

        # 1. Boundary Check:
        # Check if the *next* position (next_grid_x) is outside screen bounds
        if next_grid_x < 0 or (next_grid_x * self.grid_size + self.grid_size) > screen_width:
            self.collision_detected_flag = True
            return # Collision detected, no need to check mushrooms

        # 2. Mushroom Collision Check:
        # Create a temporary rect representing the segment at its *next* horizontal grid position
        # The y position remains current self.grid_y for this check
        potential_next_rect = pygame.Rect(next_grid_x * self.grid_size, 
                                           self.grid_y * self.grid_size, 
                                           self.grid_size, 
                                           self.grid_size)

        for mushroom in mushrooms_group:
            if potential_next_rect.colliderect(mushroom.rect):
                self.collision_detected_flag = True
                return # Collision detected

        # If no collision, this segment itself doesn't trigger a descent.
        # The head segment's flag will be checked in main.py to decide for all.

    def apply_descent_and_reverse(self):
        """
        Moves the segment down by one grid unit and reverses its horizontal speed.
        Updates rect position.
        """
        self.grid_y += 1
        self.speed_x *= -1
        self.rect.x = self.grid_x * self.grid_size # x remains same during descent, but speed direction changes for next move
        self.rect.y = self.grid_y * self.grid_size
        self.collision_detected_flag = False # Reset after handling

    def apply_horizontal_move(self):
        """
        Applies horizontal movement based on current grid_x and speed_x.
        Updates rect position. This is called if no descent occurred.
        """
        # Update grid_x based on current speed direction if no collision forced a descent
        self.grid_x += (1 if self.speed_x > 0 else -1 if self.speed_x < 0 else 0)
        self.rect.x = self.grid_x * self.grid_size
        self.rect.y = self.grid_y * self.grid_size # y should already be correct

    def draw(self, screen): # For completeness, though all_sprites.draw is usually used
        screen.blit(self.image, self.rect)
