import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, action, *groups, scale=5):  # позиция задается центром
        super().__init__(*groups)

        image = pygame.transform.scale(image, (image.get_rect().width * scale, image.get_rect().height * scale))
        self.image = image
        self.rect = image.get_rect()
        self.scale = scale
        self.rect.center = pos

        self.action = action
