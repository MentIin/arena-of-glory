from random import randint

import pygame
from additional import *
from interface import Button, CoinCounter
from creatures import *


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
        interface = pygame.sprite.Group()

        player, x, y, spawn_points = generate_level(load_level("simple_arena.map"), creatures, tile_size=TILE_SIZE)
        player.weapon = Gun(player, creatures)
        player.weapon.power *= 2
        player.weapon.reload_speed *= 2
        counter = CoinCounter((WIDTH - 165, 0), interface)

        spawner = EnemySpawner(spawn_points, creatures, [(Slime, 10)])
        spawner.spawn_mob()

        space_pressed = False

        while running:
            clock.tick(FPS)
            if roulette(1):
                spawner.spawn_mob()

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

            interface.update(player_coins=player.coins)
            interface.draw(screen)

            pygame.display.flip()
