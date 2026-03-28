import pygame
import math
import random
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.base_size = ENEMY_SIZE
        self.image = pygame.Surface((ENEMY_SIZE + 20, ENEMY_SIZE + 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True
        self.time = 0
        self.glitch_timer = 0
        self.pulse_phase = random.uniform(0, 6.28)
        self.color_shift = 0
        self.spawn_effect = False
        self.spawn_timer = 0
        self.spawn_duration = 30
        self.target_pos = pygame.math.Vector2(x, y)

    def update(self, player):
        if not self.alive:
            return

        if self.spawn_effect:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_duration:
                self.spawn_effect = False
            else:
                progress = self.spawn_timer / self.spawn_duration
                spawn_x = self.target_pos.x + (1 - progress) * 100
                spawn_y = self.target_pos.y + (1 - progress) * 50
                self.pos = pygame.math.Vector2(spawn_x, spawn_y)
                self.rect.center = (int(self.pos.x), int(self.pos.y))
                self.render()
                return

        self.time += 1
        self.pulse_phase += 0.1
        self.glitch_timer += 1

        if self.glitch_timer % 60 < 5:
            self.color_shift = random.randint(-20, 20)
        else:
            self.color_shift = 0

        dx = player.pos.x - self.pos.x
        dy = player.pos.y - self.pos.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.pos.x += (dx / dist) * ENEMY_SPEED
            self.pos.y += (dy / dist) * ENEMY_SPEED
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        self.render()

    def die(self):
        self.alive = False

    def render(self):
        self.image.fill((0, 0, 0, 0))
        center_x = (ENEMY_SIZE + 20) // 2
        center_y = (ENEMY_SIZE + 20) // 2
        pulse = 0.85 + 0.15 * math.sin(self.pulse_phase)
        enemy_size = int((self.base_size // 2) * pulse)

        spawn_alpha = 255
        if self.spawn_effect:
            spawn_alpha = int(255 * (self.spawn_timer / self.spawn_duration))

        danger_pulse = 0.7 + 0.3 * math.sin(self.time * 0.15)

        for layer in range(6, 0, -1):
            alpha = int(20 * (7 - layer) * danger_pulse * (spawn_alpha / 255))
            glow_radius = enemy_size + layer * 5
            glow_surf = pygame.Surface((glow_radius * 2 + 4, glow_radius * 2 + 4), pygame.SRCALPHA)
            red_val = min(255, 255 + self.color_shift)
            pygame.draw.circle(glow_surf, (red_val, 0, 80, alpha), (glow_radius + 2, glow_radius + 2), glow_radius)
            self.image.blit(glow_surf, (0, 0))

        core_color = (
            min(255, MAGENTA[0] + self.color_shift),
            max(0, MAGENTA[1] - abs(self.color_shift)),
            min(255, MAGENTA[2] + abs(self.color_shift // 2))
        )
        core_alpha = int(spawn_alpha)
        pygame.draw.circle(self.image, (*core_color[:3], core_alpha), (center_x, center_y), enemy_size + 2)
        pygame.draw.circle(self.image, (HOT_PINK[0], HOT_PINK[1], HOT_PINK[2], core_alpha), (center_x, center_y), enemy_size)

        inner_size = int(enemy_size * 0.5)
        inner_surf = pygame.Surface((inner_size * 2 + 4, inner_size * 2 + 4), pygame.SRCALPHA)
        inner_alpha = int(180 * danger_pulse * (spawn_alpha / 255))
        pygame.draw.circle(inner_surf, (*DANGER_RED[:3], inner_alpha), (inner_size + 2, inner_size + 2), inner_size)
        self.image.blit(inner_surf, (center_x - inner_size - 2, center_y - inner_size - 2))

        eye_alpha = int(spawn_alpha)
        eye_color = (WHITE[0], WHITE[1], WHITE[2], eye_alpha) if self.spawn_effect else WHITE
        eye_offset = 6
        eye_size = 3
        eye_y = center_y - 2
        pygame.draw.circle(self.image, eye_color, (center_x - eye_offset, eye_y), eye_size)
        pygame.draw.circle(self.image, eye_color, (center_x + eye_offset, eye_y), eye_size)
        pygame.draw.circle(self.image, DEEP_BLACK, (center_x - eye_offset, eye_y), eye_size - 1)
        pygame.draw.circle(self.image, DEEP_BLACK, (center_x + eye_offset, eye_y), eye_size - 1)

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
