from pygame import *
from random import randint 
win_x = 700
win_y = 500
window = display.set_mode((win_x, win_y))
display.set_caption('Шахматы онлайн')
background = transform.scale(image.load('galaxy.jpg'),(win_x, win_y))

scor = 0
lost = 0
font.init()
font1 = font.Font(None, 36)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

kick = mixer.Sound('fire.ogg')

game = True
finish = False

font.init()
font = font.Font(None, 70)

game_win = font.render('YOU WIN!', True, (255, 215, 0))

game_lose = font.render('YOU LOSE!', True, (255, 215, 0))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), ( 50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)  
        kick.play() 

    def update(self):
        keys = key.get_pressed() 
        if (keys[K_s] or keys[K_DOWN]) and self.rect.y < win_y - 80:
            self.rect.y += self.speed
        if (keys[K_w] or keys[K_UP]) and self.rect.y > 5:
            self.rect.y -= self.speed
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < win_x - 80:
            self.rect.x += self.speed
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >  win_y:
            self.rect.x = randint(80, win_y -80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill() 


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >  win_y:
            self.rect.x = randint(80, win_y -80)
            self.rect.y = 0

bullets = sprite.Group()

asteroids = sprite.Group()

monsters = sprite.Group()

for i in range(1, 5):
    monster = Enemy('ufo.png', randint(80, win_x - 80), -40, randint(1, 2))
    monsters.add(monster)

for i in range(2, 3):
    asteroid = Asteroid('asteroid.png', randint(80, win_x - 80), -40, randint(1, 1))
    asteroids.add(asteroid)


player = Player('rocket.png', win_x/2, win_y - 80, 10)

clock = time.Clock()
FPS = 120

win = 0

live = 5

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()


    if not finish:
        window.blit(background, (0, 0))

        for i in sprite.groupcollide(monsters, bullets, True, True):
            scor += 1
            monster = Enemy('ufo.png', randint(80, win_x - 80), -40, randint(1, 2))
            monsters.add(monster)

        if sprite.spritecollide(player, monsters, True):
            live -=1
            monster = Enemy('ufo.png', randint(80, win_x - 80), -40, randint(1, 2))

        if sprite.spritecollide(player, asteroids, True):
            finish = True
            window.blit(game_lose, (175, 125))


        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()

        text = font1.render('Счёт: ' + str(scor),  1, (255, 255, 255))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))

        if scor >= 20:
            finish = True
            window.blit(game_win, (175, 125))

        if lost >= 5:
            finish = True
            window.blit(game_lose, (175, 125))            

        if live <=0:
            finish = True
            window.blit(game_lose, (175, 125))


        window.blit(text_lose, (10, 50))
        window.blit(text, (10, 15))

    display.update()
    clock.tick(FPS)
