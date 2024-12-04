import pygame
import random

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((800, 600))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/mince_pie.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -50
        self.speed = random.randint(3, 7)
        self.hitbox = self.rect.inflate(-15, -15)

    def update(self):
        self.rect.y += self.speed
        self.hitbox.y += self.speed
        if self.speed > 3 and self.speed < 7:
            self.image = pygame.image.load('assets/angry_elf.png')
            self.hitbox = pygame.Rect(
            self.rect.x + 0,    # Left shift
            self.rect.y + 0,    # Top shift
            self.rect.width - 100,  # Reduced width
            self.rect.height - 90  # Reduced height
                )
        if self.speed == 7:
            self.image = pygame.image.load('assets/penguin.png')
            self.hitbox = pygame.Rect(
            self.rect.x + 15,    # Left shift
            self.rect.y + 0,    # Top shift
            self.rect.width - 60,  # Reduced width
            self.rect.height - 60 # Reduced height
                )
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

