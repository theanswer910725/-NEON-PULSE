import pygame
import random
import math
from constants import *

class Particle:
    def __init__(self, x, y, color, speed_multiplier=1):
        self.pos = pygame.math.Vector2(x, y)
        angle = random.uniform(0, 6.28)
        speed = random.uniform(2, 5) * speed_multiplier
        self.vel = pygame.math.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        self.color = color
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.size = random.randint(2, 5)

    def update(self):
        self.pos += self.vel
        self.vel *= 0.95
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, speed=1):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, speed))

    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.life <= 0:
                self.particles.remove(p)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
