import pygame
import math
from constants import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.vel = pygame.math.Vector2(
                (dx / dist) * BULLET_SPEED,
                (dy / dist) * BULLET_SPEED
            )
        else:
            self.vel = pygame.math.Vector2(BULLET_SPEED, 0)
        self.image = pygame.Surface((BULLET_SIZE * 4, BULLET_SIZE * 4), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.trail_timer = 0
        self.time = 0
        self.trail = []

    def update(self, particles):
        self.time += 1
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if (self.pos.x < -50 or self.pos.x > SCREEN_WIDTH + 50 or
            self.pos.y < -50 or self.pos.y > SCREEN_HEIGHT + 50):
            self.kill()

        self.trail_timer += 1
        if self.trail_timer % 2 == 0 and particles:
            self.trail.append({
                'x': self.pos.x,
                'y': self.pos.y,
                'life': 15,
                'max_life': 15
            })
            particles.emit(int(self.pos.x), int(self.pos.y), NEON_CYAN, 1, 0.5)

        self.trail = [t for t in self.trail if t['life'] > 0]
        for t in self.trail:
            t['life'] -= 1

        self.render()

    def render(self):
        self.image.fill((0, 0, 0, 0))
        center = (BULLET_SIZE * 2, BULLET_SIZE * 2)

        for trail_point in self.trail:
            progress = trail_point['life'] / trail_point['max_life']
            trail_size = int(BULLET_SIZE * 0.5 * progress)
            if trail_size > 0:
                trail_x = int(trail_point['x'] - self.rect.left)
                trail_y = int(trail_point['y'] - self.rect.top)
                trail_surf = pygame.Surface((trail_size * 4, trail_size * 4), pygame.SRCALPHA)
                alpha = int(100 * progress)
                pygame.draw.circle(trail_surf, (*NEON_CYAN[:3], alpha), (trail_size * 2, trail_size * 2), trail_size)
                self.image.blit(trail_surf, (trail_x - trail_size * 2, trail_y - trail_size * 2))

        pulse = 0.8 + 0.2 * math.sin(self.time * 0.3)

        for layer in range(4, 0, -1):
            alpha = int(30 * (5 - layer) * pulse)
            glow_radius = BULLET_SIZE + layer * 3
            glow_surf = pygame.Surface((glow_radius * 2 + 4, glow_radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*ELECTRIC_CYAN[:3], alpha), (glow_radius + 2, glow_radius + 2), glow_radius)
            self.image.blit(glow_surf, (0, 0))

        pygame.draw.circle(self.image, CYAN, center, int(BULLET_SIZE * pulse) + 1)
        pygame.draw.circle(self.image, WHITE, center, int(BULLET_SIZE * 0.6 * pulse))

        core_size = int(BULLET_SIZE * 0.3 * pulse)
        if core_size > 0:
            core_surf = pygame.Surface((core_size * 4, core_size * 4), pygame.SRCALPHA)
            pygame.draw.circle(core_surf, (*GLOW_WHITE[:3], 200), (core_size * 2, core_size * 2), core_size)
            self.image.blit(core_surf, (center[0] - core_size * 2, center[1] - core_size * 2))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
