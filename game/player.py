import pygame
import math
from pygame.math import Vector2
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.base_image = pygame.Surface((PLAYER_SIZE + 20, PLAYER_SIZE + 20), pygame.SRCALPHA)
        self.image = pygame.Surface((PLAYER_SIZE + 20, PLAYER_SIZE + 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.on_ground = False
        self.can_double_jump = True
        self.health = PLAYER_HEALTH
        self.invincible = False
        self.invincible_timer = 0
        self.time = 0
        self.breathe_phase = 0
        self.direction = 1

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.direction = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED
            self.direction = 1

    def jump(self):
        if self.on_ground:
            self.vel.y = JUMP_FORCE
            self.on_ground = False
            self.can_double_jump = True
        elif self.can_double_jump:
            self.vel.y = DOUBLE_JUMP_FORCE
            self.can_double_jump = False

    def apply_gravity(self):
        self.vel.y += GRAVITY
        if self.vel.y > 15:
            self.vel.y = 15

    def update(self, platforms):
        self.time += 1
        self.breathe_phase += 0.08
        self.apply_gravity()
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if self.pos.x < PLAYER_SIZE // 2:
            self.pos.x = PLAYER_SIZE // 2
            self.vel.x = 0
        if self.pos.x > SCREEN_WIDTH - PLAYER_SIZE // 2:
            self.pos.x = SCREEN_WIDTH - PLAYER_SIZE // 2
            self.vel.x = 0

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        self.check_platform_collision(platforms)
        self.render()

    def check_platform_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel.y > 0 and self.rect.bottom > platform.rect.top:
                    self.pos.y = platform.rect.top - PLAYER_SIZE//2
                    self.vel.y = 0
                    self.on_ground = True
                    self.can_double_jump = True

    def attack(self, target_x, target_y, projectiles):
        from projectile import Projectile
        projectiles.add(Projectile(self.pos.x, self.pos.y, target_x, target_y))

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            if self.health < 0:
                self.health = 0
            self.invincible = True
            self.invincible_timer = INVINCIBILITY_TIME

    def render(self):
        self.image.fill((0, 0, 0, 0))
        center_x = (PLAYER_SIZE + 20) // 2
        center_y = (PLAYER_SIZE + 20) // 2
        breathe = 0.8 + 0.2 * math.sin(self.breathe_phase)
        breathe_size = int((PLAYER_SIZE // 2) * breathe)

        for layer in range(5, 0, -1):
            alpha = int(25 * (6 - layer) * breathe)
            glow_radius = breathe_size + layer * 4
            glow_surf = pygame.Surface((glow_radius * 2 + 4, glow_radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*NEON_CYAN[:3], alpha), (glow_radius + 2, glow_radius + 2), glow_radius)
            self.image.blit(glow_surf, (0, 0))

        pygame.draw.circle(self.image, CYAN, (center_x, center_y), breathe_size + 2)
        pygame.draw.circle(self.image, WHITE, (center_x, center_y), breathe_size)

        inner_pulse = breathe_size * 0.6
        inner_alpha = int(150 * breathe)
        inner_surf = pygame.Surface((int(inner_pulse * 2 + 4), int(inner_pulse * 2 + 4)), pygame.SRCALPHA)
        pygame.draw.circle(inner_surf, (*ELECTRIC_CYAN[:3], inner_alpha), (int(inner_pulse) + 2, int(inner_pulse) + 2), int(inner_pulse))
        self.image.blit(inner_surf, (center_x - int(inner_pulse) - 2, center_y - int(inner_pulse) - 2))

        indicator_y = center_y - breathe_size - 8
        indicator_size = 4
        pygame.draw.polygon(self.image, NEON_CYAN, [
            (center_x, indicator_y - indicator_size),
            (center_x - indicator_size, indicator_y),
            (center_x + indicator_size, indicator_y)
        ])

    def draw(self, surface):
        if self.invincible and self.invincible_timer % 10 < 5:
            return
        surface.blit(self.image, self.rect)
