import pygame
import random

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/mince_pie.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -50
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.speed > 3 and self.speed < 7:
            self.image = pygame.image.load('assets/angry_elf.png')
        if self.speed == 7:
            self.image = pygame.image.load('assets/penguin.png')
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
