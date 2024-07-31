# Example file showing a basic pygame "game loop"
import pygame
from settings import *
from player import Player
from sprites import *
from groups import AllSprites
# This imports a TMX map that you can use inside of the code
from pytmx.util_pygame import load_pygame

from random import randint, choice

class Game():
    def __init__(self):
        # Main setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gun Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

        # Enemy timers
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 100)
        self.spawn_positions = []

        # Sound effects/background music
        self.hit_sound = pygame.mixer.Sound(join('audio', 'impact.ogg'))
        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        bg_music = pygame.mixer.Sound(join('audio', 'music.wav'))
        bg_music.set_volume(0.04)
        # Setting the music to a loop of -1 will have it loop indefinitely
        bg_music.play(loops = -1)

        # Game setup 
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surface = pygame.image.load(join('.', 'images', 'gun', 'bullet.png')).convert_alpha()

        # This sets up a list of the folders associated with the enemies, it grabs the first list printed out since there are no files to grab
        folders = list(walk(join('.', 'images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            # Loop searches through the folder path using walk and join: current -> images -> enemies -> then checks for the folder which holds each enemies individual frames
            for folder_path, _, file_names in walk(join('.', 'images', 'enemies', folder)):
                # Sets the dictionary with the folder key to an empty list
                self.enemy_frames[folder] = []
                # This searches through the folders for the specific file names, splits them on the '.' and then converts the string that is returned into an integer to be used in the loop
                for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                    # Sets the full path to the joint value of the folder path and the file name
                    full_path = join(folder_path, file_name)
                    # Creates a surface which has the image contained in the previous variable and converts it to an alpha to remove the spare pixels
                    surf = pygame.image.load(full_path).convert_alpha()
                    # Adds the new image to the values in the frames dictionary based upon the folder  
                    self.enemy_frames[folder].append(surf)
                    
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            # Creates the starting postion for the bullet based off of the guns direction, plus the direction that the player is facing with an arbitrary number as padding
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surface, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.shoot_sound.play()
            self.shoot_sound.set_volume(0.02)

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True
                
    def setup(self):
        map = load_pygame(join('.', 'data', 'maps', 'world.tmx'))
            
        # Creates the collision object for the player to interact with. Didn't have a surface so had to create one with pygame by using the width and height of the collision object
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
            
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                # Putting the collision sprites at the end of Player makes it an arguement and allows the player to access the group, it isn't in the Collision Sprites group
                self.player = Player((obj.x,obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                # Setting up the spawn locations for the enemy based on the tmx map that was provided by adding the x and y for the obj to the spawn positions
                self.spawn_positions.append((obj.x, obj.y))

    def import_assets(self):
        self.player_surf = [pygame.image.load(join('.', 'images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)]

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                # If a bullet collides with an enemy, it will remove the enemy from the active enemy list
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.hit_sound.play()
                    self.hit_sound.set_volume(0.1)
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    # Choice cannot grab values directly, it has to be taken from a list
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # Update
            pygame.mouse.set_visible(False)
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)
            self.bullet_collision()
            self.player_collision()

            # Drawing
            self.display_surface.fill('black')
            # This is causing the display surface to follow the player around, like a camera
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

            # self.clock.tick(60)
        pygame.quit()

# Checks if the file is the current main file, if so it runs the game
if __name__ == '__main__':
    game = Game()
    game.run()