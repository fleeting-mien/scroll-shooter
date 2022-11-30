import pygame
from config import *

enemy_bullet_group = pygame.sprite.Group()
ally_bullet_group = pygame.sprite.Group()
enemy_ship_group = pygame.sprite.Group()
ally_ship_group = pygame.sprite.Group()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, picture_path="images/enemy_bullet.png", x=MAX_X/2, y=MAX_Y*1/4, group = enemy_bullet_group):
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
    def __init__(self, picture_path="enemy_ship.png", x=MAX_X/2, y=MAX_Y/4, group=enemy_ship_group):
        super().__init__(picture_path)
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        group.add(self)


class AllyBullet(pygame.sprite.Sprite):  # зачем мы сидели планировали классы? всё равно по-другому вышло
    def __init__(self, picture_path="ally_bullet.png", x=MAX_X/2, y=MAX_Y*3/4, group=ally_bullet_group):
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
    def __init__(self, picture_path, x=MAX_X/2, y=MAX_Y*3/4):
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
        # self.rect.center = pygame.mouse.get_pos()
        self.rect.center = (self.x, self.y)
        if self.lives == 0:
            die()
        self.move()
        self.hit()

    def move(self):
        if self.x <= 0 and self.vx < 0:
            self.x = 0
        elif self.x >= MAX_X and self.vx > 0:
            self.x = MAX_X
        elif self.y <= MAX_Y/2 and self.vy > 0:
            self.y = MAX_Y/2
        elif self.y >= MAX_Y and self.vy < 0:
            self.y = MAX_Y
        else:
            self.x += self.vx
            self.y -= self.vy

    def hit(self):
        global enemy_bullet_group
        for i in pygame.sprite.spritecollide(self, enemy_bullet_group, True):
            self.lives -= 1

    def shoot(self):
        AllyBullet("images/ally_bullet.png", self.x, self.y)

    def react_on_keys(self, event):  # команда для перемещения по нажатию клавиатуры
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.vx = self.v
            elif event.key == pygame.K_a:
                self.vx = -self.v
            elif event.key == pygame.K_w:
                self.vy = self.v
            elif event.key == pygame.K_s:
                self.vy = -self.v
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                self.vx = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                self.vy = 0


def die():
    pass
    # очищаются группы пуль и кораблей
    # прекращаются игровые процессы
    # вылезает менюшка


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
