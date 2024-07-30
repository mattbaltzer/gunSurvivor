from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # Creates an AllSprites class to inherit the pygame.display.get_surface() function
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        # Sets up the camera to put the player in the middle of the screen and follow the player if they move left, right, up or down. [0] references the x position and [1] references the y position
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        for layer in [ground_sprites, object_sprites]:
        # A dynamic comparison of the center y of the player vs the object sprites, whichever is greater will be drawn later
        # Lambda is taking all of the information from the self group, then passing it through the arguement of sprite and sorting the values of the center y. Sorted works from lowest to highest
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                # Creates a basic camera, it places the topleft of the player rectangle and uses the offset that was created before the loop
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)