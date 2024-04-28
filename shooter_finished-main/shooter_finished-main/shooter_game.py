from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "nochnoe-nebo-izmenilos-i-uchenye-ne-znajut-pochemu-ba1b2a1.jpg"
img_hero = "klipartz.com.png"
img_enemy = "ufo.png"
img_ast = "asteroid.png"
img_health = "pngwing.com.png"
#new_bullet_img = "bul.png"
score = 0
lost = 0
goal = 10
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        self.shoot_frequency = randint(1, 20)
        self.last_shot_time = timer()
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0
            lost +=1

    def shoot(self):
        now_time = timer()
        if now_time - self.last_shot_time > self.shoot_frequency:
            self.last_shot_time = now_time
            bullet = EnemyBullet("bullet.png", self.rect.centerx, self.rect.bottom, 10, 20, 5)
            enemy_bullets.add(bullet)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0

class HealthPack(GameSprite):
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0
    
    def apply(self, player):
        global life
        if sprite.collide_rect(self, player):
            life += 1
            self.kill()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

class EnemyBullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.speed = -sprite_speed
        if self.rect.y > 500:
            self.kill()

#class NewBullet(GameSprite):
#    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
#        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
enemy_bullets = sprite.Group()

health_pack = HealthPack(img_health, randint(30, win_width - 30), -40, 30, 30, randint(1, 5))
health_packs = sprite.Group()
health_packs.add(health_pack)

#new_bullet = NewBullet(new_bullet_img, ship.rect.centerx, ship.rect.top, 15, 20, -15)
#bullets.add(new_bullet)

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)
for i in range(1, 3):
    asteroid = Asteroid(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

run = True
finish = False
clock = time.Clock()
FPS = 30
rel_time = False  # прапор, що відповідає за перезаряджання
num_fire = 0  # змінна для підрахунку пострілів    


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish: ###
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                   
                if num_fire >= 5 and rel_time == False : #якщо гравець зробив 5 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки


    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        enemy_bullets.update()
        enemy_bullets.shoot()
        
        health_packs.update()
        health_packs.draw(window)

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        enemy_bullets.draw(window)

        if rel_time == True:
            now_time = timer() # зчитуємо час
            if now_time - last_time < 2: #поки не минуло 2 секунди виводимо інформацію про перезарядку
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (win_width/2-200, win_height-100))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки


        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)


        # # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        # if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
        #     finish = True # програли, ставимо тло і більше не керуємо спрайтами.
        #     window.blit(lose, (200, 200))
        
        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

        for health_pack in health_packs:
            health_pack.apply(ship)

        #програш
        if life == 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))


        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font1.render("Рахунок: " + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))
        display.update()

    clock.tick(FPS)