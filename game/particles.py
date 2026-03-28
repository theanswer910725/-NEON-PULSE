import pygame
import random
import math
from constants import *

class Particle:
    def __init__(self, x, y, color, speed_multiplier=1, particle_type='spark'):
        self.pos = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 6.28)
        speed = random.uniform(2, 6) * speed_multiplier
        self.vel = pygame.math.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        self.color = color
        self.particle_type = particle_type
        self.life = random.randint(PARTICLE_LIFE_MIN, PARTICLE_LIFE_MAX)
        self.max_life = self.life
        self.base_size = random.randint(2, 5)
        self.rotation = random.uniform(0, 6.28)
        self.rotation_speed = random.uniform(-0.2, 0.2) if particle_type == 'spark' else 0

    def update(self):
        self.pos += self.vel
        self.vel *= 0.96
        self.life -= 1
        self.rotation += self.rotation_speed

    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            life_ratio = self.life / self.max_life
            size = int(self.base_size * (0.5 + 0.5 * life_ratio))

            if self.particle_type == 'spark':
                self.draw_spark(surface, alpha, size)
            elif self.particle_type == 'ring':
                self.draw_ring(surface, alpha, size)
            elif self.particle_type == 'trail':
                self.draw_trail(surface, alpha, size)

    def draw_spark(self, surface, alpha, size):
        length = size * 3
        cos_a = math.cos(self.rotation)
        sin_a = math.sin(self.rotation)

        end_x = int(self.pos.x + cos_a * length)
        end_y = int(self.pos.y + sin_a * length)
        start_x = int(self.pos.x - cos_a * length * 0.5)
        start_y = int(self.pos.y - sin_a * length * 0.5)

        glow_surf = pygame.Surface((length * 2 + size * 2, length * 2 + size * 2), pygame.SRCALPHA)
        pygame.draw.line(glow_surf, (*self.color[:3], alpha // 3), (length + size, length + size), (end_x - start_x + length + size, end_y - start_y + length + size), size)
        pygame.draw.line(glow_surf, (*self.color[:3], alpha), (length + size, length + size), (end_x - start_x + length + size, end_y - start_y + length + size), size // 2)

        offset_x = int(self.pos.x) - length - size
        offset_y = int(self.pos.y) - length - size
        surface.blit(glow_surf, (offset_x, offset_y))

    def draw_ring(self, surface, alpha, size):
        ring_radius = int(size * (2 - self.life / self.max_life))
        if ring_radius > 0:
            glow_surf = pygame.Surface((ring_radius * 2 + 4, ring_radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.color[:3], alpha // 2), (ring_radius + 2, ring_radius + 2), ring_radius, 1)
            pygame.draw.circle(glow_surf, (*self.color[:3], alpha), (ring_radius + 2, ring_radius + 2), ring_radius // 2 if ring_radius > 2 else 1, 1)
            surface.blit(glow_surf, (int(self.pos.x) - ring_radius - 2, int(self.pos.y) - ring_radius - 2))

    def draw_trail(self, surface, alpha, size):
        glow_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*self.color[:3], alpha // 2), (size * 2, size * 2), size * 2)
        pygame.draw.circle(glow_surf, (*self.color[:3], alpha), (size * 2, size * 2), size)
        surface.blit(glow_surf, (int(self.pos.x) - size * 2, int(self.pos.y) - size * 2))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, speed=1, particle_type='spark'):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed, particle_type))

    def emit_explosion(self, x, y, colors=None):
        if colors is None:
            colors = [CYAN, MAGENTA, NEON_PURPLE, WHITE]

        for color in colors:
            self.emit(x, y, color, 8, 1.5, 'spark')
            self.emit(x, y, color, 4, 2.0, 'ring')

    def emit_burst(self, x, y, color, count=5):
        self.emit(x, y, color, count, 1.2, 'spark')

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
