import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 32

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)

imgBrick = pygame.image.load('images/block_brick.png')
imgCannabis = pygame.image.load('images/cannabis.png')
imgTanks = [
    pygame.image.load('images/Hunter.png'),
    pygame.image.load('images/Hunter.png'),
    pygame.image.load('images/Hunter.png'),
    pygame.image.load('images/Hunter.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png')
    ]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png')
    ]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        # for object in objects:
        #     if object.type == 'tank':
        #         pygame.draw.rect(window, object.color, (5 + i * 70, 5, 22, 22))
        #         text = fontUI.render(str(object.hp), True, object.color)
        #         rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
        #         window.blit(text, rect)
        #         i += 1


class Tank:
    def __init__(self, color, px, py, direct, key_list):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5

        self.bulletSpeed = 5
        self.bulletDamage = 1
        self.shotTimer = 0
        self.shotDelay = 60

        self.keyLEFT = key_list[0]
        self.keyRIGHT = key_list[1]
        self.keyUP = key_list[2]
        self.keyDOWN = key_list[3]
        self.keySHOT = key_list[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

        # AI variables
        self.ran_move = 1
        self.movement_count = 0
        self.vision = pygame.Rect(0, 0, 300, 20)
        self.angle = 0

    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height()
                                                                  - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        oldX, oldY = self.rect.topleft

        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for object in objects:
            if object != self and object.type == 'block' and self.rect.colliderect(object.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for object in objects:
                if object != self.parent and object.type != 'bang' and object.rect.collidepoint(self.px, self.py):
                    object.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


class Cannabis:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'cannabis'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        window.blit(imgCannabis, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


bullets = []
objects = []
Tank('blue', 350, 570, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
# Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
Cannabis(350, 0, TILE)
ui = UI()

for _ in range(170):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        found = False
        for object in objects:
            if rect.colliderect(object.rect):
                found = True

        if not found:
            break

    Block(x, y, TILE)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for object in objects:
        object.update()
    for bullet in bullets:
        bullet.update()
    ui.update()

    window.fill('black')

    for object in objects:
        object.draw()
    for bullet in bullets:
        bullet.draw()
    ui.draw()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()