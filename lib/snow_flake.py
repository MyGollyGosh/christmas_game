import pygame
import random

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Snow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/snow_flake.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -50
        self.speed = 2
        self.hitbox = self.rect.inflate(-10, -10)

    def update(self):
        self.rect.y += self.speed
        self.hitbox.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()