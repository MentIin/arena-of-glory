import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join("data\images", name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def get_scaled_image(image, scale):
    return pygame.transform.scale(image, (image.get_rect().width * scale,
                                          image.get_rect().height * scale))
