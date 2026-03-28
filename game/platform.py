import pygame
import math
from constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.base_y = y
        self.width = width
        self.height = height
        self.time = 0
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(x=x, y=y)
        self.render()

    def update(self):
        self.time += 1
        self.render()

    def render(self):
        self.image.fill((0, 0, 0, 0))

        base_fill = (10, 10, 25)
        pygame.draw.rect(self.image, base_fill, (0, 0, self.width, self.height))

        pulse = 0.6 + 0.4 * math.sin(self.time * 0.05)

        for i in range(4, 0, -1):
            alpha = int(15 * pulse * (5 - i))
            glow_surf = pygame.Surface((self.width + i * 4, self.height + i * 4), pygame.SRCALPHA)
            glow_rect = pygame.Rect(i // 2, i // 2, self.width - i + i, self.height - i + i)
            pygame.draw.rect(glow_surf, (*NEON_BLUE[:3], alpha), glow_rect, 2)
            self.image.blit(glow_surf, (-i // 2, -i // 2))

        pygame.draw.rect(self.image, MIDNIGHT_BLUE, (0, 0, self.width, self.height))

        border_thickness = 3
        top_color = CYAN
        bottom_color = NEON_PURPLE
        left_color = NEON_CYAN
        right_color = MAGENTA

        pygame.draw.rect(self.image, top_color, (0, 0, self.width, border_thickness))
        pygame.draw.rect(self.image, bottom_color, (0, self.height - border_thickness, self.width, border_thickness))
        pygame.draw.rect(self.image, left_color, (0, 0, border_thickness, self.height))
        pygame.draw.rect(self.image, right_color, (self.width - border_thickness, 0, border_thickness, self.height))

        corner_size = 8
        corner_glow = 6

        for i in range(corner_glow, 0, -1):
            alpha = int(40 * pulse * (corner_glow + 1 - i) / corner_glow)
            corner_surf = pygame.Surface((corner_size * 2 + i * 2, corner_size * 2 + i * 2), pygame.SRCALPHA)

            pygame.draw.line(corner_surf, (*top_color[:3], alpha), (0, corner_size + i), (i, corner_size + i), 1)
            pygame.draw.line(corner_surf, (*top_color[:3], alpha), (i, corner_size + i), (i, i), 1)

            pygame.draw.line(corner_surf, (*bottom_color[:3], alpha), (0, self.height - corner_size - i), (i, self.height - corner_size - i), 1)
            pygame.draw.line(corner_surf, (*bottom_color[:3], alpha), (i, self.height - corner_size - i), (i, self.height - i), 1)

            self.image.blit(corner_surf, (0, 0))

            corner_surf2 = pygame.Surface((corner_size * 2 + i * 2, corner_size * 2 + i * 2), pygame.SRCALPHA)

            pygame.draw.line(corner_surf2, (*left_color[:3], alpha), (0, corner_size + i), (i, corner_size + i), 1)
            pygame.draw.line(corner_surf2, (*left_color[:3], alpha), (i, corner_size + i), (i, i), 1)

            pygame.draw.line(corner_surf2, (*right_color[:3], alpha), (self.width - i, corner_size + i), (self.width, corner_size + i), 1)
            pygame.draw.line(corner_surf2, (*right_color[:3], alpha), (self.width - i, corner_size + i), (self.width - i, i), 1)

            self.image.blit(corner_surf2, (self.width - corner_size * 2 - i * 2, 0))

        inner_line_y = self.height // 2
        inner_alpha = int(30 * pulse)
        inner_surf = pygame.Surface((self.width - 20, 2), pygame.SRCALPHA)
        pygame.draw.line(inner_surf, (*NEON_BLUE[:3], inner_alpha), (0, 0), (self.width - 20, 0), 1)
        self.image.blit(inner_surf, (10, inner_line_y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
