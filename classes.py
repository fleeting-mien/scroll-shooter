import pygame
import sys

enemy_bullet_group = pygame.sprite.Group()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()


class Enemy(Bullet):
    def __init__(self):
        super().__init__(self)
        self.rect.center = enemy.rect.center
        self.vy = 20    # Можно добавить ползунок сложности и менять значение скорости вражеских пуль

    def create(self):
        new_enemy_bullet = Enemy("pixil-frame-0 (1).png")
        enemy_bullet_group.add(new_enemy_bullet)

    def update(self):
        self.rect.top -= 20

    def hittest(self):
        pass


class Ship(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.x = self.rect.left
        self.y = self.rect.top



class Ally(Ship):

    def shoot(self):
        global ally_bullets
        new_bullet = Bullet("pixil-frame-0 (1).png")


    def update(self):
        self.rect.center = pygame.mouse.get_pos()


pygame.init()
clock = pygame.time.Clock()
print(enemy_bullet_group)



background = pygame.image.load("Space (1).jpg")

ally_ship = Ally("pixil-frame-0 (3).png")
ship_group = pygame.sprite.Group()
ship_group.add(ally_ship)

screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.mouse.set_visible(False)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, (0,0))
    ship_group.draw(screen)
    ship_group.update()
    pygame.display.update()

class Scene:  # ?
    pass


class Game_over_screen:  # ?
    pass
