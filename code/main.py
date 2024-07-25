# Example file showing a basic pygame "game loop"
import pygame
from settings import *
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.surf = surf
        self.pos = pos
    
    def update(self, dt):
        pass

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gun Survivor')
        self.clock = pygame.time.Clock()

    def import_assets(self):
        self.player_surf = [pygame.image.load(join('.', 'images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)]

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_surface.fill("black")
            pygame.display.update()

            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()