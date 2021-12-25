import pygame
from additional import AnimatedSprite, load_image, get_scaled_image, FPS, TILE_SIZE, GRAVITY


class Creature(pygame.sprite.Sprite):
    def __init__(self, image, pos, *groups, scale=5, is_rigid=False, right=True):
        super().__init__(*groups)
        self.orig_image = get_scaled_image(image, scale)

        self.scale = scale
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos
        self.is_rigid = is_rigid
        self.right = right


class Tile(Creature):
    def __init__(self, pos, *groups, scale=5):
        super().__init__(load_image(r"tiles\tile1.png"), pos, *groups, scale=scale, is_rigid=True)


class Player(Creature, AnimatedSprite):
    def __init__(self, pos, *groups):
        im = get_scaled_image(load_image(r"hero\hero.png"), 5)
        self.set_frames(im, 4, 1)
        super().__init__(self.frames[0], pos, *groups, scale=1, is_rigid=False)
        self.xvel = 0
        self.yvel = 0
        self.on_ground = False
        self.jump_power = 13
        self.xdir = 0  # лево или право
        self.speed = 5
        self.weapon = None

        self.animation_tick = 0
        self.animation_speed = 15000
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

    def update(self, *args, **kwargs):
        self.move()
        self.on_ground = False

        self.rect.x += self.xvel
        self.collide(self.xvel, 0)
        self.rect.y += self.yvel
        self.collide(0, self.yvel)

        if self.yvel < 0 and self.on_ground:
            self.on_ground = False

        if not self.on_ground:
            self.yvel += GRAVITY / 60

        self.set_image()

        self.pos = (self.rect.x, self.rect.y)

    def set_image(self):
        self.animation_tick += self.animation_speed / FPS
        if self.animation_tick > 1000:
            self.animation_tick = 0
            self.update_frame()
        if self.right and self.xdir == 0:
            self.image = pygame.transform.flip(self.frames[0], True, False)
        elif self.xdir == 0:
            self.image = self.frames[0]
        elif self.right and self.xdir == 1:
            self.image = pygame.transform.flip(self.frames[self.cur_frame], True, False)

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


class Weapon(Creature):
    def __init__(self, owner: Creature, *groups, scale=5, reload_speed=1000, level=1):
        super().__init__(load_image(r"tiles\tile1.png"), owner.pos, *groups, scale=scale, is_rigid=False)
        self.owner = owner
        self.level = level
        self.reload_speed = reload_speed
        self.reload_tick = 0

    def update(self, *args, **kwargs) -> None:
        self.set_pos()
        self.reload_tick += self.reload_speed / FPS

    def set_pos(self):
        self.pos = self.owner.rect.center
        if self.owner.right:
            self.pos = (self.pos[0] + self.owner.rect.width // 2, self.pos[1] - self.owner.rect.height // 4)
            self.image = self.orig_image
        else:
            self.pos = (self.pos[0] - self.owner.rect.width // 2, self.pos[1] - self.owner.rect.height // 4)
            self.image = pygame.transform.flip(self.orig_image, True, False)
        self.rect.y = self.pos[1]
        self.rect.x = self.pos[0] - self.rect.width // 2

    def activate(self):
        if self.reload_tick >= 1000:
            self.reload_tick = 0
            self.fire()

    def fire(self):
        b = Bullet(self, load_image(r"tiles\tile1.png"), *self.groups())


class Bullet(Creature):
    def __init__(self, weapon: Weapon, image, *groups, speed=10, damage=10, live_time=20, scale=5):
        if weapon.owner.right:
            pos = weapon.rect.topright
            self.right = True
        else:
            pos = weapon.rect.topleft
            self.right = False
        super().__init__(image, weapon.pos, *groups, scale=scale, is_rigid=False, right=self.right)
        self.weapon = weapon
        self.speed = speed
        self.damage = damage
        self.live_time = live_time

    def update(self, *args, **kwargs) -> None:
        self.live_time -= 100 / FPS
        if self.live_time <= 0:
            a = Tile(self.pos, *self.groups(), scale=5)
            self.kill()
        if self.right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        self.pos = (self.rect.x, self.rect.y)


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
