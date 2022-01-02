import pygame
import scenes
from additional import HEIGHT, WIDTH


pygame.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

scenes.StartScene(screen)
