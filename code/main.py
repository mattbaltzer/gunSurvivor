# Example file showing a basic pygame "game loop"
import pygame
from settings import *
from player import Player
from sprites import *
# This imports a TMX map that you can use inside of the code
from pytmx.util_pygame import load_pygame

from random import randint

class Game():
    def __init__(self):
        # main setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gun Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

        # sprites
        # Putting the collision sprites at the end of Player makes it an arguement and allows the player to access the group, it isn't in the Collision Sprites group
        self.player = Player((400,300), self.all_sprites, self.collision_sprites)

    def setup(self):
        map = load_pygame(join('.', 'data', 'maps', 'world.tmx'))
        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

    def import_assets(self):
        self.player_surf = [pygame.image.load(join('.', 'images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)]

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.display_surface.fill('black')
            self.all_sprites.update(dt)

            # drawing
            self.all_sprites.draw(self.display_surface)
            pygame.display.update()

            # self.clock.tick(60)
        pygame.quit()

# Checks if the file is the current main file, if so it runs the game
if __name__ == '__main__':
    game = Game()
    game.run()