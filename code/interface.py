import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, action, *groups, scale=5):  # позиция задается центром
        super().__init__(*groups)

        self.orig_image = image

        self.image = image
        self.scale = scale
        image = self.get_scaled_image(image, scale)
        self.rect = image.get_rect()
        self.pos = pos
        self.rect.center = pos

        self.action = action

    def update(self, *args, **kwargs) -> None:
        cof = self.scale
        if self.check_focus():
            cof = round(cof * 1.1)
        self.image = self.get_scaled_image(self.orig_image, cof)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def get_scaled_image(self, image, scale):
        return pygame.transform.scale(image, (image.get_rect().width * scale,
                                              image.get_rect().height * scale))

    def check_focus(self):
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            return True
        return False
