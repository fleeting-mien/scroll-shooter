# import pygame - already imported through classes
from classes import *
# from config import * - already imported through classes
import sys
# from random import randint - already imported through classes

pygame.init()
screen = pygame.display.set_mode((MAX_X, MAX_Y))
game_state = "game"
# пока что будут два состояния: "game" когда играем, "gameover" когда мы проиграли.
# потом сделаем "menu", вместо "game" сделаем уровни и т.д. наверное

background = pygame.image.load("images/background.jpg")

AllyShip()
LineEnemy()

# enemy_bullet = EnemyBullet("images/enemy_bullet.png")

pygame.mouse.set_visible(False)
pygame.display.update()
clock = pygame.time.Clock()
finished = False


def update():
    """
    calls the update method of all objects
    """
    for group in groups:
        group.update()


def draw():
    """
    calls the draw method of all objects
    """
    for group in groups:
        group.draw(screen)


def shoot():
    """
    all allies shoot
    """
    for ship in ally_ship_group:
        ship.shoot()


def react_on_keys(pygame_event):
    """
    processes a KEYUP/KEYDOWN event and updates keys_down
    """
    if pygame_event.type == pygame.KEYDOWN:
        if pygame_event.key == pygame.K_w:
            keys_down["w"] = 1
        elif pygame_event.key == pygame.K_a:
            keys_down["a"] = 1
        elif pygame_event.key == pygame.K_s:
            keys_down["s"] = 1
        elif pygame_event.key == pygame.K_d:
            keys_down["d"] = 1
    elif pygame_event.type == pygame.KEYUP:
        if pygame_event.key == pygame.K_w:
            keys_down["w"] = 0
        elif pygame_event.key == pygame.K_a:
            keys_down["a"] = 0
        elif pygame_event.key == pygame.K_s:
            keys_down["s"] = 0
        elif pygame_event.key == pygame.K_d:
            keys_down["d"] = 0


while not finished:
    clock.tick(FPS)
    if game_state == "game":  # блок действий, когда идет игра
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shoot()
            react_on_keys(event)

    screen.blit(background, (0, 0))

    # if randint(1, 100) == 10:  # тестовая пуля, насколько я понимаю?
    #     enemy_bullet = EnemyBullet()

    update()
    draw()

    pygame.display.update()
    # print(ally_ship.lives)

pygame.quit()
