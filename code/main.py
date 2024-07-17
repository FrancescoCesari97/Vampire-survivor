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
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


        # * gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 150

        # * enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positons = []

        # * setup
        self.load_images()
        self.setup()

        
    def load_images(self):
        self.bullet_surf = pygame.image.load(join('images', 'gun','bullet.png')).convert_alpha()

        folders =  list(walk(join('images', 'enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join ('images', 'enemies', folder)):
                 self.enemy_frames[folder] = []
                 for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                     full_path = join(folder_path, file_name)
                     surf = pygame.image.load(full_path).convert_alpha()
                     self.enemy_frames[folder].append(surf)
    
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 60
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

        # * sprites
        # self.player = Player((400, 300), self.all_sprites, self.collision_sprites)
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

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positons.append((obj.x, obj.y))

        
    def run(self):
        while self.running:
            # * dt
            dt = self.clock.tick() / 1000

            # * event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_positons), choice(list(self.enemy_frames.values())), (self.all_sprites, self.enemy_sprites), self.player, self.collision_sprites)

            # * update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)


            # * draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()