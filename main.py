import pygame
from pygame import *

W = 800
H = 640
BACKGROUND_COLOR = "#9996AF"
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#9977BF"
WIDTH = 22
HEIGHT = 32
COLOR = "#665AD5"
MOVE_SPEED = 7
JUMP_POWER = 10
GRAVITY = 0.35


def draw_text(screen, score, lifes, timer):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f'Очки: {score}', True, (0, 0, 0))
    lifes_text = font.render(f'Жизни: {lifes}', True, (0, 0, 0))
    timer_text = font.render(f'Таймер: {timer}(не больше 1000)', True, (0, 0, 0))
    screen.blit(score_text, (30, 10))
    screen.blit(lifes_text, (150, 10))
    screen.blit(timer_text, (270, 10))


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.OnGround = False
        self.startX = x
        self.startY = y
        self.score = 0
        self.lifes = 3
        self.timer = 0
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update(self, left, right, up, platforms, enemies, coins):
        self.timer += 1
        if self.timer > 1000 or self.score == 10 or self.lifes == 0:
            if self.score == 10:
                print("you win")
            else:
                print("You lose")
            exit()
        if up:
            if self.OnGround:
                self.yvel = -JUMP_POWER
        if left:
            self.xvel = -MOVE_SPEED
        if right:
            self.xvel = MOVE_SPEED
        if not (left or right):
            self.xvel = 0
        if not self.OnGround:
            self.yvel += GRAVITY
        self.OnGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, enemies, coins)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, enemies, coins)

    def collide(self, xvel, yvel, platforms, enemies, coins):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.OnGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
        for e in enemies:
            if sprite.collide_rect(self, e):
                if self.lifes > 0:
                    self.lifes -= 1
                    enemies.remove(e)
        for c in coins:
            if sprite.collide_rect(self, c):
                self.score += 1
                coins.remove(c)

    def draw_text(self, screen):
        draw_text(screen, self.score, self.lifes, self.timer)


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(PLATFORM_COLOR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Enemy(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color('red'))
        self.rect = Rect(x, y, WIDTH, HEIGHT)


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
        self.image.fill(pygame.Color('yellow'))
        self.rect = Rect(x, y, PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2)


def main():
    entities = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    platforms = []
    hero = Player(55, 55)
    up = False
    left = right = False
    entities.add(hero)
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    bg = Surface((W, H))
    bg.fill(BACKGROUND_COLOR)
    level = ['-------------------------',
             '-                       -',
             '------                  -',
             '-         E  C          -',
             '-        -------        -',
             '-   C                C  -',
             '-                   -----',
             '-       C   E           -',
             '-     ---------       C -',
             '-                  E    -',
             '----               ------',
             '-      C                -',
             '-                       -',
             '-  C         C          -',
             '-        -------        -',
             '-                     C -',
             '-  C                -----',
             '--------                -',
             '-                       -',
             '-------------------------']
    timer = pygame.time.Clock()
    x = y = 0
    for row in level:
        for col in row:
            if col == '-':
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == 'E':
                e = Enemy(x, y)
                enemies.add(e)
            elif col == 'C':
                c = Coin(x, y)
                coins.add(c)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0
    while 1:
        timer.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                raise SystemExit
            elif event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            elif event.type == KEYDOWN and event.key == K_UP:
                up = True
            elif event.type == KEYUP and event.key == K_LEFT:
                left = False
            elif event.type == KEYUP and event.key == K_RIGHT:
                right = False
            elif event.type == KEYUP and event.key == K_UP:
                up = False
        screen.blit(bg, (0, 0))
        hero.update(left, right, up, platforms, enemies, coins)
        entities.draw(screen)
        enemies.draw(screen)
        coins.draw(screen)
        hero.draw_text(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
