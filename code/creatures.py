import pygame
from additional import load_image, get_scaled_image, FPS, TILE_SIZE


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
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False
        self.jump_power = 10
        self.xdir = 0  # лево или право
        self.speed = 5
        self.animation = [get_scaled_image(load_image("hero/hero1.png"), self.scale),
                          get_scaled_image(load_image("hero/hero2.png"), self.scale),
                          get_scaled_image(load_image("hero/hero3.png"), self.scale),
                          get_scaled_image(load_image("hero/hero4.png"), self.scale)]
        self.animation_tick = 0
        self.animation_speed = 200
        self.right = True

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.on_ground:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -self.jump_power
        if keys[pygame.K_a]:
            self.xdir = -1
            self.right = False
        elif keys[pygame.K_d]:
            self.xdir = 1
            self.right = True
        else:
            self.xdir = 0
        self.xvel = self.speed * self.xdir

    def update(self, *args):
        self.move()
        self.on_ground = False

        self.rect.x += self.xvel
        self.collide(self.xvel, 0)
        self.rect.y += self.yvel
        self.collide(0, self.yvel)

        if self.yvel < 0 and self.on_ground:
            self.on_ground = False

        if not self.on_ground:
            self.yvel += 20 / 60

        self.set_image()

    def set_image(self):
        self.animation_tick = (self.animation_tick + self.animation_speed / FPS) % 100
        self.orig_image = self.animation[int(self.animation_tick // 25)]
        if self.xdir == 0:
            self.orig_image = self.animation[0]
        if self.right:
           self.image = pygame.transform.flip(self.orig_image, True, False)
        else:
            self.image = self.orig_image

    def collide(self, xvel, yvel):

        for p in self.groups()[0]:
            if not p.is_rigid:
                continue
            if pygame.sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.on_ground = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает


def generate_level(level, *groups, tile_size=TILE_SIZE):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
                # Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile((x * tile_size, y * tile_size), *groups)
            elif level[y][x] == '@':
                # Tile('empty', x, y)
                new_player = Player((x * tile_size, y * tile_size), *groups)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y
