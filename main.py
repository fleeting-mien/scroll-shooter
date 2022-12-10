# import pygame - already imported through classes
import pygame.time

from classes import *
from menu import *

pygame.init()


screen = pygame.display.set_mode((MAX_X, MAX_Y))

background = Background()
about_image = AboutInfo()
ARIAL_18 = pygame.font.SysFont('arial', 18)
ARIAL_25 = pygame.font.SysFont('arial', 25)
ARIAL_45 = pygame.font.SysFont('arial', 45)
spawn_timer = 0

pygame.display.update()
clock = pygame.time.Clock()
finished = False
boss = 0
ost_game = 0
ost_boss = 0
boss_timer = 0

def initial_set():
    """Создает игрока и изначальных врагов"""
    global player
    player = AllyShip()
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


def start_shooting():
    """
    all allies start shooting
    """
    for ship in ally_ship_group:
        ship.start_shooting()


def stop_shooting():
    """
    all allies stop shooting
    """
    for ship in ally_ship_group:
        ship.stop_shooting()


def shooting():
    """
    all allies shoot
    """
    for ship in ally_ship_group:
        ship.shooting()


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


def react_on_menu_keys(menu_event):
    """
    Реакция на нажатие кнопок меню
    """
    global finished
    global game_state
    if menu_event.type == pygame.KEYDOWN:
        if menu_event.key == pygame.K_DOWN:
            menu_is_here.switch(1)
        if menu_event.key == pygame.K_UP:
            menu_is_here.switch(-1)
        if menu_event.key == pygame.K_SPACE or menu_event.key == pygame.K_RETURN:
            if menu_is_here.check_current_index() == 0:
                if game_state == "game":
                    print("Ты уже и так играешь, идиот")
                else:
                    game_state = "game"
            elif menu_is_here.check_current_index() == 1:
                game_state = "pause"
                # game_state = menu_is_here.select()
                # команда выше, вероятно будет работать, когда я до конца допишу условия для всех game_state
                # pass
            elif menu_is_here.check_current_index() == 2:
                finished = True
                menu_is_here.select()
            elif menu_is_here.check_current_index() == 4:
                game_state = "about"


def spawn():
    """
    Эта функция создаёт нам 4 типа врагов раз в 100 тиков
    """
    global spawn_timer
    if not boss:
        spawn_timer += 1
    else:
        spawn_timer = 0

    if spawn_timer == SPAWN_TIME:
        spawn_timer = 0
        CircleEnemy()
    elif spawn_timer == SPAWN_TIME/3:
        EnemyShip()
    elif spawn_timer == SPAWN_TIME*2/3:
        LineEnemy()
        Asteroid()


def textbar():
    """
    Игровая информация на экране в правом верхнем углу
    """
    healthbar = ARIAL_25.render(
        "Your health: " + str(player.lives),
        True, (255, 255, 0)
    )
    screen.blit(healthbar, (MAX_X * 3 / 4, 0))
    scorebar = ARIAL_25.render(
        "Your score: " + str(player.score),
        True, (255, 255, 0)
    )
    screen.blit(scorebar, (MAX_X * 3 / 4, 30))


def round_of_game(x):
    return int(10*x) / 10


def buff_text():
    if player.shield.timer > 0:
        shieldbar = ARIAL_18.render(
            "Shield: " + str(round_of_game(player.shield.timer / FPS)) + " sec",
            True, (255, 255, 0)
        )
        screen.blit(shieldbar, (0, MAX_Y/2))

    if player.score_factor.timer > 0:
        scorefactorbar = ARIAL_18.render(
            "x2: " + str(round_of_game(player.score_factor.timer / FPS)) + "sec",
            True, (255, 255, 0)
        )
        screen.blit(scorefactorbar, (0, MAX_Y/2 + 20))

    if player.shooting_style.timer > 0:
        if player.shooting_style.state == "double":
            shootingbar = ARIAL_18.render(
                "Double shot: " + str(round_of_game(player.shooting_style.timer / FPS)) + " sec",
                True, (255, 255, 0)
            )
        elif player.shooting_style.state == "triple":
            shootingbar = ARIAL_18.render(
                "Triple shot: " + str(round_of_game(player.shooting_style.timer / FPS)) + " sec",
                True, (255, 255, 0)
            )
        else:
            shootingbar = ARIAL_18.render(
                "Laser: " + str(round_of_game(player.shooting_style.timer / FPS)) + " sec",
                True, (255, 255, 0)
            )
        screen.blit(shootingbar, (0, MAX_Y/2 + 40))

    if player.heal.timer > 0:
        healbar = ARIAL_18.render(
            "Healed 1 HP!",
            True, (255, 255, 0)
        )
        screen.blit(healbar, (0, MAX_Y/2 + 60))


def boss_arrival():
    if BOSS_SCORE - 5 <= player.score < BOSS_SCORE:
        bossbar = ARIAL_18.render(
            str(BOSS_SCORE - player.score) + " point remaining until the arrival of the Boss",
            True, (255, 255, 0)
        )
        screen.blit(bossbar, (MAX_X/4, 20))

initial_set()

while not finished:
    """
    mainloop
    """
    clock.tick(FPS)
    if game_state == "game":  # блок действий, когда идет игра
        if not ost_game:
            game_music = random.choice(['game1', 'game2'])
            print(music[game_music])
            pygame.mixer.music.load(music[game_music])
            pygame.mixer.music.play()
            ost_game = 1
        spawn()
        shooting()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_shooting()
            elif event.type == pygame.MOUSEBUTTONUP:
                stop_shooting()
            react_on_menu_keys(event)
            react_on_keys(event)
        menu_is_here.drawmenu(screen, 5, 5, 25)
        update()
        draw()
        textbar()
        buff_text()
        boss_arrival()
        if player.score >= BOSS_SCORE:
            boss_timer +=1
            if not ost_boss:
                game_music = random.choice(['boss1'])
                pygame.mixer.music.load(music[game_music])
                pygame.mixer.music.play()
                ost_boss = 1
                boss = 1
            if boss_timer == 900:
                Boss(ARIAL_25)
        pygame.display.update()
    elif game_state == "pause":
        stop_shooting()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            react_on_menu_keys(event)
        menu_is_here.drawmenu(screen, 5, 5, 25)
        pausebar = ARIAL_25.render("Pause!", True, (255, 255, 0))
        screen.blit(pausebar, (MAX_X / 2 - 50, MAX_Y / 2))
        textbar()
        pygame.display.update()
    elif game_state == "about":
        stop_shooting()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            react_on_menu_keys(event)
        about_image.update()
        menu_is_here.drawmenu(screen, 5, 5, 25)
        aboutbar = ARIAL_45.render("About", True, (255, 255, 255))
        screen.blit(aboutbar, (MAX_X / 2 - 50, 10))
        pygame.display.update()


    background.update()

if finished:
    '''
    Здесь происходят все события вне mainloop
    '''
    if game_state == "startscreen":
        pass
    elif game_state == "gameover":
        pass
        # дописать

    background.update()

    menu_is_here.drawmenu(screen, 25, 25, 25)

    update()

    pygame.display.update()

pygame.quit()
