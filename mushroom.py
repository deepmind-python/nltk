import pygame

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, x, y, health=3):
        super().__init__()
        self.original_image = pygame.Surface([30, 30])  # Diameter of 30
        self.original_image.set_colorkey((0,0,0)) # Black transparent
        pygame.draw.circle(self.original_image, (139, 69, 19), (15, 15), 15)  # Brown circle
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.health = health
        self.max_health = health
        # Point constants for mushroom
        self.points_hit = 1
        self.points_destroyed = 5


    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return self.points_destroyed # Return points for destruction
        else:
            # Change appearance on hit
            damage_factor = (self.health / self.max_health)
            r = int(139 * damage_factor)
            g = int(69 * damage_factor)
            b = int(19 * damage_factor)
            
            r = max(0, min(r, 255))
            g = max(0, min(g, 255))
            b = max(0, min(b, 255))

            new_color = (r,g,b)
            self.image = self.original_image.copy()
            pygame.draw.circle(self.image, new_color, (15, 15), 15)
            return self.points_hit # Return points for just a hit


    def update(self):
        # Not strictly necessary for stationary mushrooms, but can be added if needed later.
        pass
