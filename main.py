import pygame
import math
from lib.obstacle import Obstacle
from lib.present import Present
from lib.sleigh import Sleigh
from lib.snow_flake import Snow
from lib.golden_candy_cane import Golden_candy_cane

class Game:
    def __init__(self):
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Santa's Present Collection")

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)

        # Game clock and font
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.presents = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.snow_flakes = pygame.sprite.Group()
        self.golden_candy_canes = pygame.sprite.Group()

        # Game variables
        self.sleigh = Sleigh()
        self.all_sprites.add(self.sleigh)
        self.score = 0
        self.health = 3
        self.game_over = False

        # Timers and frequencies
        self.spawn_present_timer = 0
        self.spawn_obstacle_timer = 0
        self.spawn_golden_candy_cane_timer = -500
        self.spawn_snow_flake_timer = 0
        self.obstacle_frequency = 120
        self.snow_flake_frequency = 30

        #music and sound effects
        pygame.mixer.init()
        self.hit_sound = pygame.mixer.Sound('assets/hit.mp3')
        self.bite_sound = pygame.mixer.Sound('assets/bite.mp3')
        self.ding_sound = pygame.mixer.Sound('assets/ding.mp3')
        self.music = pygame.mixer.music.load('assets/music.mp3')

    def restart(self):
        self.game_over = False
        self.score = 0
        self.health = 3

        # Clear sprite groups and recreate the sleigh
        self.all_sprites.empty()
        self.presents.empty()
        self.obstacles.empty()
        self.snow_flakes.empty()
        self.golden_candy_canes.empty()

        self.sleigh = Sleigh()
        self.all_sprites.add(self.sleigh)

    def game_over_screen(self):
        self.screen.fill(self.WHITE)

        elapsed_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
        float_offset = math.sin(elapsed_time * 2) * 10  # Adjust frequency and amplitude of float

        game_over_text = self.font.render('GAME OVER', True, self.RED)
        score_text = self.font.render(f'Your final score was {self.score}', True, self.RED)
        restart_text = self.font.render('Press R to restart', True, self.RED)

        # Center alignment
        game_over_rect = game_over_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2.3 + float_offset))
        score_rect = score_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + float_offset))
        restart_rect = restart_text.get_rect(center=(self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 1.75 + float_offset))
        self.screen.blit(game_over_text, game_over_rect.topleft)
        self.screen.blit(score_text, score_rect.topleft)
        self.screen.blit(restart_text, restart_rect.topleft)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.restart()

    def spawn_presents_and_obstacles(self):
        self.spawn_present_timer += 1
        self.spawn_obstacle_timer += 1
        self.spawn_snow_flake_timer += 1
        self.spawn_golden_candy_cane_timer += 1

        if self.spawn_present_timer > 60:
            present = Present()
            self.all_sprites.add(present)
            self.presents.add(present)
            self.spawn_present_timer = 0

        if self.spawn_obstacle_timer > self.obstacle_frequency:
            obstacle = Obstacle()
            self.all_sprites.add(obstacle)
            self.obstacles.add(obstacle)
            self.spawn_obstacle_timer = 0

        if self.spawn_snow_flake_timer > self.snow_flake_frequency:
            snow = Snow()
            self.all_sprites.add(snow)
            self.snow_flakes.add(snow)
            self.spawn_snow_flake_timer = 0

        if self.spawn_golden_candy_cane_timer > 500:
            golden_candy_cane = Golden_candy_cane()
            self.all_sprites.add(golden_candy_cane)
            self.golden_candy_canes.add(golden_candy_cane)
            self.spawn_golden_candy_cane_timer = 0

        # Adjust difficulty
        if self.score > 20 and self.score <= 29:
            self.obstacle_frequency = 100
            self.snow_flake_frequency = 25
        if self.score >= 30 and self.score <= 39:
            self.obstacle_frequency = 80
            self.snow_flake_frequency = 20
        if self.score >= 40 and self.score <= 59:
            self.obstacle_frequency = 60
            self.snow_flake_frequency = 15
        if self.score >= 60 and self.score <= 149:
            self.snow_flake_frequency = 8
            self.obstacle_frequency = 40
        if self.score >= 150:
            self.snow_flake_frequency = 2
            self.obstacle_frequency = 10

    def detect_hits(self):
        present_hits = [p for p in self.presents if self.sleigh.hitbox.colliderect(p.hitbox)]
        for hit in present_hits:
            hit.kill()
            self.score += 1
            self.bite_sound.play()

        snow_flake_hits = [s for s in self.snow_flakes if self.sleigh.hitbox.colliderect(s.hitbox)]
        for hit in snow_flake_hits:
            hit.kill()
            self.sleigh.speed -= 0.02
            if self.score >= 60:
                self.sleigh.speed -= 0.02

        golden_candy_cane_hits = [g for g in self.golden_candy_canes if self.sleigh.hitbox.colliderect(g.hitbox)]
        for hit in golden_candy_cane_hits:
            hit.kill()
            self.sleigh.speed = 7.5
            self.health += 1
            self.score += 10
            self.ding_sound.play()

        obstacle_hits = [o for o in self.obstacles if self.sleigh.hitbox.colliderect(o.hitbox)]
        for hit in obstacle_hits:
            self.health -= 1
            hit.kill()
            self.hit_sound.play()
            if self.health < 1:
                self.game_over = True

    def run(self):
        running = True
        pygame.mixer.music.play(-1)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not self.game_over:
                self.spawn_presents_and_obstacles()
                self.detect_hits()
                self.all_sprites.update()
            # Draw everything
            self.screen.fill(self.WHITE)
            if not self.game_over:
                self.all_sprites.draw(self.screen)
                score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
                health_text = self.font.render(f'Health: {self.health}', True, (0, 0, 0))
                self.screen.blit(health_text, (690, 10))
                self.screen.blit(score_text, (10, 10))
            else:
                self.game_over_screen()

            pygame.display.flip()
            self.clock.tick(60)

        print(f"Final Score: {self.score}")
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
