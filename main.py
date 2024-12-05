import pygame
from lib.obstacle import Obstacle
from lib.present import Present
from lib.sleigh import Sleigh
from lib.snow_flake import Snow
from lib.golden_candy_cane import Golden_candy_cane

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
    golden_candy_canes = pygame.sprite.Group()
    
    sleigh = Sleigh()
    all_sprites.add(sleigh)

    score = 0
    spawn_present_timer = 0
    spawn_obstacle_timer = 0
    spawn_golden_candy_cane_timer = -500
    obstacle_frequency = 120
    spawn_snow_flake_timer = 0
    snow_flake_frequency = 30

    health = 3

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn presents and obstacles
        spawn_present_timer += 1
        spawn_obstacle_timer += 1
        spawn_snow_flake_timer += 1
        spawn_golden_candy_cane_timer += 1

        if spawn_present_timer > 60:
            present = Present()
            all_sprites.add(present)
            presents.add(present)
            spawn_present_timer = 0

        if spawn_obstacle_timer > obstacle_frequency:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            spawn_obstacle_timer = 0
        
        if spawn_snow_flake_timer > snow_flake_frequency:
            snow = Snow()
            all_sprites.add(snow)
            snow_flakes.add(snow)
            spawn_snow_flake_timer = 0

        if spawn_golden_candy_cane_timer > 500:
            golden_candy_cane = Golden_candy_cane()
            all_sprites.add(golden_candy_cane)
            golden_candy_canes.add(golden_candy_cane)
            spawn_golden_candy_cane_timer = 0

        #add difficulty as score goes up
        if score > 20 and score <= 29:
            obstacle_frequency = 100
            snow_flake_frequency = 25
        if score >= 30 and score <= 39:
            obstacle_frequency = 80
            snow_flake_frequency = 20
        if score >= 40 and score <= 59:
            obstacle_frequency = 60
            snow_flake_frequency = 15  
        if score >= 60:
            snow_flake_frequency = 8
            obstacle_frequency= 40

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
            sleigh.speed -= 0.02
            if score >= 60:
                sleigh.speed -= 0.02

        golden_candy_cane_hits = [g for g in golden_candy_canes if sleigh.hitbox.colliderect(g.hitbox)]
        for hit in golden_candy_cane_hits:
            hit.kill()
            sleigh.speed = 7.5
            health += 1
            score += 10

        # Game over on obstacle collision
        obstacle_hits = [o for o in obstacles if sleigh.hitbox.colliderect(o.hitbox)]
        for hit in obstacle_hits:
            health -= 1
            hit.kill()
            if health < 1:
                running = False

        # Draw
        screen.fill(WHITE)
        all_sprites.draw(screen)

         # Draw hitboxes in red
        # pygame.draw.rect(screen, BLUE, sleigh.hitbox, 2)
        # for present in presents:
        #     pygame.draw.rect(screen, RED, present.hitbox, 2)
        # for obstacle in obstacles:
        #     pygame.draw.rect(screen, RED, obstacle.hitbox, 2)
        # for flake in snow_flakes:
        #     pygame.draw.rect(screen, BLUE, flake.hitbox, 2)
        # for cane in golden_candy_canes:
        #     pygame.draw.rect(screen, BLUE, cane.hitbox, 2)

        # Score display
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        health_text = font.render(f'Health: {health}', True, (0, 0, 0))
        screen.blit(health_text, (690, 10))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    print(f"Final Score: {score}")
    pygame.quit()

if __name__ == "__main__":
    main()