import pygame
from pygame.math import Vector2
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (PLAYER_SIZE//2, PLAYER_SIZE//2), PLAYER_SIZE//2)
        pygame.draw.circle(self.image, CYAN, (PLAYER_SIZE//2, PLAYER_SIZE//2), PLAYER_SIZE//2, 3)
        self.rect = self.image.get_rect(center=(x, y))
        self.on_ground = False
        self.can_double_jump = True
        self.health = PLAYER_HEALTH
        self.invincible = False
        self.invincible_timer = 0

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = PLAYER_SPEED

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
        self.apply_gravity()
        self.pos += self.vel
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

        self.check_platform_collision(platforms)

    def check_platform_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel.y > 0 and self.rect.bottom > platform.rect.top:
                    self.pos.y = platform.rect.top - PLAYER_SIZE//2
                    self.vel.y = 0
                    self.on_ground = True
                    self.can_double_jump = True

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.invincible_timer = INVINCIBILITY_TIME

    def draw(self, surface):
        if self.invincible and self.invincible_timer % 10 < 5:
            return
        surface.blit(self.image, self.rect)
