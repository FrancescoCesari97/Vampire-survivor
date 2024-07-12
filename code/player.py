from pygame.sprite import _Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos ,groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('image', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)