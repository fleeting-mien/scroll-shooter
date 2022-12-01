import pygame
from config import *
from random import randint
from random import choice
from numpy import *

enemy_bullet_group = pygame.sprite.Group()
ally_bullet_group = pygame.sprite.Group()
enemy_ship_group = pygame.sprite.Group()
ally_ship_group = pygame.sprite.Group()
groups = {enemy_bullet_group, ally_bullet_group, enemy_ship_group, ally_ship_group}
#большая группа групп, чтобы по ней можно было итерировать все группы сразу

keys_down = {"w": 0, "a": 0, "s": 0, "d": 0}
# словарь, используемый для перемещения игрока

game_state = "game"
# Пока что будут два состояния: "game" когда играем, "gameover" когда мы проиграли.
# Потом сделаем "menu", вместо "game" сделаем уровни и т.д.


class EnemyBullet(pygame.sprite.Sprite):
    """Класс вражеских пуль"""
    def __init__(self, picture_path="images/enemy_bullet.png", x=MAX_X/2, y=MAX_Y*1/4, group=enemy_bullet_group):
        """Конструктор класса EnemyBullet

        Атрибуты:
        image - изображение пули
        rect - 'прямоугольник' пули, хитбокс
        x, y - положение пули
        vy - скорость ее движения

        """
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.vy = 20  # Можно добавить ползунок сложности и менять значение скорости вражеских пуль
        group.add(self)

    def update(self):
        """Изменяет положение пули, одновременно перемещая ее изображение"""
        self.y += self.vy
        self.rect.center = (self.x, self.y)


class EnemyShip(pygame.sprite.Sprite):
    """Класс вражеских кораблей"""
    def __init__(self, picture_path="images/enemy_ship.png", group=enemy_ship_group):
        """Констурктор класса EnemyShip

        Атрибуты:
        image - изображение корабля
        rect - 'прямоугольник' корабля, хитбокс
        x, y - положение корабля
        vx, vy - скорость его движения
        lives - количество жизней корабля

        """
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = randint(BORDER_X, MAX_X - BORDER_X)
        self.y = randint(BORDER_Y, MAX_Y/2)

        self.vx = 0
        self.vy = 0
        self.lives = 1

        self.rect.center = (self.x, self.y)
        group.add(self)

    def update(self):
        """Функция изменения состояния корабля"""
        self.rect.center = (self.x, self.y)
        self.move()
        self.hit()
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


class AllyBullet(pygame.sprite.Sprite):  # зачем мы сидели планировали классы? всё равно по-другому вышло
    """Класс дружественных пуль"""
    def __init__(self, picture_path="images/ally_bullet.png", x=MAX_X/2, y=MAX_Y*3/4, group=ally_bullet_group):
        """Конструктор класса AllyBullet

        Атрибуты:
        image - изображение пули
        rect - 'прямоугольник' пули, хитбокс
        x, y - положение пули
        vy - скорость ее движения

        """
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.vy = 20
        group.add(self)

    def update(self):
        """Изменяет положение пули, одновременно перемещая ее изображение"""
        self.y -= self.vy
        self.rect.center = (self.x, self.y)


class AllyShip(pygame.sprite.Sprite):
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
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.v = 20
        self.vx = 0
        self.vy = 0
        self.lives = 3
        ally_ship_group.add(self)

    def update(self):
        """Функция изменения состояния корабля"""
        self.move()
        self.rect.center = (self.x, self.y)
        self.hit()

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
        self.vx = randint(-10, 10)
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
        self.omega = choice([0.1, -0.1])
        self.angle = 0
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)

    def move(self):
        self.angle += self.omega
        self.x = self.x0 + self.R * cos(self.angle)
        self.y = self.y0 + self.R * sin(self.angle)


# Старый код, который Миша попросил закомментить но не убирать. Не уверен что с последними
# обновлениями он всё еще работает
#
# pygame.init()
# clock = pygame.time.Clock()
# print(type(enemy_bullet_group), enemy_bullet_group)
#
# enemy = EnemyBullet("enemy_bullet.png")
# enemy.create()
#
# background = pygame.image.load("background.jpg")
#
# ally_ship = AllyShip("ally_ship.png")
# ship_group = pygame.sprite.Group()
# ship_group.add(ally_ship)
# ship = AllyShip("ally_ship.png")
# screen_width = 600
# screen_height = 700
# screen = pygame.display.set_mode((screen_width, screen_height))
# enemy_bullet = EnemyBullet("enemy_bullet.png")
# pygame.mouse.set_visible(False)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         elif event.type == pygame.KEYDOWN:
#            ally_ship.evolve(event)
#     screen.blit(background, (0,0))
#     ship.hit()
#     if randint(1, 10000) == 10:
#         enemy_bullet.create()
#     enemy_bullet_group.draw(screen)
#     ship_group.draw(screen)
#     ship_group.update()
#     pygame.display.update()
#     print(ship.lives)
