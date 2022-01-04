import pygame
from scenes import StartScene
from additional import HEIGHT, WIDTH


pygame.init()
pygame.font.init()
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

StartScene(screen)
