import pygame
import random

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Present(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/candy_cane.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -50
        self.speed = random.randint(3, 7)
        self.hitbox = self.rect.inflate(-50, -10)

    def update(self):
        self.rect.y += self.speed
        self.hitbox.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()