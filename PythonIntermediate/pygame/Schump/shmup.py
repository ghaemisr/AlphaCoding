import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img', 'PNG')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = int(WIDTH / 2)
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.radius=20
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks()- self.hide_timer >1000:
            self.hidden = False
            self.rect.centerx = int(WIDTH/2)
            self.rect.bottom = HEIGHT - 10
            
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (int(WIDTH/2), HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(loaded_meteors)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 *0.85)
        self.go_to_top()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.go_to_top()

    def go_to_top(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.frame = 0
        self.image = explosion_animation[self.size][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animation[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animation[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'killer'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class pow_effect(pygame.sprite.Sprite):
    def __init__(self, pow_type):
        pygame.sprite.Sprite.__init__(self)
        self.type = pow_type
        self.image = shield_effects[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.start_timer = pygame.time.get_ticks()
        self.radius = 30
        self.kill_timer = pygame.time.get_ticks()

    def update(self):
        global effects
        self.rect.center = player.rect.center
        if pygame.time.get_ticks() - self.start_timer > 5000:
            effects = None
            self.kill()
        if self.type == 'killer' and pygame.time.get_ticks() - self.kill_timer > 1000:
            self.kill_timer = pygame.time.get_ticks()
            player.shield -= 10
            if player.shield <= 0 :
                player_expl = Explosion(hit.rect.center, 'player')
                all_sprites.add(player_expl)
                player.hide()
                player.lives -= 1
                player.shield = 100
            if player.lives == 0:
                running = False
            

font_name=pygame.font.match_font('arial')
def draw_text(surf,text,size,x,y):
     font=pygame.font.Font(font_name,size)
     text_surface=font.render(text,True,WHITE)
     text_rect=text_surface.get_rect()
     text_rect.midtop =(int(x),int(y))
     surf.blit(text_surface,text_rect)

def draw_shield_bar(surf, x, y, amount_left):
    if amount_left < 0:
        amount_left = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (amount_left /100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, int(fill), BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'playerShip1_blue.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

meteors_list = ['meteorBrown_big2.png', 'meteorBrown_big4.png', 'meteorBrown_med3.png', 'meteorBrown_tiny2.png']
loaded_meteors = []
for meteor in meteors_list:
    loaded_meteors.append(pygame.image.load(path.join(img_dir, 'Meteors', meteor)).convert())
    
bullet_img = pygame.image.load(path.join(img_dir, 'Lasers', 'laserRed16.png')).convert()

explosion_animation = {'large':[], 'small': [], 'player':[]}

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    filename_player = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, 'Explosions', filename))
    img_player = pygame.image.load(path.join(img_dir, 'player_explosion', filename_player))
    img.set_colorkey(BLACK)
    img_player.set_colorkey(BLACK)
    img_player = pygame.transform.scale(img, (90, 90))
    explosion_animation['player'].append(img_player)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_animation['large'].append(img_lg)
    img_sm = pygame.transform.scale(img, (30, 30))
    explosion_animation['small'].append(img_sm)
    
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'Power-ups', 'pill_green.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'Power-ups', 'star_silver.png')).convert()
powerup_images['killer'] = pygame.image.load(path.join(img_dir, 'Power-ups', 'bolt_bronze.png')).convert()

shield_effects = {}
shield_effects['gun'] = pygame.image.load(path.join(img_dir, 'spr_shield.png')).convert()
shield_effects['gun'] = pygame.transform.scale(shield_effects['gun'], (150, 150))

shield_effects['killer'] = pygame.image.load(path.join(img_dir, 'spr_shield3.png')).convert()
shield_effects['killer'] = pygame.transform.scale(shield_effects['killer'], (150, 150))

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_Shoot.wav'))
explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'Explosion4.wav'))

pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

score = 0
pygame.mixer.music.play(loops=-1)
running = True
effects = None
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speedx = -8
            if event.key == pygame.K_RIGHT:
                player.speedx = 8
            # if event.key == pygame.K_SPACE:
                # player.shoot()
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    if effects == None:
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:  
            player.shield -= hit.radius
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            expl = Explosion(hit.rect.center, 'small')
            all_sprites.add(expl)
            if player.shield <= 0 :
                player_expl = Explosion(hit.rect.center, 'player')
                all_sprites.add(player_expl)
                player.hide()
                player.lives -= 1
                player.shield = 100
            if player.lives == 0:
                running = False
    elif effects.type == 'gun':
        hits = pygame.sprite.spritecollide(effects, mobs, True, pygame.sprite.collide_circle)
        for hit in hits: 
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            expl = Explosion(hit.rect.center, 'small')
            all_sprites.add(expl)
            
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 65 - hit.radius
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        explosion_sound.play()
        if random.random() > 0.5:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, False)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
            hit.kill()
                
        if hit.type == 'gun':
            if effects == None:
                effects = pow_effect(hit.type)
                all_sprites.add(effects)
                
        if hit.type == 'killer':
            if effects == None:
                effects = pow_effect(hit.type)
                all_sprites.add(effects)
            

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, int(player.shield))
    draw_lives(screen, WIDTH-100, 5, player.lives, player_mini_img)
    pygame.display.flip()

pygame.quit()
