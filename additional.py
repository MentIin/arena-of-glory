import pygame
import os
import sys
from random import random

FPS = 60
TILE_SIZE = 50
GRAVITY = 25
GAME_OVER = pygame.USEREVENT + 1

class Effect:
    def __init__(self, name, duration, dealer, owner):
        self.name = name
        self.duration = duration
        self.owner = owner
        self.dealer = dealer
        self.start_duration = duration

    def update(self):
        self.duration -= 1 / FPS


class Knockback(Effect):
    def __init__(self, dealer, owner, duration=0.4, power=8):
        super(Knockback, self).__init__("knockback", duration, dealer, owner)
        self.power = power


    def update(self):
        if self.duration == self.start_duration:
            self.owner.effects_force = (self.owner.effects_force[0], self.owner.effects_force[1] - self.power)
        super(Knockback, self).update()
        if self.owner.rect.x - self.dealer.rect.x >= 0:
            self.owner.effects_force = (self.owner.effects_force[0] + self.power, self.owner.effects_force[1])
        else:
            self.owner.effects_force = (self.owner.effects_force[0] - self.power, self.owner.effects_force[1])


class AnimatedSprite(pygame.sprite.Sprite):
    def set_frames(self, sheet, columns, rows):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_frame(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name, colorkey=-1):
    fullname = os.path.join("data\images", name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def get_scaled_image(image, scale):
    return pygame.transform.scale(image, (image.get_rect().width * scale,
                                          image.get_rect().height * scale))


def terminate():
    pygame.quit()
    sys.exit()


def roulette(chance):
    # шанс указывается в процентах
    if random() * 100 <= chance:
        return True
    return False
