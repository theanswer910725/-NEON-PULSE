import pygame
import sys
import random
import math
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
        pygame.display.set_caption("NEON RUNNER // CYBERDECK v2.0")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, 300)
        self.keys_pressed = set()
        self.platforms = pygame.sprite.Group()
        self.platforms.add(Platform(0, 550, 800, 50))
        self.particles = ParticleSystem()
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(600, 200))
        self.enemies.add(Enemy(400, 100))
        self.projectiles = pygame.sprite.Group()
        self.screen_shake = 0
        self.time = 0
        self.score = 0
        self.spawn_timer = 0
        self.collision_cooldown = 0
        self.base_spawn_interval = 180
        self.min_spawn_interval = 60
        self.max_enemies_on_screen = 8

        self.background_particles = []
        for _ in range(30):
            self.background_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(1, 3),
                'speed': random.uniform(0.2, 0.8),
                'color': random.choice([CYAN, MAGENTA, NEON_PURPLE]),
                'phase': random.uniform(0, 6.28)
            })

        self.title_glitch_timer = 0
        self.scanline_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.time += 1
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
                self.keys_pressed.add(event.key)
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                    self.particles.emit(int(self.player.pos.x), int(self.player.pos.y) + 20, CYAN, 8, 0.8)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    self.player.attack(mx, my, self.projectiles)
                    self.particles.emit(int(self.player.pos.x), int(self.player.pos.y), NEON_CYAN, 5, 1.2)

    def update(self):
        class KeysProxy:
            def __init__(self, pressed_set):
                self._pressed = pressed_set
            def __getitem__(self, key):
                return key in self._pressed
        self.player.handle_input(KeysProxy(self.keys_pressed))
        self.player.update(self.platforms)

        for platform in self.platforms:
            platform.update()

        for e in self.enemies:
            e.update(self.player)

        self.enemies.update(self.player)
        for dead_enemy in list(self.enemies):
            if not dead_enemy.alive:
                self.enemies.remove(dead_enemy)

        self.spawn_timer += 1
        alive_count = sum(1 for e in self.enemies if e.alive)
        if alive_count < self.max_enemies_on_screen:
            difficulty_factor = min(self.score / 1000, 1.0)
            spawn_interval = int(self.base_spawn_interval - difficulty_factor * (self.base_spawn_interval - self.min_spawn_interval))
            if self.spawn_timer >= spawn_interval:
                self.spawn_enemy()
                self.spawn_timer = 0

        for bullet in self.projectiles:
            bullet.update(self.particles)
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect) and enemy.alive:
                    enemy.die()
                    self.score += 100
                    self.particles.emit(int(enemy.pos.x), int(enemy.pos.y), MAGENTA, 10, 1.5)
                    self.particles.emit(int(enemy.pos.x), int(enemy.pos.y), NEON_PURPLE, 8, 1.2)
                    bullet.kill()
                    self.screen_shake = 6

        for enemy in self.enemies:
            if enemy.alive and not self.player.invincible and self.collision_cooldown <= 0:
                dx = self.player.pos.x - enemy.pos.x
                dy = self.player.pos.y - enemy.pos.y
                dist = math.sqrt(dx*dx + dy*dy)
                collision_threshold = (PLAYER_SIZE + ENEMY_SIZE) // 2
                if dist < collision_threshold:
                    self.player.take_damage()
                    self.screen_shake = 8
                    self.particles.emit(int(self.player.pos.x), int(self.player.pos.y), DANGER_RED, 6, 1.2)
                    knockback_dir = pygame.math.Vector2(dx, dy)
                    if knockback_dir.length() > 0:
                        knockback_dir = knockback_dir.normalize()
                        self.player.vel.x = knockback_dir.x * 10
                        self.player.vel.y = knockback_dir.y * 5
                    self.collision_cooldown = 30

        if self.player.health <= 0:
            self.game_over()

        if self.screen_shake > 0:
            self.screen_shake -= 1

        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1

        self.particles.update()

        for p in self.background_particles:
            p['y'] -= p['speed']
            if p['y'] < -10:
                p['y'] = SCREEN_HEIGHT + 10
                p['x'] = random.randint(0, SCREEN_WIDTH)

        self.title_glitch_timer += 1

    def spawn_enemy(self):
        min_dist_from_player = 150
        min_dist_from_other = 80
        margin = 50
        max_attempts = 20

        for _ in range(max_attempts):
            spawn_x = random.randint(margin, SCREEN_WIDTH - margin)
            spawn_y = random.randint(margin, SCREEN_HEIGHT // 2)

            player_dist = math.sqrt((spawn_x - self.player.pos.x)**2 + (spawn_y - self.player.pos.y)**2)
            if player_dist < min_dist_from_player:
                continue

            too_close = False
            for enemy in self.enemies:
                if enemy.alive:
                    dist = math.sqrt((spawn_x - enemy.pos.x)**2 + (spawn_y - enemy.pos.y)**2)
                    if dist < min_dist_from_other:
                        too_close = True
                        break

            if not too_close:
                new_enemy = Enemy(spawn_x, spawn_y)
                new_enemy.spawn_effect = True
                new_enemy.spawn_timer = 0
                new_enemy.target_pos = pygame.math.Vector2(spawn_x, spawn_y)
                self.enemies.add(new_enemy)
                self.particles.emit(spawn_x, spawn_y, NEON_PURPLE, 12, 1.5)
                return

    def game_over(self):
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        game_over_text = font_large.render("GAME OVER", True, DANGER_RED)
        score_text = font_small.render(f"FINAL SCORE: {self.score}", True, NEON_MAGENTA)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(DEEP_BLACK)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
            pygame.display.flip()
            self.clock.tick(FPS)

    def reset_game(self):
        self.running = True
        self.keys_pressed = set()
        self.player = Player(100, 300)
        self.platforms = pygame.sprite.Group()
        self.platforms.add(Platform(0, 550, 800, 50))
        self.particles = ParticleSystem()
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy(600, 200))
        self.enemies.add(Enemy(400, 100))
        self.projectiles = pygame.sprite.Group()
        self.screen_shake = 0
        self.time = 0
        self.score = 0
        self.spawn_timer = 0

    def draw_background(self):
        for y in range(0, SCREEN_HEIGHT, 4):
            alpha = int(15 + 10 * math.sin(self.time * 0.02 + y * 0.01))
            pygame.draw.line(self.scanline_surface, (0, 0, 0, alpha), (0, y), (SCREEN_WIDTH, y))

        self.screen.fill(DEEP_BLACK)

        for x in range(0, SCREEN_WIDTH, 40):
            alpha = int(GRID_OPACITY * (0.5 + 0.5 * math.sin(self.time * 0.015 + x * 0.005)))
            color = (*NEON_CYAN[:3], alpha) if x % 80 == 0 else (*DARK_BLUE[:3], alpha // 2)
            pygame.draw.line(self.grid_surface, color, (x, 0), (x, SCREEN_HEIGHT))

        for y in range(0, SCREEN_HEIGHT, 40):
            alpha = int(GRID_OPACITY * (0.5 + 0.5 * math.sin(self.time * 0.018 + y * 0.008)))
            color = (*NEON_PURPLE[:3], alpha) if y % 80 == 0 else (*DARK_BLUE[:3], alpha // 2)
            pygame.draw.line(self.grid_surface, color, (0, y), (SCREEN_WIDTH, y))

        self.screen.blit(self.grid_surface, (0, 0))
        self.grid_surface.fill((0, 0, 0, 0))

        for p in self.background_particles:
            pulse = 0.5 + 0.5 * math.sin(self.time * 0.05 + p['phase'])
            alpha = int(100 + 100 * pulse)
            glow_size = p['size'] + int(3 * pulse)
            glow_surf = pygame.Surface((glow_size * 4, glow_size * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*p['color'][:3], alpha // 3), (glow_size * 2, glow_size * 2), glow_size * 2)
            pygame.draw.circle(glow_surf, (*p['color'][:3], alpha), (glow_size * 2, glow_size * 2), glow_size)
            self.screen.blit(glow_surf, (int(p['x']) - glow_size * 2, int(p['y']) - glow_size * 2))

        self.screen.blit(self.scanline_surface, (0, 0))
        self.scanline_surface.fill((0, 0, 0, 0))

        corners = [
            (35, 35), (SCREEN_WIDTH - 35, 35),
            (35, SCREEN_HEIGHT - 35), (SCREEN_WIDTH - 35, SCREEN_HEIGHT - 35)
        ]
        for cx, cy in corners:
            for i in range(2):
                offset = (2 - i) * 3
                alpha = 50 - i * 20
                color = CYAN if (cx < SCREEN_WIDTH // 2) == (cy < SCREEN_HEIGHT // 2) else MAGENTA
                pygame.draw.circle(self.screen, (*color[:3], alpha), (cx, cy), 12 - offset, 2)

    def draw_ui(self):
        health_bar_width = 120
        health_bar_height = 20
        health_bar_x = 15
        health_bar_y = 35

        shield_panel = pygame.Surface((150, 60), pygame.SRCALPHA)
        pygame.draw.rect(shield_panel, (0, 0, 0, 150), (0, 0, 150, 60), border_radius=8)
        pygame.draw.rect(shield_panel, NEON_CYAN, (0, 0, 150, 60), 2, border_radius=8)
        self.screen.blit(shield_panel, (10, 12))

        font_shield = pygame.font.Font(None, 26)
        shield_text = font_shield.render("SHIELD", True, NEON_CYAN)
        self.screen.blit(shield_text, (20, 15))

        max_health = PLAYER_HEALTH
        current_health = max(0, self.player.health)
        bar_fill_width = int((current_health / max_health) * health_bar_width)

        pygame.draw.rect(self.screen, (20, 20, 40), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), border_radius=4)

        if bar_fill_width > 0:
            pulse = 0.8 + 0.2 * math.sin(self.time * 0.15)
            health_glow = pygame.Surface((bar_fill_width + 8, health_bar_height + 8), pygame.SRCALPHA)
            pygame.draw.rect(health_glow, (*NEON_CYAN[:3], int(40 * pulse)), (4, 4, bar_fill_width, health_bar_height), border_radius=4)
            self.screen.blit(health_glow, (health_bar_x - 4, health_bar_y - 4))

            pygame.draw.rect(self.screen, CYAN, (health_bar_x, health_bar_y, bar_fill_width, health_bar_height), border_radius=4)
            inner_fill = max(2, bar_fill_width - 4)
            if inner_fill > 0:
                pygame.draw.rect(self.screen, WHITE, (health_bar_x + 2, health_bar_y + 2, inner_fill, health_bar_height - 4), border_radius=3)

        pygame.draw.rect(self.screen, NEON_CYAN, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2, border_radius=4)

        for i in range(max_health):
            segment_x = health_bar_x + (health_bar_width // max_health) * i + (health_bar_width // max_health) // 2
            alive = i < current_health
            if alive:
                pygame.draw.circle(self.screen, NEON_CYAN, (segment_x, health_bar_y + health_bar_height // 2), 4)
                pygame.draw.circle(self.screen, WHITE, (segment_x, health_bar_y + health_bar_height // 2), 2)
            else:
                pygame.draw.circle(self.screen, (50, 50, 70), (segment_x, health_bar_y + health_bar_height // 2), 3, 1)

        score_x = SCREEN_WIDTH - 160
        score_y = 12

        pygame.draw.rect(self.screen, (0, 0, 0, 180), (score_x, score_y, 145, 60), border_radius=8)
        pygame.draw.rect(self.screen, NEON_MAGENTA, (score_x, score_y, 145, 60), 2, border_radius=8)

        pygame.draw.line(self.screen, NEON_MAGENTA, (score_x + 10, score_y + 25), (score_x + 135, score_y + 25), 1)

        font_score = pygame.font.Font(None, 20)
        score_label = font_score.render("SCORE", True, NEON_MAGENTA)
        self.screen.blit(score_label, (score_x + 72 - score_label.get_width() // 2, score_y + 6))

        font_score_num = pygame.font.Font(None, 38)
        score_value = font_score_num.render(f"{self.score}", True, WHITE)
        self.screen.blit(score_value, (score_x + 72 - score_value.get_width() // 2, score_y + 30))

    def draw_title(self):
        if self.player.health <= 0:
            return

        glitch_active = self.title_glitch_timer % 120 < 15

        font_large = pygame.font.Font(None, 64)
        font_small = pygame.font.Font(None, 24)

        title = "NEON RUNNER"
        title_surf = font_large.render(title, True, WHITE)

        if glitch_active:
            offset = random.randint(-4, 4)
            glitch_colors = [DANGER_RED, NEON_CYAN, NEON_MAGENTA]
            glitch_color = random.choice(glitch_colors)
            glitch_surf = font_large.render(title, True, glitch_color)
            self.screen.blit(glitch_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 + offset, 125))

        for i in range(3, 0, -1):
            alpha = 25 + i * 12
            glow_surf = pygame.Surface((title_surf.get_width() + i * 4, title_surf.get_height() + i * 4), pygame.SRCALPHA)
            glow_text = font_large.render(title, True, (*NEON_CYAN[:3], alpha))
            glow_surf.blit(glow_text, (i * 2, i * 2))
            self.screen.blit(glow_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2 - i * 2, 125 - i * 2))

        self.screen.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 125))

        subtitle = "// CYBERDECK PROTOCOL //"
        sub_surf = font_small.render(subtitle, True, NEON_PURPLE)
        pulse = 0.6 + 0.4 * math.sin(self.time * 0.08)
        alpha_sub = int(180 * pulse)
        sub_glow = font_small.render(subtitle, True, (*NEON_PURPLE[:3], alpha_sub))
        self.screen.blit(sub_glow, (SCREEN_WIDTH // 2 - sub_surf.get_width() // 2, 110))

    def draw_instructions(self):
        font_small = pygame.font.Font(None, 22)
        instructions = "[ARROW KEYS] MOVE   [SPACE] JUMP   [MOUSE CLICK] ATTACK"
        inst_surf = font_small.render(instructions, True, (150, 150, 180))

        pygame.draw.rect(self.screen, (0, 0, 0, 120), (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
        pygame.draw.line(self.screen, NEON_PURPLE, (0, SCREEN_HEIGHT - 40), (SCREEN_WIDTH, SCREEN_HEIGHT - 40), 1)

        for i in range(5):
            x_pos = (self.time * 2 + i * 200) % (SCREEN_WIDTH + 200) - 100
            alpha = int(100 * (1 - abs(x_pos - SCREEN_WIDTH // 2) / (SCREEN_WIDTH // 2)))
            if alpha > 0:
                pygame.draw.circle(self.screen, (*NEON_PURPLE[:3], alpha), (int(x_pos), SCREEN_HEIGHT - 20), 2)

        self.screen.blit(inst_surf, (SCREEN_WIDTH // 2 - inst_surf.get_width() // 2, SCREEN_HEIGHT - 30))

    def draw(self):
        if self.screen_shake > 0:
            offset_x = random.randint(-6, 6)
            offset_y = random.randint(-6, 6)
        else:
            offset_x = 0
            offset_y = 0

        surface = self.screen
        if offset_x != 0 or offset_y != 0:
            surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        self.draw_background()

        for platform in self.platforms:
            platform.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        for bullet in self.projectiles:
            bullet.draw(self.screen)
        self.player.draw(self.screen)
        self.particles.draw(self.screen)

        self.draw_title()
        self.draw_ui()
        self.draw_instructions()

        if offset_x != 0 or offset_y != 0:
            self.screen.blit(surface, (offset_x, offset_y))
        else:
            corner_frame(self.screen)

        pygame.display.flip()

def corner_frame(surface):
    frame_color = NEON_CYAN
    thickness = 2
    corner_size = 25

    pygame.draw.line(surface, frame_color, (0, corner_size), (0, 0), thickness)
    pygame.draw.line(surface, frame_color, (0, 0), (corner_size, 0), thickness)
    pygame.draw.line(surface, frame_color, (SCREEN_WIDTH - corner_size, 0), (SCREEN_WIDTH, 0), thickness)
    pygame.draw.line(surface, frame_color, (SCREEN_WIDTH, 0), (SCREEN_WIDTH, corner_size), thickness)
    pygame.draw.line(surface, frame_color, (0, SCREEN_HEIGHT - corner_size), (0, SCREEN_HEIGHT), thickness)
    pygame.draw.line(surface, frame_color, (0, SCREEN_HEIGHT), (corner_size, SCREEN_HEIGHT), thickness)
    pygame.draw.line(surface, frame_color, (SCREEN_WIDTH - corner_size, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT), thickness)
    pygame.draw.line(surface, frame_color, (SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - corner_size), thickness)

if __name__ == "__main__":
    game = Game()
    game.run()
