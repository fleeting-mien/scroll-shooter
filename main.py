import pygame
from classes import *
from config import *

pygame.init()
screen = pygame.display.set_mode((MAX_X, MAX_Y))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            pass


    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
