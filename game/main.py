import pygame
import sys
import random
from constants import *
from player import Player
from platform import Platform
from particles import ParticleSystem
from enemy import Enemy
from projectile import Projectile

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neon Runner")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, 300)
        self.platforms = pygame.sprite.Group()
        self.platforms.add(Platform(0, 550, 800, 50))
        self.particles = ParticleSystem()
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(600, 200))
        self.enemies.add(Enemy(400, 100))
        self.projectiles = pygame.sprite.Group()
        self.screen_shake = 0

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    self.player.attack(mx, my, self.projectiles)

    def update(self):
        self.player.handle_input(pygame.key.get_pressed())
        self.player.update(self.platforms)
        for e in self.enemies:
            e.update(self.player)
        for bullet in self.projectiles:
            bullet.update(self.particles)
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect) and enemy.alive:
                    enemy.die()
                    self.particles.emit(int(enemy.pos.x), int(enemy.pos.y), MAGENTA, 15, 1.5)
                    bullet.kill()
                    self.screen_shake = 10
        for enemy in self.enemies:
            if enemy.alive and self.player.rect.colliderect(enemy.rect):
                self.player.take_damage()
                self.screen_shake = 10
        if self.screen_shake > 0:
            self.screen_shake -= 1
        self.particles.update()

    def draw_background(self):
        self.screen.fill(BLACK)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, DARK_BLUE, (0, y), (SCREEN_WIDTH, y), 1)
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, DARK_BLUE, (x, 0), (x, SCREEN_HEIGHT), 1)

    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        for i in range(self.player.health):
            x = 20 + i * 35
            pygame.draw.circle(self.screen, PINK, (x + 12, 30), 12)
            pygame.draw.circle(self.screen, WHITE, (x + 12, 30), 8)

    def draw(self):
        if self.screen_shake > 0:
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
        else:
            offset_x = 0
            offset_y = 0

        self.draw_background()

        for platform in self.platforms:
            platform.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        for bullet in self.projectiles:
            bullet.draw(self.screen)
        self.player.draw(self.screen)
        self.particles.draw(self.screen)
        self.draw_ui()

        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
