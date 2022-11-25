import pygame
from classes import *
from config import *

pygame.init()
screen = pygame.display.set_mode((MAX_X, MAX_Y))
game_state = "game"
# пока что будут два состояния: "game" когда играем, "gameover" когда мы проиграли.
# потом сделаем "menu", вместо "game" сделаем уровни и т.д. наверное

pygame.display.update()
clock = pygame.time.Clock()
finished = False
enemies = []
bullets = []
player = Ship.Ally()
Ship.Enemy()
Ship.Enemy()


while not finished:
    clock.tick(FPS)
    if game_state == "game": # блок действий, когда идет игра
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                pass


    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
