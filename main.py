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
ost_menu = 0
boss_timer = 0


def initial_set():
    """
    Создает игрока и изначальных врагов
    """
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


def restart_game():
    """
    Перезапускает игру сначала
    """
    global ost_menu, ost_game, ost_boss
    for group in groups:
        group.empty()
    global game_state, boss, boss_timer
    game_state = "game"
    ost_game = 0
    ost_boss = 0
    ost_menu = 0
    boss = 0
    boss_timer = 0
    initial_set()


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
    function for wasd moving
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
    Навигация по кнопкам - стрелки вверх/вниз
    Активация выбранного пункта меню - Enter
    """
    global finished
    global game_state
    if menu_event.type == pygame.KEYDOWN:
        if menu_event.key == pygame.K_DOWN:
            menu_is_here.switch(1)
        if menu_event.key == pygame.K_UP:
            menu_is_here.switch(-1)
        if menu_event.key == pygame.K_RETURN:
            if menu_is_here.check_current_index() == 0:
                game_state = "game"
            elif menu_is_here.check_current_index() == 1:
                game_state = "pause"
            elif menu_is_here.check_current_index() == 2:
                if game_state == "startscreen":
                    finished = True
                    menu_is_here.select()
                else:
                    game_state = "startscreen"
            elif menu_is_here.check_current_index() == 3:
                restart_game()
            elif menu_is_here.check_current_index() == 4:
                game_state = "about"


def spawn():
    """
    Эта функция создаёт нам 4 типа врагов раз в 100 тиков
    """
    global spawn_timer
    if not boss and player.lives > 0:
        spawn_timer += 1
    else:
        spawn_timer = 0

    if spawn_timer == FPS * SPAWN_SECONDS:
        spawn_timer = 0
        CircleEnemy()
    elif spawn_timer == FPS * SPAWN_SECONDS/3:
        EnemyShip()
    elif spawn_timer == FPS * SPAWN_SECONDS*2/3:
        LineEnemy()
        Asteroid()


def textbar():
    """
    Игровая информация на экране в правом верхнем углу
    healthbar - показывает жизни игрока
    scorebar - показывает набранные игроком очки
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


def buff_text():
    """
    Функция, выводящая информацию о баффах
    """
    if player.shield.timer > 0:
        shieldbar = ARIAL_18.render(
            "Shield: " + str(round(player.shield.timer / FPS, 1)) + " sec",
            True, (255, 255, 0)
        )
        screen.blit(shieldbar, (0, MAX_Y/2))

    if player.score_factor.timer > 0:
        scorefactorbar = ARIAL_18.render(
            "x2: " + str(round(player.score_factor.timer / FPS, 1)) + "sec",
            True, (255, 255, 0)
        )
        screen.blit(scorefactorbar, (0, MAX_Y/2 + 20))

    if player.shooting_style.timer > 0:
        if player.shooting_style.state == "double":
            shootingbar = ARIAL_18.render(
                "Double shot: " + str(round(player.shooting_style.timer / FPS, 1)) + " sec",
                True, (255, 255, 0)
            )
        elif player.shooting_style.state == "triple":
            shootingbar = ARIAL_18.render(
                "Triple shot: " + str(round(player.shooting_style.timer / FPS, 1)) + " sec",
                True, (255, 255, 0)
            )
        else:
            shootingbar = ARIAL_18.render(
                "Laser: " + str(round(player.shooting_style.timer / FPS, 1)) + " sec",
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
    """
    Предупреждает, что скоро будет мясо
    """
    if BOSS_SCORE - 5 <= player.score < BOSS_SCORE:
        bossbar = ARIAL_18.render(
            str(BOSS_SCORE - player.score) + " points remaining until the arrival of the Boss",
            True, (255, 255, 0)
        )
        screen.blit(bossbar, (MAX_X/4, 20))


def boss_is_here():
    global boss_timer, ost_boss, boss

    if player.score >= BOSS_SCORE:
        if boss_timer >= 901:
            boss_timer = 901
        else:
            boss_timer += 1
            warning = ARIAL_25.render("WARNING, BOSS INCOMING!!!", True, (255, 255, 0))
            screen.blit(warning, (MAX_X / 4 + 15, MAX_Y / 1.5))

        if not ost_boss:
            game_music = random.choice(['boss1', 'boss2'])
            pygame.mixer.music.load(music[game_music])
            pygame.mixer.music.play()
            ost_boss = 1
            boss = 1

        if 0 < boss_timer < 900 and boss_timer % 40 < 20:
            screen.blit(pygame.image.load('images/boss_warning.png'), (MAX_X / 3.5, MAX_Y / 4))

        if boss_timer == 900:
            Boss(ARIAL_25)
            # BOSS_SCORE += BOSS_SCORE


initial_set()

while not finished:
    """
    mainloop
    далее идёт обработка различных значений game_state
    """
    clock.tick(FPS)

    if game_state == "startscreen":
        if not ost_menu:
            game_music = random.choice(['menu1', 'menu2'])
            pygame.mixer.music.load(music[game_music])
            pygame.mixer.music.play()
            ost_menu = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            react_on_menu_keys(event)
        menu_is_here.drawmenu(screen, MAX_X / 2 - 30, 40, 40)
        start_text_1 = ARIAL_45.render("Press <Start> to play the game", True, (255, 0, 0))
        screen.blit(start_text_1, (100, MAX_Y / 2 - 100))
        start_text_2 = ARIAL_45.render("Press <About> to help and more info", True, (255, 0, 0))
        screen.blit(start_text_2, (50, MAX_Y / 2))
        help_text = ARIAL_18.render(
            "Use the Up/Down arrow keys and press Enter/Space button to activate the selected option ",
            True, (255, 255, 0))
        screen.blit(help_text, (60, MAX_Y - 50))
        pygame.display.update()
    elif game_state == "game":  # блок действий, когда идет игра
        if not ost_game:
            game_music = random.choice(['game1', 'game2'])
            pygame.mixer.music.load(music[game_music])
            pygame.mixer.music.play()
            ost_game = 1
        spawn()
        shooting()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_shooting()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    stop_shooting()
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
        boss_is_here()
        pygame.display.update()
        laser_group.empty()

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

pygame.quit()
