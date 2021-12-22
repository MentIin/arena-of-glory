import pygame
from additional import load_image, get_scaled_image


class Creature(pygame.sprite.Sprite):
    def __init__(self, image, pos, *groups, scale=5, is_rigid=False):
        super().__init__(*groups)
        self.orig_image = load_image(image)

        self.scale = scale
        image = get_scaled_image(load_image(image), scale)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.rect.topleft = pos
        self.is_rigid = is_rigid

class Tile(Creature):
    def __init__(self, pos, *groups, scale=5):
        super().__init__(r"tiles\tile1.png", pos, *groups, scale=scale, is_rigid=True)

class Player(Creature):
    def __init__(self, pos, *groups):
        super().__init__(r"hero\hero1.png", pos, *groups, scale=5, is_rigid=False)


def generate_level(level, *groups, tile_size=50):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
                #Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile((x * tile_size, y * tile_size), *groups)
            elif level[y][x] == '@':
                #Tile('empty', x, y)
                new_player = Player((x * tile_size, y * tile_size), *groups)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y