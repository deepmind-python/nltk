import pygame

class Character:
    def __init__(self, x, y, size, color, id):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.id = id
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.knowledge_base = set()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def update_rect(self):
        self.rect.topleft = (self.x, self.y)
