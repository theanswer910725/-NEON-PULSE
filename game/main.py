import pygame
import sys
from constants import *
from player import Player
from platform import Platform

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neon Runner")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player(100, 300)
        self.platforms = pygame.sprite.Group()
        self.platforms.add(Platform(0, 550, 800, 50))

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self):
        self.player.handle_input(pygame.key.get_pressed())
        self.player.update(self.platforms)

    def draw(self):
        self.screen.fill(BLACK)
        for platform in self.platforms:
            platform.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
