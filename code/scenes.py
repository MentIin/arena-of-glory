import pygame
from additional import load_image
from interface import Button


class StartScene:
    def __init__(self, screen):
        self.screen = screen
        size = width, height = screen.get_size()

        running = True
        FPS = 60

        clock = pygame.time.Clock()
        scene_sprites = pygame.sprite.Group()

        btn_start = Button(load_image(r"buttons\start_button.png"),
                           (width // 2, height // 2), self.load_game, scene_sprites)

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            scene_sprites.draw(screen)
            pygame.display.flip()

    def load_game(self):
        pass
