import pygame
from lib.obstacle import Obstacle
from lib.present import Present
from lib.sleigh import Sleigh
# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Santa's Present Collection")


# Game objects

def main():
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    presents = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    
    sleigh = Sleigh()
    all_sprites.add(sleigh)

    score = 0
    spawn_present_timer = 0
    spawn_obstacle_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn presents and obstacles
        spawn_present_timer += 1
        spawn_obstacle_timer += 1

        if spawn_present_timer > 60:
            present = Present()
            all_sprites.add(present)
            presents.add(present)
            spawn_present_timer = 0

        if spawn_obstacle_timer > 120:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            spawn_obstacle_timer = 0

        # Update
        all_sprites.update()

        # Collision detection
        present_hits = pygame.sprite.spritecollide(sleigh, presents, True)
        score += len(present_hits)

        # Game over on obstacle collision
        if pygame.sprite.spritecollideany(sleigh, obstacles):
            running = False

        # Draw
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Score display
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    print(f"Final Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()