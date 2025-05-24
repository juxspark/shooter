from pygame import *
from random import randint

lost = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= 3
        if keys[K_d]:
            self.rect.x += 3
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if  self.rect.y > 700:
            self.rect.x = randint(80, 500 - 80)
            self.rect.y = 0
            lost = lost + 1

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 500-80), 40, randint(1, 5))
    monsters.add(monster)


font.init()
font1 = font.SysFont('Arial', 36)
text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255,255))




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 700:
            self.rect.x = randint(80, 500 - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


FPS = 60
window = display.set_mode((700, 500))
display.set_caption('Maze')
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
player = Player('rocket.png', 350, 420, 4)
# enemy = Enemy('ufo.png', 300, 250, 4)
game = True
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bullets = sprite.Group()
finish = False
score = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if not finish:
        window.blit(background,(0,0)) 
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (2,2))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        # enemy.reset()
        # enemy.update()
        clock.tick(FPS)

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprites_list:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 500-80), 40, randint(1, 5))
            monsters.add(monster)
        win = font1.render('YOU WIN', True, (255, 255, 255))
        if score >= 30:
            finish = True
            window.blit(win, (200, 200))
        lose = font1.render('YOU LOSE', True, (255, 255, 255))
        if lost > 3:
            finish = True
            window.blit(lose, (200, 200))
        display.update()

