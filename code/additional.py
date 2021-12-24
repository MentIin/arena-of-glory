import pygame
import os
import sys


FPS = 60
TILE_SIZE = 50
GRAVITY = 25

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
