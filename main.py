import pygame

import sys
import os

path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(path)  # изменение рабочего пути на 1 вверх

import scenes



pygame.init()
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
scenes.StartScene(screen)
