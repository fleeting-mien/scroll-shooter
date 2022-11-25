import pygame, sys


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()

    def update(self):
        # Пока хз
        pass


class Ship(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

pygame.init()
clock = pygame.time.Clock()

bullet = Bullet("pixil-frame-0 (1).png")
bullet_group = pygame.sprite.Group()
bullet_group.add(bullet)

background = pygame.image.load("Space (1).jpg")

ship = Ship("pixil-frame-0 (2).png")
ship_group = pygame.sprite.Group()
ship_group.add(ship)

screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, (0,0))
    ship_group.draw(screen)
    ship_group.update()
    pygame.display.update()





class Ally(Ship):
    pass


class Enemy(Ship):
    pass


class Scene:  # ?
    pass


class Game_over_screen:  # ?
    pass
