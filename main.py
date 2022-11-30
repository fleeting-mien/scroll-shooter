import pygame
from classes import *
from config import *
import sys
from random import randint

pygame.init()
screen = pygame.display.set_mode((MAX_X, MAX_Y))
game_state = "game"
# пока что будут два состояния: "game" когда играем, "gameover" когда мы проиграли.
# потом сделаем "menu", вместо "game" сделаем уровни и т.д. наверное

background = pygame.image.load("images/background.jpg")

ally_ship = AllyShip("images/ally_ship.png")
ship_group = pygame.sprite.Group()
ship_group.add(ally_ship)
enemy_bullet = EnemyBullet("images/enemy_bullet.png")
enemy_bullet.create()
pygame.mouse.set_visible(False)
pygame.display.update()
clock = pygame.time.Clock()
finished = False


while not finished:
    clock.tick(FPS)
    if game_state == "game":  # блок действий, когда идет игра
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ally_ship.shoot()
            ally_ship.react_on_keys(event)

    screen.blit(background, (0, 0))
    ship_group.update()

    ally_ship.move()
    ally_ship.hit()

    if randint(1, 100) == 10:  # тестовая пуля, насколько я понимаю?
        enemy_bullet = EnemyBullet("images/enemy_bullet.png")
        enemy_bullet.create()

    enemy_bullet_group.update()  # строчка, заcтавляющая пулю лететь вниз
    ally_bullet_group.update()
    enemy_bullet_group.draw(screen)
    ally_bullet_group.draw(screen)

    ship_group.draw(screen)
    pygame.display.update()
    # print(ally_ship.lives)

pygame.quit()
