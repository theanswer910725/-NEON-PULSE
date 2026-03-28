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
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, CYAN, (BULLET_SIZE//2, BULLET_SIZE//2), BULLET_SIZE//2)
        self.rect = self.image.get_rect(center=(x, y))
        self.trail_timer = 0

    def update(self, particles):
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.trail_timer += 1
        if self.trail_timer % 3 == 0 and particles:
            particles.emit(int(self.pos.x), int(self.pos.y), CYAN, 2, 0.3)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
