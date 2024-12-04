import pygame
from lib.obstacle import Obstacle
from lib.present import Present
from lib.sleigh import Sleigh
from lib.snow_flake import Snow
# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
    snow_flakes = pygame.sprite.Group()
    
    sleigh = Sleigh()
    all_sprites.add(sleigh)

    score = 0
    spawn_present_timer = 0
    spawn_obstacle_timer = 0
    spawn_snow_flake_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn presents and obstacles
        spawn_present_timer += 1
        spawn_obstacle_timer += 1
        spawn_snow_flake_timer += 1

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
        
        if spawn_snow_flake_timer > 30:
            snow = Snow()
            all_sprites.add(snow)
            snow_flakes.add(snow)
            spawn_snow_flake_timer = 0

        # Update
        all_sprites.update()

        # Collision detection using hitboxes
        present_hits = [p for p in presents if sleigh.hitbox.colliderect(p.hitbox)]
        for hit in present_hits:
            hit.kill()
            score += 1

        # Collision detection for snowflakes
        snow_flake_hits = [s for s in snow_flakes if sleigh.hitbox.colliderect(s.hitbox)]
        for hit in snow_flake_hits:
            hit.kill()
            sleigh.speed -= 0.01

        # Game over on obstacle collision
        obstacle_hits = [o for o in obstacles if sleigh.hitbox.colliderect(o.hitbox)]
        if obstacle_hits:
            running = False
        # Draw
        screen.fill(WHITE)
        all_sprites.draw(screen)

         # Draw hitboxes in red
        pygame.draw.rect(screen, BLUE, sleigh.hitbox, 2)
        for present in presents:
            pygame.draw.rect(screen, RED, present.hitbox, 2)
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle.hitbox, 2)
        for flake in snow_flakes:
            pygame.draw.rect(screen, BLUE, flake.hitbox, 2)

        # Score display
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    print(f"Final Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()