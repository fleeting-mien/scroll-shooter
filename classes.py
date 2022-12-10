import pygame
from config import *
from random import randint
from random import choice
from numpy import *


powerup_images = {}
'''
powerup_images - Used skins (dictionary)
'''
powerup_images['heal'] = pygame.image.load('images/heal_buff.png')
powerup_images['shield'] = pygame.image.load('images/shield_buff.png')
powerup_images['laser'] = pygame.image.load('images/laser.png')
powerup_images['double_score'] = pygame.image.load('images/coins_buff.png')
powerup_images['double_shot'] = pygame.image.load('images/double_shot.png')
powerup_images['triple_shot'] = pygame.image.load('images/triple_shot.png')

music = {}
'''
music - Used music (dictionary)
'''
music['game1'] = 'OST/game_ost1.mp3'
music['game2'] = 'OST/game_ost2_KoppenAsF.mp3'
music['boss1'] = 'OST/boss_ost1_Hydrophobia.mp3'
music['boss2'] = 'OST/better-call-saul.mp3'



drop_group = pygame.sprite.Group()
'''
drop_group - Group hierarchy
'''
laser_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
ally_bullet_group = pygame.sprite.Group()
enemy_ship_group = pygame.sprite.Group()
ally_ship_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
groups = {laser_group, asteroid_group, enemy_bullet_group, ally_bullet_group, enemy_ship_group, ally_ship_group, drop_group}

# большая группа групп, чтобы по ней можно было итерировать все группы сразу

keys_down = {"w": 0, "a": 0, "s": 0, "d": 0}
'''
keys_down = {"w": 0, "a": 0, "s": 0, "d": 0} - Cловарь, используемый для перемещения игрока
'''

game_state = "game"
# Пока что будут два состояния: "game" когда играем, "gameover" когда мы проиграли.
# Потом сделаем "menu", вместо "game" сделаем уровни и т.д.


class Bullet(pygame.sprite.Sprite):
    """Класс-родитель пуль"""
    def __init__(self, x, y, picture_path, direction, enemy, damage=1, v=1, ):
        """
        Конструктор класса Bullet

        Аргументы:
        picture_path - изображение пули
        x, y - положение пули (в пикселях)
        enemy - True если Enemy, False если Ally

        v (optional) - скорость движения пули (ед. изм. - скорость по умолчанию)
        direction (optional) - направление движения пули (ед. изм. - рад., относ. Ox)
        damage (optional) - сколько урона наносит

        """
        super().__init__()
        self.direction = direction
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.v = v * DEFAULT_SPEED

        self.group = enemy_bullet_group if enemy else ally_bullet_group
        self.group.add(self)

        self.damage = damage

    def update(self):
        """Изменяет положение пули, одновременно перемещая ее изображение"""
        self.y -= self.v * sin(self.direction)  # минус потому что Oy вниз
        self.x += self.v * cos(self.direction)
        self.rect.center = (self.x, self.y)
        if self.x > MAX_X or self.x < 0 or self.y < 0 or self.y > MAX_Y:
            self.group.remove(self)


class Ship(pygame.sprite.Sprite):
    """Класс-родитель кораблей"""
    def __init__(self, x, y, picture_path, enemy, speed=1, lives=1):
        """
        Конструктор класса Ship

        Аргументы:
        picture_path - путь к текстуре корабля
        x, y - положение
        vx, vy - проекции скоростей за тик
        enemy - True если Enemy, False если Ally
        speed (optional) - собственная скорость (ед. изм. - скорость по умолчанию)
        lives (optional) - количество жизней

        """
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        # self.active = active
        self.lives = lives
        self.v = speed * DEFAULT_SPEED

        self.rect.center = (self.x, self.y)

        self.enemy = enemy
        group = enemy_ship_group if enemy else ally_ship_group
        group.add(self)

    def update(self):
        """Функция изменения состояния корабля"""
        self.rect.center = (self.x, self.y)
        self.move()
        self.hit()
        self.update_buffs()

    def move(self):
        """Перемещает корабль (переписан в AllyShip, наследуется EnemyShip)"""
        self.x += self.vx
        self.y += self.vy

    def hit(self):
        """
        Проверка столкновения дружеского корабля с вражескими пулями, и удаление корабля при нулевом количестве жизней
        """
        opposing_bullet_group = ally_bullet_group if self.enemy else enemy_bullet_group
        for bullet in pygame.sprite.spritecollide(self, opposing_bullet_group, True):
            self.lives -= bullet.damage
        for i in pygame.sprite.spritecollide(self, asteroid_group, False):
            self.lives -= 1

    def update_buffs(self):
        """
        Функция обновления состояния баффов, переписана в AllyShip
        """
        pass


class EnemyBullet(Bullet):
    """Класс вражеских пуль"""
    def __init__(self, x, y, direction, picture_path="images/enemy_bullet.png"):
        """
        Конструктор класса EnemyBullet

        Аргументы:
        picture_path - изображение пули
        x, y - положение пули (в пикселях)

        """
        super().__init__(x, y, picture_path, direction, enemy=True)


class EnemyShip(Ship):
    """Класс вражеских кораблей"""
    def __init__(self, picture_path="images/enemy_ship.png"):
        """
        Конструктор класса EnemyShip

        Атрибуты:
        image - изображение корабля
        rect - 'прямоугольник' корабля, хитбокс
        x, y - положение корабля
        vx, vy - скорость его движения
        lives - количество жизней корабля
        active - активность корабля в игре (True - стреляет, False - не стреляет)

        """

        x = randint(BORDER_X, MAX_X - BORDER_X)
        y = randint(BORDER_Y, MAX_Y/2)

        super().__init__(x, y, picture_path, True)

    def update(self):
        """Функция изменения состояния корабля"""
        super().update()
        active = True  # Временная заплатка
        if randint(1, INTENSITY) == 1 and active:
            self.shoot()

    def shoot(self):
        """Корабль стреляет: создает EnemyBullet, вылетающую из корабля"""
        EnemyBullet(x=self.x, y=self.y, direction=-pi/2)

    def hit(self):
        """
        Проверка столкновения вражеского корабля с дружественными пулями, и
        удаление корабля при нулевом количестве жизней
        """
        super().hit()
        for laser in pygame.sprite.spritecollide(self, laser_group, False):
            self.lives -= 1
        if self.lives <= 0:
            if randint(1, DROP_CHANCE) == 1:
                Drop(x=self.x, y=self.y)
            self.kill()
            for ship in ally_ship_group:
                if ship.score_factor.state == "x2":
                    ship.score += 2
                else:
                    ship.score += 1


class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, x, y, picture_path="images/laser_beam.png", damage=1):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.damage = damage

        self.group = laser_group
        self.group.add(self)

    def update(self):
        self.rect.center = (self.x, self.y)

class AllyBullet(Bullet):
    """Класс дружественных пуль"""
    def __init__(self, x, y, direction, picture_path="images/ally_bullet.png"):
        """Конструктор класса AllyBullet

        Аргументы:
        picture_path - изображение пули
        x, y - положение пули (в пикселях)

        """
        super().__init__(x, y,  picture_path, direction, enemy=False)


class AllyShip(Ship):
    """Класс дружеских кораблей (корабля?)"""
    def __init__(self, x=MAX_X/2, y=MAX_Y*3/4, picture_path="images/ally_ship.png"):
        """
        Констурктор класса AllyShip

        Атрибуты:
        image - изображение корабля
        rect - 'прямоугольник' корабля, хитбокс
        x, y - положение корабля
        vx, vy - скорость его движения
        lives - количество жизней корабля
        shooting_num - число, отвечающее за стрельбу корабля.
            Пока равно нулю - стрельба не ведется.
            Пока стрельба ведется, каждый кадр увеличивается на 1
            Далее каждое кратное значение shooting_num производится выстрел
        shield - переменная, отвечающая за то, взят ли щит игроком или нет
        shooting_style - переменная, определяющая то, как в данный момент
            будет стрелять корабль игрока
        score_factor - переменная, отвечающая за множитель очков игрока
        sound - звук выстрела

        """

        super().__init__(x, y, picture_path, False, lives=ALLY_LIVES)
        self.shot_sound = pygame.mixer.Sound('OST/shooting_sound.wav')
        self.laser_sound = pygame.mixer.Sound('OST/laser_effect.wav')
        self.shot_sound.set_volume((0.2))
        self.laser_sound.set_volume((0.4))
        self.shooting_num = 0
        self.shield = Shield("not applied", self)  # 2 состояния: "applied" и "not applied"
        self.shooting_style = Buff("normal")
        self.heal = Buff("not applied")
        # 4 состояния: "normal", "double", "triple", "laser"
        self.score_factor = Buff("x1")  # 2 состояния: "х1" и "х2"
        self.score = 0

    def move(self):
        """Функция перемещения корабля"""
        self.vx = (keys_down["d"] - keys_down["a"]) * self.v
        self.vy = (keys_down["s"] - keys_down["w"]) * self.v

        x = self.x + self.vx  # будущие координаты
        y = self.y + self.vy

        # проверка, не вылез ли корабль наружу экрана
        if x < BORDER_X:
            self.x = BORDER_X
        elif x > MAX_X - BORDER_X:
            self.x = MAX_X - BORDER_X
        else:
            self.x = x

        if y < MAX_Y/2 + BORDER_Y:
            self.y = MAX_Y/2 + BORDER_Y
        elif y > MAX_Y - BORDER_Y:
            self.y = MAX_Y - BORDER_Y
        else:
            self.y = y

    def hit(self):
        """
        Проверка столкновения дружеского корабля с вражескими пулями, и удаление корабля
        при нулевом количестве жизней, а также наложение эффекта баффа
        """
        if self.shield.state == "not applied":
            super().hit()
        else:
            pygame.sprite.spritecollide(self, enemy_bullet_group, True)

        if self.lives <= 0:
            self.lives = 0
            game_over()
        # проверка того, что игрок подобрал бафф
        for drop in pygame.sprite.spritecollide(self, drop_group, True):
            if drop.type == 'shield':
                self.shield.apply("applied", BUFF_DURATION)
            elif drop.type == 'laser':
                self.shooting_style.apply("laser", BUFF_DURATION)
            elif drop.type == 'heal':
                self.lives += 2
                self.heal.apply("applied", 1)
            elif drop.type == 'double_shot':
                self.shooting_style.apply("double", BUFF_DURATION)
            elif drop.type == 'triple_shot':
                self.shooting_style.apply("triple", BUFF_DURATION)
            elif drop.type == 'double_score':
                self.score_factor.apply("x2", BUFF_DURATION)

    def update_buffs(self):
        """Функция, обновляющая состояние баффов игрока"""
        self.shield.update()
        self.shooting_style.update()
        self.score_factor.update()
        self.heal.update()

    def start_shooting(self):
        """Начало стрельбы по нажатию кнопки мыши"""
        self.shooting_num = 1

    def stop_shooting(self):
        """Прекращение стрельбы по отпусканию кнопки мыши"""
        self.shooting_num = 0

    def shooting(self):
        """Собственно стрельба (зависит от SHOOTING_COEF)"""
        if self.shooting_num % SHOOTING_COEF == 1:
            self.shoot()
        if self.shooting_num > 0:
            self.shooting_num += 1
        if self.shooting_style.state == 'laser':
            LaserBeam(x=self.x, y=self.y - 350)
            self.laser_sound.play()


    def shoot(self):
        """
        Корабль стреляет по-разному в зависимости от того,
        какое значение self.shooting_style
        """
        if self.shooting_style.state == "normal":
            self.normal_shot()

        elif self.shooting_style.state == "double":
            self.double_shot()

        elif self.shooting_style.state == "triple":
            self.triple_shot()


    def normal_shot(self):
        """Обычный выстрел"""
        AllyBullet(x=self.x, y=self.y, direction=pi/2)
        self.shot_sound.play()

    # ДРУГИЕ ТИПЫ ВЫСТРЕЛОВ ПОКА НЕ ПРОРАБОТАНЫ
    def double_shot(self):
        """Двойной выстрел"""
        AllyBullet(x=self.x-16, y=self.y, direction=pi/2)
        AllyBullet(x=self.x+16, y=self.y, direction=pi/2)
        self.shot_sound.play()

    def triple_shot(self):
        """Тройной выстрел"""
        AllyBullet(x=self.x, y=self.y, direction=pi/2)
        AllyBullet(x=self.x, y=self.y, direction=pi/2.5)
        AllyBullet(x=self.x, y=self.y, direction=-3.5 * pi/2.5)
        self.shot_sound.play()


def game_over():
    """Функция окончания игры когда игрок был сражен"""
    global game_state
    for group in groups:
        group.empty()
    game_state = "gameover"


class LineEnemy(EnemyShip):
    """Класс врагов, которые не стоят на месте, а двигаются по горизонтальной прямой"""
    def __init__(self):
        """
        Конструктор класса LineEnemy

        Атрибуты:
        a - 'амплитуда', значение, на которое корабль отклоняется от центрального положения
        x0 - положение центра его траектории

        """
        self.a = randint(MAX_X/5, MAX_X/2 - 2*BORDER_X)
        self.x0 = randint(self.a + BORDER_X, MAX_X - self.a - BORDER_X)
        super().__init__(picture_path="images/line_enemy.png")
        self.vx = randint(-300 / FPS, -300 / FPS)
        self.x = self.x0

    def move(self):
        if not (self.x0 - self.a < self.x < self.x0 + self.a):
            self.vx *= -1
        super().move()


class CircleEnemy(EnemyShip):
    """Класс врагов, которые не стоят на месте, а двигаются по окружности"""
    def __init__(self):
        """
        Конструктор класса LineEnemy

        Атрибуты:
        R - радиус окружности, его траектории
        x0, y0 - центр его траектории
        omega - угловая скорость вращение корабля по траектории
        angle - мгновенное значение угла дуги на окружности

        """
        self.R = randint(10, 50)
        self.x0 = randint(self.R + BORDER_X, MAX_X - self.R - BORDER_X)
        self.y0 = randint(self.R + BORDER_Y, MAX_Y/2 - self.R)
        super().__init__(picture_path="images/circle_enemy.png")
        self.omega = choice([3 / FPS, -3 / FPS])
        self.angle = 0
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)

    def move(self):
        self.angle += self.omega
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)


class Asteroid(pygame.sprite.Sprite):
    """Класс астероидов, летящих навстречу игроку"""
    def __init__(self, picture_path="images/asteroid.png", group=asteroid_group):
        """
        Конструктор класса Asteroid

        Атрибуты:
        image - изображение астероида
        rect - 'прямоугольник' астероида, хитбокс
        x, y - положение астероида
        vy - скорость его движения
        lives - количество жизней астероида

        """
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = randint(BORDER_X, MAX_X - BORDER_X)
        self.y = -20

        self.vy = 300 / FPS
        self.lives = 5

        self.rect.center = (self.x, self.y)
        asteroid_group.add(self)

    def move(self):
        """Функция движения астероида"""
        self.y += self.vy

    def hit(self):
        """Функция столкновения астероида с дружественными пулями"""
        for i in pygame.sprite.spritecollide(self, ally_bullet_group, True):
            self.lives -= 1
        for i in pygame.sprite.spritecollide(self, laser_group, False):
            self.lives -= 1
        if self.lives <= 0:
            self.kill()

    def update(self):
        """Функция обновления состояния астероида"""
        self.rect.center = (self.x, self.y)
        self.move()
        self.hit()


class Drop(pygame.sprite.Sprite):
    """Класс того дропа ('плюшек'), который падает с
        поверженных врагов (с некоторой вероятностью)"""
    def __init__(self, x, y, group=drop_group):
        """
        Конструктор класса Drop

        Атрибуты:
        type - тип дропа
        image - изображение дропа
        rect - 'прямоугольник' дропа, хитбокс
        x, y - положение дропа
        vy - скорость его движения
        lives - количество жизней дропа

        """
        super().__init__()
        self.type = random.choice(['shield', 'heal', 'triple_shot', 'double_shot', 'laser', 'double_score'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vy = 300/FPS

        group.add(self)

    def update(self):
        """Обновление положения летящего дропа"""
        self.y += self.vy
        self.rect.center = (self.x, self.y)


class Buff:
    """Класс баффа, которым может обладать корабль игрока"""
    def __init__(self, state):
        """
        Конструктор класса Buff

        Атрибуты:
        timer - значение времени, которое еще бафф будет длиться
        state - переменная состояния баффа
        default_state - значение state по умолчанию (фактически отличает
            разные виды баффов друг от друга)

        """
        self.timer = 0

        self.default_state = state
        """
        shield: "not applied". other states: "applied"
        shooting_style: "normal". other states: "double", "triple", "laser"
        score_factor: "x1". other states: "x2"
        """

        self.state = self.default_state
        """
        shield: "not applied", "applied"
        shooting_style: "normal", "double", "triple", "laser"
        score_factor: "x1", "x2"
        """

    def update(self):
        """Функция того, как 'тикает' таймер баффа"""
        if self.timer > 0:
            self.timer -= 1
        elif self.timer == 0:
            self.state = self.default_state

    def apply(self, state, time):
        """Функция присваивания баффу определенного состояния на определенное время"""
        self.state = state
        self.timer += time * FPS  # время указывается в секундах!


class Shield(Buff):
    def __init__(self, state, ship, picture_path="images/shield.png"):
        super().__init__(state)
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.ship = ship
        self.x, self.y = ship.rect.center

    def update(self):
        super().update()  # updates timer
        if self.state == "applied":
            screen.blit(self.image, self.rect)
            self.x = self.ship.x
            self.y = self.ship.y
            self.rect.center = (self.x, self.y)


class Background:
    def __init__(self, picture_path="images/back.png"):
        global screen
        screen = pygame.display.set_mode((MAX_X, MAX_Y))
        self.image = pygame.image.load(picture_path)
        self.x = 0
        self.y = -2400
        self.vy = 2

    def update(self):
        self.y += self.vy
        if self.y == 0:
            self.y = -2400
        screen.blit(self.image, (self.x, self.y))


class AboutInfo:
    def __init__(self, picture_path="images/test_about.jpg"):
        global screen
        screen = pygame.display.set_mode((MAX_X, MAX_Y))
        self.image = pygame.image.load(picture_path)
        self.x = 50
        self.y = 125

    def update(self):
        screen.blit(self.image, (self.x, self.y))


class Boss(EnemyShip):
    def __init__(self, font):
        super().__init__(picture_path='images/boss.png')
        self.x0 = MAX_X/2  # серединка восьмерки
        self.y0 = MAX_Y/6
        self.R = 100
        self.omega = 3 / FPS
        self.angle = 0
        self.x = self.x0 + self.R * (-1 + cos(self.angle))
        self.y = self.y0 + self.R * sin(self.angle)
        self.lives = BOSS_LIVES
        self.font = font

    def move(self):
        if 0 <= self.angle < 2*pi:
            self.angle += self.omega
            self.x = self.x0 + self.R * (1 - cos(self.angle))
            self.y = self.y0 + self.R * sin(self.angle)
        elif 2*pi <= self.angle < 4*pi:
            self.angle += self.omega
            self.x = self.x0 + self.R * (-1 + cos(-self.angle))
            self.y = self.y0 + self.R * sin(self.angle)
        elif self.angle >= 4*pi:
            self.angle = 0

    def shoot(self):
        if randint(1, 40) == 1:
            BossBullet(x=self.x, y=self.y, direction=-pi / 2,
                       image=pygame.image.load("images/pelmen.png"), damage=5)
        else:
            BossBullet(x=self.x, y=self.y, direction=-pi/2,
                       image=pygame.image.load("images/boss_bullet.png"), damage=3)

    def update(self):
        self.rect.center = (self.x, self.y)
        self.move()
        self.hit()
        self.health_bar()
        if randint(1, INTENSITY) == 1:
            self.shoot()

    def health_bar(self):
        pygame.draw.rect(screen, (127, 255, 0), [100, 10, 400, 20])
        pygame.draw.rect(screen, (255, 0, 0), [500 - 400*((100 - self.lives)/100), 10, 400*((100 - self.lives)/100), 20])
        healthbar = self.font.render(
            str(self.lives),
            True, (0, 0, 0)
        )
        screen.blit(healthbar, (300, 5))



class BossBullet(EnemyBullet):
    def __init__(self, x, y, direction, image, damage):
        super().__init__(x, y, direction)
        self.damage = damage
        self.phase = 0
        self.omega = self.omega = choice([20 / FPS, -20 / FPS])
        self.image = image

    def update(self):
        """Изменяет положение пули, одновременно перемещая ее изображение"""
        self.phase += self.omega
        self.y += self.v  # минус потому что Oy вниз
        self.x += self.v * cos(self.phase)
        self.rect.center = (self.x, self.y)
        if self.x > MAX_X or self.x < 0 or self.y < 0 or self.y > MAX_Y:
            self.group.remove(self)
