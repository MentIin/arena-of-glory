import pygame
from additional import load_image, get_scaled_image


class Creature(pygame.sprite.Sprite):
    def __init__(self, image, pos, *groups, scale=5, is_rigid=False):  # позиция задается центром
        super().__init__(*groups)
        self.orig_image = load_image(image)

        self.scale = scale
        image = get_scaled_image(load_image(image), scale)
        self.image = image
        self.rect = image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.is_rigid = is_rigid

class Player(Creature):
    def __init__(self, pos, *groups, scale=5):
        super().__init__(r"hero\hero1.png", pos, *groups, scale=5, is_rigid=False)
