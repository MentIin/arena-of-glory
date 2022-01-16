from random import choice

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
                if event.type == pygame.KEYDOWN:
                    self.load_game()

            screen.fill(pygame.color.Color("darkgreen"))

            scene_sprites.update()
            scene_sprites.draw(screen)
            pygame.display.flip()

    def load_game(self) -> None:
        GameScene(self.screen)


class GameScene:
    def __init__(self, screen):
        self.screen = screen
        size = width, height = screen.get_size()

        running = True

        clock = pygame.time.Clock()

        creatures = pygame.sprite.Group()
        buttons = pygame.sprite.Group()
        interface = pygame.sprite.Group()

        level_name = choice(LEVELS)

        player, x, y, spawn_points = generate_level(load_level(level_name), creatures, tile_size=TILE_SIZE)
        player.weapon = Gun(player, creatures)
        counter = CoinCounter((WIDTH - 165, 5), interface)

        spawner = EnemySpawner(spawn_points, creatures, [(Slime, 10)])
        spawner.spawn_mob()

        space_pressed = False

        while running:
            clock.tick(FPS)
            spawner.update()

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
        GameOverScene(self.screen, counter.coins)


class GameOverScene:
    def __init__(self, screen, score):
        self.screen = screen
        size = width, height = screen.get_size()

        record = get_stat("record")

        running = True

        clock = pygame.time.Clock()
        scene_sprites = pygame.sprite.Group()
        buttons = pygame.sprite.Group()

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
                    running = False

            screen.fill(pygame.color.Color("lightblue"))
            draw_text(self.screen, "Your score:", 40, (WIDTH // 2, height // 2 - 80), center=True)
            draw_text(self.screen, str(score), 40, (WIDTH // 2, height // 2 - 40), center=True)
            draw_text(self.screen, "Record:", 40, (WIDTH // 2, height // 2), center=True)
            draw_text(self.screen, str(record), 40, (WIDTH // 2, height // 2 + 40), center=True)

            scene_sprites.update()
            scene_sprites.draw(screen)
            pygame.display.flip()
