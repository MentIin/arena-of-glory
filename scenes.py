import pygame
from additional import *
from interface import Button
from creatures import Player, generate_level, Weapon, Gun, Enemy, Slime


class StartScene:
    def __init__(self, screen):
        self.screen = screen
        size = width, height = screen.get_size()

        running = True

        clock = pygame.time.Clock()
        scene_sprites = pygame.sprite.Group()
        buttons = pygame.sprite.Group()

        btn_start = Button(load_image(r"buttons\start_button.png"),
                           (width // 2, height // 2), self.load_game, buttons, scene_sprites)

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    for btn in buttons:
                        if btn.check_focus():
                            btn.action()


            screen.fill(pygame.color.Color("darkgreen"))

            scene_sprites.update()
            scene_sprites.draw(screen)
            pygame.display.flip()

    def load_game(self) -> None:
        GameScane(self.screen)


class GameScane:
    def __init__(self, screen):
        self.screen = screen
        size = width, height = screen.get_size()

        running = True

        clock = pygame.time.Clock()

        creatures = pygame.sprite.Group()
        buttons = pygame.sprite.Group()

        player, x, y = generate_level(load_level("simple_arena.map"), creatures, tile_size=80)
        player.weapon = Gun(player, creatures, scale=5)
        slime = Slime((100, 100), creatures)


        space_pressed = False

        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    terminate()
                if event.type == pygame.MOUSEBUTTONUP:
                    for btn in buttons:
                        if btn.check_focus():
                            btn.action()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        space_pressed = False
                if event.type == GAME_OVER:
                    running = False
            if space_pressed:
                player.use_weapon()

            screen.fill(pygame.color.Color("lightblue"))

            creatures.update(screen)
            creatures.draw(screen)
            pygame.display.flip()
