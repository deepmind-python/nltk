import pygame

# Screen dimensions (assuming these are defined in main.py or a config file)
SCREEN_HEIGHT = 600

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([5, 15])  # Small, thin rectangle
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y  # Laser starts from the bottom of this y (player's top)
        self.speed = -10  # Negative for upward movement

    def update(self):
        self.rect.y += self.speed
        # Remove laser if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()
