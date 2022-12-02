import pygame
from config import *
from random import randint
from random import choice
from numpy import *

import math

enemy_bullet_group = pygame.sprite.Group()
ally_bullet_group = pygame.sprite.Group()
enemy_ship_group = pygame.sprite.Group()
ally_ship_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
groups = {asteroid_group, enemy_bullet_group, ally_bullet_group, enemy_ship_group, ally_ship_group}
# большая группа групп, чтобы по ней можно было итерировать все группы сразу

keys_down = {"w": 0, "a": 0, "s": 0, "d": 0}
# словарь, используемый для перемещения игрока

game_state = "game"
# Пока что будут два состояния: "game" когда играем, "gameover" когда мы проиграли.
# Потом сделаем "menu", вместо "game" сделаем уровни и т.д.


class Bullet(pygame.sprite.Sprite):
    """Класс-родитель пуль"""
    def __init__(self, picture_path, x, y, enemy, damage=1, v=1, direction=None):
        """Конструктор класса Bullet

        Аргументы:
        picture_path - изображение пули
        x, y - положение пули (в пикселях)
        enemy - True если Enemy, False если Ally

        v (optional) - скорость движения пули (ед. изм. - скорость по умолчанию)
        direction (optional) - направление движения пули (ед. изм. - рад., относ. Ox)
        damage (optional) - сколько урона наносит (пока не влияет)

        """
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.v = v * DEFAULT_SPEED

        if direction is None:
            self.direction = -pi / 2 if enemy else pi / 2
        else:
            self.direction = direction

        group = enemy_bullet_group if enemy else ally_bullet_group
        group.add(self)

        self.damage = damage

    def update(self):
        """Изменяет положение пули, одновременно перемещая ее изображение"""
        self.y -= self.v * sin(self.direction)  # минус потому что Oy вниз
        self.x += self.v * cos(self.direction)
        self.rect.center = (self.x, self.y)


class Ship(pygame.sprite.Sprite):
    """Класс-родитель кораблей"""
    def __init__(self, picture_path, x, y, enemy, speed=1, lives=1):
        """Констурктор класса Ship

        Аргументы:
        picture_path - путь к текстурке корабля
        x, y - положение
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

        self.lives = lives
        self.v = speed * DEFAULT_SPEED

        self.rect.center = (self.x, self.y)

        group = enemy_ship_group if enemy else ally_ship_group
        group.add(self)

    def update(self):
        """Функция изменения состояния корабля"""
        self.rect.center = (self.x, self.y)
        self.move()
        self.hit()

class EnemyBullet(Bullet):
    """Класс вражеских пуль"""
    def __init__(self, picture_path="images/enemy_bullet.png", x=MAX_X/2, y=MAX_Y*1/4):
        """Конструктор класса EnemyBullet

        Аргументы:
        picture_path - изображение пули
        x, y - положение пули (в пикселях)

        """
        super().__init__(picture_path, x, y, enemy=True)


class EnemyShip(Ship):
    """Класс вражеских кораблей"""
    def __init__(self, picture_path="images/enemy_ship.png"):
        """Констурктор класса EnemyShip

        Атрибуты:
        image - изображение корабля
        rect - 'прямоугольник' корабля, хитбокс
        x, y - положение корабля
        vx, vy - скорость его движения
        lives - количество жизней корабля

        """

        x = randint(BORDER_X, MAX_X - BORDER_X)
        y = randint(BORDER_Y, MAX_Y/2)

        super().__init__(picture_path, x, y, True)

    def update(self):
        """Функция изменения состояния корабля"""
        super().update()
        if randint(1, INTENSITY) == 1:
            self.shoot()

    def move(self):  # for inheritance purposes
        """Перемещает корабль"""
        self.x += self.vx
        self.y += self.vy

    def shoot(self):
        """Корабль стреляет: создает EnemyBullet, вылетающую из корабля"""
        EnemyBullet(x=self.x, y=self.y)

    def hit(self):
        """Проверка столкновения вражеского корабля с дружественными пулями, и удаление корабля
        при нулевом количестве жизней"""
        for i in pygame.sprite.spritecollide(self, ally_bullet_group, True):
            self.lives -= 1
        if self.lives <= 0:
            self.kill()


class AllyBullet(Bullet):
    """Класс дружественных пуль"""
    def __init__(self, picture_path="images/ally_bullet.png", x=MAX_X/2, y=MAX_Y*3/4):
        """Конструктор класса AllyBullet

        Аргументы:
        picture_path - изображение пули
        x, y - положение пули (в пикселях)

        """
        super().__init__(picture_path, x, y, enemy=False)


class AllyShip(Ship):
    """Класс дружеских кораблей (корабля?)"""
    def __init__(self, picture_path="images/ally_ship.png", x=MAX_X/2, y=MAX_Y*3/4):
        """Констурктор класса AllyShip

        Атрибуты:
        image - изображение корабля
        rect - 'прямоугольник' корабля, хитбокс
        x, y - положение корабля
        vx, vy - скорость его движения
        lives - количество жизней корабля

        """

        super().__init__(picture_path, x, y, False, lives=3)

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
        """Проверка столкновения дружеского корабля с вражескими пулями, и удаление корабля
            при нулевом количестве жизней"""
        for i in pygame.sprite.spritecollide(self, enemy_bullet_group, True):
            self.lives -= 1
        for i in pygame.sprite.spritecollide(self, asteroid_group, True):
            self.lives -= 1
        if self.lives <= 0:
            game_over()

    def shoot(self):
        """Корабль стреляет: создает EnemyBullet, вылетающую из корабля"""
        AllyBullet(x=self.x, y=self.y)


def game_over():
    global game_state
    for group in groups:
        group.empty()
    game_state = "gameover"


class LineEnemy(EnemyShip):
    """Класс врагов, которые не стоят на месте, а двигаются по горизонтальной прямой"""
    def __init__(self):
        """Конструктор класса LineEnemy

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
        """Конструктор класса LineEnemy

        Атрибуты:
        R - радиус окружности, его траектории
        x0, y0 - центр его траектории
        omega - угловая скорость вращение корабля по траектории
        angle - мгновенное значение угла дуги на окружности

        """
        self.R = randint(10, 50)
        self.x0 = randint(self.R + BORDER_X, MAX_X - self.R - BORDER_X)
        self.y0 = randint(self.R + BORDER_Y, MAX_Y/2 - self.R)
        super().__init__(picture_path="images/line_enemy.png")
        self.omega = choice([3 / FPS, -3 / FPS])
        self.angle = 0
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)

    def move(self):
        self.angle += self.omega
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, picture_path="images/ally_ship.png", group=asteroid_group):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = randint(BORDER_X, MAX_X - BORDER_X)
        self.y = -20

        self.vy = 300 / FPS
        self.lives = 5

        self.rect.center = (self.x, self.y)
        group.add(self)

    def move(self):
        self.y += self.vy

    def hit(self):
        for i in pygame.sprite.spritecollide(self, ally_bullet_group, True):
            self.lives -= 1
        if self.lives <= 0:
            self.kill()

    def update(self):
        self.rect.center = (self.x, self.y)
        self.move()
        self.hit()
