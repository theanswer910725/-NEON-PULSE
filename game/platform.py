import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((26, 26, 46))
        pygame.draw.rect(self.image, NEON_BLUE, (0, 0, width, 3))
        pygame.draw.rect(self.image, NEON_BLUE, (0, 0, 3, height))
        pygame.draw.rect(self.image, NEON_BLUE, (width-3, 0, 3, height))
        pygame.draw.rect(self.image, NEON_BLUE, (0, height-3, width, 3))
        self.rect = self.image.get_rect(x=x, y=y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
