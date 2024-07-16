from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

from random import *

class Game:
    def __init__(self):
        # * setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Vampire survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # * groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()


        # * sprites
        self.player = Player((400, 300), self.all_sprites, self.collision_sprites)
        # for i in range(7):
        #     x, y = randint(0, WINDOW_WIDTH), randint(0,WINDOW_HEIGHT)
        #     w, h = randint(50, 80), randint(50, 80)
        #     CollisionSprite((x,y), (w, h), (self.all_sprites, self.collision_sprites))

    def setup(self):
        map = load_pygame(join('data', 'maps', 'world.tmx'))
        
        for x,y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        
    def run(self):
        while self.running:
            # * dt
            dt = self.clock.tick() / 1000

            # * event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # * update
            self.all_sprites.update(dt)


            # * draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()