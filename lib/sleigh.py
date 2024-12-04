import pygame

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Sleigh(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/sleigh.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 7.5
        self.hitbox = self.rect.inflate(-20, -10)

    def update(self):
        keys = pygame.key.get_pressed()
        self.image = pygame.image.load('assets/sleigh.png')
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = pygame.image.load('assets/sleigh_left.png')
            self.hitbox.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.image = pygame.image.load('assets/sleigh_right.png')
            self.hitbox.x += self.speed

