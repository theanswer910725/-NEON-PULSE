import pygame
import math
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.math.Vector2(x, y)
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (ENEMY_SIZE//2, ENEMY_SIZE//2), ENEMY_SIZE//2)
        pygame.draw.circle(self.image, MAGENTA, (ENEMY_SIZE//2, ENEMY_SIZE//2), ENEMY_SIZE//2, 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.alive = True

    def update(self, player):
        if not self.alive:
            return
        dx = player.pos.x - self.pos.x
        dy = player.pos.y - self.pos.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            self.pos.x += (dx / dist) * ENEMY_SPEED
            self.pos.y += (dy / dist) * ENEMY_SPEED
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def die(self):
        self.alive = False

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)
