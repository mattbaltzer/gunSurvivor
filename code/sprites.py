from settings import *
from math import atan2, degrees

# When importing an image from tiled, you always want to do the topleft for the position
class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # Player connection
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(0,1)

        # Sprite setup
        super().__init__(groups)
        self.gun_surface = pygame.image.load(join('.', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surface 
        # Places the gun directly next to the player and uses the same logic in the update in order to update the position of the gun relative to the player
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        # Gets the vector for the mouse direction by getting the end point(mouse) and subtracting the start point(player)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def rotate_gun(self):
        # Atan2 will take the width and the height of a triangle, and return the angle in radians which is then turned into degrees. Subtracting 90 will normalize the angle
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        # Starts the rotation from the original surface
        if self.player_direction.x > 0:
            # Rotates the image based on the surface, the angle (expressed with the angle variable) and the scale
            self.image = pygame.transform.rotozoom(self.gun_surface, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surface, abs(angle), 1)
            # This takes the image from the previous line and flips it on the vertical axis
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        # Sets up the guns location in relation to the player that will constantly update. Bases the gun off of the center of the player, plus their direction multiplied by the distance between them
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 1000

        # Movement
        self.direction = direction
        self.speed = 1200

    def update(self, dt):
        # Basic logic for the movement of the bullet. Increases the center by the diretion multipled by the speed and delta time in order to create movement
        self.rect.center += self.direction * self.speed * dt
        # Deletes the bullet sprite after the start time becomes equal or greater than the total life time of the bullet in miliseconds
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        # Grabbing the images and setting up the animation speed
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        # Basic enemy rectangle information
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 400

    def animate(self, dt):
        # Basic animation logic
        self.frame_index += self.animation_speed * dt
        # Checks the frames dictionary for the state, grabs the integer value for the index then divides it by the length of the dictionary keys(frames -> state) and gives a remainder
        self.image = self.frames[int(self.frame_index % len(self.frames))]

    def move(self, dt):
        # Set the direction for the enemies
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        # Gets the vector for the enemy movement based upon the end point(player) minus the starting point(enemy)
        self.direction = (player_pos - enemy_pos).normalize()

        # Update the position
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                # This sets up basic collisions for the enemy and the player+objects, checks the horizontal and vertical collisions
                if direction =='horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def update(self, dt):
        self.move(dt)
        self.animate(dt)