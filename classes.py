import pygame
from config import *
from random import randint

enemy_bullet_group = pygame.sprite.Group()
ally_bullet_group = pygame.sprite.Group()
enemy_ship_group = pygame.sprite.Group()
ally_ship_group = pygame.sprite.Group()
groups = {enemy_bullet_group, ally_bullet_group, enemy_ship_group, ally_ship_group}

keys_down = {"w": 0, "a": 0, "s": 0, "d": 0}


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, picture_path="images/enemy_bullet.png", x=MAX_X/2, y=MAX_Y*1/4, group=enemy_bullet_group):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        # self.rect.center = enemy.rect.center
        self.vy = 20    # Можно добавить ползунок сложности и менять значение скорости вражеских пуль
        group.add(self)

    def update(self):
        self.y += self.vy
        self.rect.center = (self.x, self.y)


class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, picture_path="images/enemy_ship.png", x=MAX_X/2, y=MAX_Y/4, group=enemy_ship_group):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.rect.center = (self.x, self.y)
        group.add(self)

    def update(self):
        self.rect.center = (self.x, self.y)
        self.move()
        if randint(1, 100) == 100:
            self.shoot()

    def move(self):  # for inheritance purposes
        self.x += self.vx
        self.y += self.vy

    def shoot(self):
        EnemyBullet(x=self.x, y=self.y)


class AllyBullet(pygame.sprite.Sprite):  # зачем мы сидели планировали классы? всё равно по-другому вышло
    def __init__(self, picture_path="images/ally_bullet.png", x=MAX_X/2, y=MAX_Y*3/4, group=ally_bullet_group):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        # self.rect.center = ally.rect.center ???
        self.vy = 20
        group.add(self)

    def update(self):
        self.y -= self.vy
        self.rect.center = (self.x, self.y)


class AllyShip(pygame.sprite.Sprite):
    def __init__(self, picture_path="images/ally_ship.png", x=MAX_X/2, y=MAX_Y*3/4):
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

        self.rect.center = (self.x, self.y)
        if self.lives == 0:
            game_over()
        self.move()
        self.hit()

    def move(self):
        self.vx = (keys_down["d"] - keys_down["a"]) * self.v
        self.vy = (keys_down["s"] - keys_down["w"]) * self.v

        x = self.x + self.vx  # будущие координаты
        y = self.y + self.vy

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
        global enemy_bullet_group
        for i in pygame.sprite.spritecollide(self, enemy_bullet_group, True):
            self.lives -= 1

    def shoot(self):
        AllyBullet(x=self.x, y=self.y)


def game_over():
    pass

    # очищаются группы пуль и кораблей
    # прекращаются игровые процессы
    # вылезает менюшка

    # for group in groups:
    #     group.empty()
    # game_state = "gameover"


class LineEnemy(EnemyShip):
    def __init__(self, x=MAX_X/2, y=MAX_Y/4, speed=10, amplitude=MAX_X/3, center=MAX_X/2):
        super().__init__(x=x, y=y)  # picture_path="line_enemy.png"
        self.vx = speed
        self.a = amplitude
        self.x0 = center

    def move(self):
        if not (self.x0 - self.a < self.x < self.x0 + self.a):
            self.vx *= -1
        super().move()


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
