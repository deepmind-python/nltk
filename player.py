import pygame
from laser import Laser # Import Laser

# Screen dimensions (assuming these are defined in main.py or a config file)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 30])  # Simple rectangle for now
        self.image.fill((0, 128, 255))  # Blue color
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - self.rect.width) // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10  # 10 pixels from bottom
        self.speed = 5

    def update(self, keys, mushrooms_group): # Added keys and mushrooms_group
        
        original_x = self.rect.x # Store original position for collision rollback

        # Attempt movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Boundary checks (horizontal) - apply these first
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
        # Mushroom collision check for horizontal movement
        # If, after boundary adjustment, the new position collides, revert.
        collided_with_mushroom = False
        for mushroom in mushrooms_group:
            if self.rect.colliderect(mushroom.rect):
                collided_with_mushroom = True
                break 
        
        if collided_with_mushroom:
            self.rect.x = original_x # Revert to original_x if collision

    def shoot(self):
        # Create a laser originating from the top-middle of the player
        laser = Laser(self.rect.centerx, self.rect.top)
        return laser

    def draw(self, screen): # Kept for completeness, though all_sprites.draw is often used
        screen.blit(self.image, self.rect)
