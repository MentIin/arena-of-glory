import pygame
from additional import load_image, get_scaled_image

class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, action, *groups, scale=5):  # позиция задается центром
        super().__init__(*groups)

        self.orig_image = image

        self.image = image
        self.scale = scale
        image = get_scaled_image(image, scale)
        self.rect = image.get_rect()
        self.pos = pos
        self.rect.center = pos

        self.action = action

    def update(self, *args, **kwargs) -> None:
        cof = self.scale
        if self.check_focus():
            cof = round(cof * 1.1)
        self.image = get_scaled_image(self.orig_image, cof)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    def check_focus(self):
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            return True
        return False
