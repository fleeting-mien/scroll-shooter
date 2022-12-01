# import pygame - already imported through classes
from classes import *
import menu


pygame.init()
screen = pygame.display.set_mode((MAX_X, MAX_Y))

background = pygame.image.load("images/background.jpg")
spawn_timer = 0

pygame.mouse.set_visible(False)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

def initial_set():
    """Создает игрока и изначальных врагов"""
    AllyShip()
    LineEnemy()
    CircleEnemy()
    EnemyShip()


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


def spawn():
    """
    Эта функция, видимо, создаёт нам врагов (3 типа) раз в 100 тиков
    """
    global spawn_timer
    spawn_timer += 1
    if spawn_timer == SPAWN_TIME:
        spawn_timer = 0
        CircleEnemy()
    elif spawn_timer == SPAWN_TIME/3:
        EnemyShip()
    elif spawn_timer == SPAWN_TIME*2/3:
        LineEnemy()

initial_set()

while not finished:
    """
    mainloop
    """
    clock.tick(FPS)
    if game_state == "game":  # блок действий, когда идет игра
        spawn()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shoot()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    menu.menu_is_here.switch(1)
                if event.key == pygame.K_UP:
                    menu.menu_is_here.switch(-1)
                if event.key == pygame.K_SPACE:
                    if menu.menu_is_here.check_current_index() == 3:
                        finished = True
                        print(menu.menu_is_here.check_current_index())
                        menu.menu_is_here.select()
                    else:
                        menu.menu_is_here.select()

            react_on_keys(event)

    screen.blit(background, (0, 0))

    menu.menu_is_here.drawmenu(screen, 25, 25, 25)

    update()
    draw()

    pygame.display.update()

pygame.quit()
