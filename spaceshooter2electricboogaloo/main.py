import pygame as pg
import random as r
import math
from os import *


#Attribution
#<###################################################################
# Art Work Credit: "Kenney.nl" @ "www.kenney.nl"
# Code by: Anthony Garrard

####################################################################


# Game object classes
####################################################################

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.shield = 100
        # self.image = pg.Surface((50,40))
        # self.image.fill(GREEN)
        self.image = player_img
        self.image = pg.transform.scale(player_img,(60,48))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width*.85 / 2
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT - (HEIGHT*.05))
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hide_timer = pg.time.get_ticks()
        self.hidden = False
        self.power = 1
        self.power_time = pg.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+200)

    def powerup(self):
        self.power += 1
        self.power_time = pg.time.get_ticks()
        powerup_snd.play()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullet_group.add(bullet)
                shoot_snd.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullet_group.add(bullet1)
                bullet_group.add(bullet2)
                shoot_snd.play()

    def update(self):
        self.speedx = 0
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -8
        if keystate[pg.K_RIGHT]:
            self.speedx = 8
        if keystate[pg.K_SPACE] or keystate[pg.K_UP]:
            self.shoot()
        self.rect.x += self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # timeout for powerups
        if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()
            powerdown_snd.play()




class NPC(pg.sprite.Sprite):
    def __init__(self):
        # pg.sprite.Sprite.__init__(self)
        # #super(NPC, self).__init__()
        # # self.image = pg.Surface((25,25))
        # # self.image.fill(RED)
        # self.image_orig = r.choice(meteor_images)
        # self.image_orig.set_colorkey(BLACK)
        # self.image = self.image_orig.copy()
        #
        # self.rect = self.image.get_rect()
        # self.radius = int(self.rect.width * .85 / 2)
        # #pg.draw.circle(self.image,RED,self.rect.center,self.radius)
        # # self.rect.centerx = (WIDTH/2)
        # # self.rect.top = 0
        # self.rsx = r.randint(-3, 3)
        # self.rsy = r.randint(1, 8)
        # self.rect.x = r.randrange(WIDTH - self.rect.width)
        # self.rect.y = r.randrange(-100, -40)
        # self.speedx = self.rsx
        # self.speedy = self.rsy
        # self.rot = 0
        # self.rot_speed = r.randint(-8,8)
        # self.last_update = pg.time.get_ticks()
        pg.sprite.Sprite.__init__(self)
        self.image_orig = r.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = r.randrange(WIDTH - self.rect.width)
        self.rect.y = r.randrange(-150, -100)
        self.speedy = r.randrange(1, 8)
        self.speedx = r.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = r.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        # now = pg.time.get_ticks()
        # if now - self.last_update > 50:
        #     self.last_update = now
        #     # do a barrel roll
        #     old_center = self.rect.center
        #     self.rot = (self.rot + self.rot_speed) % 360
        #     new_image = pg.transform.rotate(self.image, self.rot)
        #     self.image = new_image
        #     self.rect = self.image.get_rect()
        #     self.rect.center = old_center
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def spawn(self):
        m = NPC()
        all_sprites.add(m)
        npc_group.add(m)



    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = r.randrange(WIDTH - self.rect.width)
            self.rect.y = r.randrange(-100, -40)
            self.speedy = r.randrange(1, 8)
            self.speedx = r.randrange(-1,1)

        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
        if self.rect.left < 0:
            self.speedx = -self.speedx


class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        super(Bullet, self).__init__()
        # self.image = pg.Surface((5,10))
        # self.image.fill(BLUE)
        self.image = bullet_img
        self.image = pg.transform.scale(self.image, (15, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = r.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        #  kill if moves off bottom
        if self.rect.top > HEIGHT:
            self.kill()


####################################################################

# Game Function
#####################################################################
font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_healthbar(surf, x, y, pct):
    if pct < 0 :
        pct = 0
    bar_len = 100
    bar_height = 10
    fill = (pct/100)*bar_len
    outline_rect = pg.Rect(x, y, bar_len, bar_height)
    fill_rect = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4, WHITE)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2, RED)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4, BLUE)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False

####################################################################

# Game Constants
####################################################################
HEIGHT = 900
WIDTH = 600
FPS = 60
POWERUP_TIME = 5000

# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

title = "Shmup"
#font_name = pg.Font()

####################################################################

# initialize pygame and create window
####################################################################
pg.init()
pg.mixer.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()
####################################################################

#image locations
####################################################################
project_folder = path.dirname(__file__)
img_folder = path.join(project_folder,"imgs")
background_img_folder = path.join(img_folder, "background")
player_img_folder =  path.join(img_folder, "player")
enemy_img_folder = path.join(img_folder, "enemy")
snds_folder = path.join(project_folder,"snds")
base_snds_folder = path.join(snds_folder, "base")
animation_folder = path.join(img_folder, "animation")
powerup_folder = path.join(img_folder,"powerups")
####################################################################

# load imgs
####################################################################
#back grond img loaded
background = pg.image.load(path.join(background_img_folder,"starfield.png")).convert()
background = pg.transform.scale(background,(WIDTH,HEIGHT))
background_rect = background.get_rect()
# player img loaded
player_img = pg.image.load(path.join(player_img_folder,"player1ship.png")).convert()
player_mini_img = pg.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
#npc_img = pg.image.load(path.join(enemy_img_folder,"img_1.png")).convert()
bullet_img = pg.image.load(path.join(player_img_folder,"bullet_img.png")).convert()

# load asteroids
meteor_images = []
meteor_list = ['img_1.png', 'img_2.png', 'img_3.png', 'img_4.png', 'img_5.png', 'img_6.png', 'img_7.png',
               'img_8.png', 'img_9.png', 'img_10.png']
for img in meteor_list:
    meteor_images.append(pg.image.load(path.join(enemy_img_folder, img)).convert())

# load explosions
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []
explosion_anim["player"] = []
for i in range(0,9):
    fn = "regularExplosion0{}.png".format(i)
    img = pg.image.load(path.join(animation_folder, fn)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img, (100, 100))
    img_sm = pg.transform.scale(img, (40, 40))
    explosion_anim["sm"].append(img_sm)
    explosion_anim["lg"].append(img_lg)
    fn = "sonicExplosion0{}.png".format(i)
    img = pg.image.load(path.join(animation_folder, fn)).convert()
    img.set_colorkey(BLACK)
    explosion_anim["player"].append(img)

# load powerups
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(powerup_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pg.image.load(path.join(powerup_folder, 'bolt_gold.png')).convert()

####################################################################

# load Sounds
####################################################################
shoot_snd = pg.mixer.Sound(path.join(base_snds_folder,"pew.wav"))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pg.mixer.Sound(path.join(base_snds_folder, snd)))
shield_snd = pg.mixer.Sound(path.join(base_snds_folder, "shield_snd.ogg"))
powerup_snd = pg.mixer.Sound(path.join(base_snds_folder, "gun_powerup.ogg"))
powerdown_snd = pg.mixer.Sound(path.join(base_snds_folder, "gun_powerdown.ogg"))
pg.mixer.music.load(path.join(base_snds_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pg.mixer.music.set_volume(0.4)
pg.mixer.music.play(loops=-1)
####################################################################

# create Sprite groups
####################################################################
all_sprites = pg.sprite.Group()
players_group = pg.sprite.Group()
npc_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()
powerups = pg.sprite.Group()
####################################################################

# create Game Objects
####################################################################
player = Player()
npc = NPC()

####################################################################

# add objects to sprite groups
####################################################################
players_group.add(player)
for i in players_group:
    all_sprites.add(i)
for i in range(8):
    m = NPC()
    all_sprites.add(m)
    npc_group.add(m)

####################################################################


# Game Loop
###################
# game update Variables
########################################
playing = True
game_over = True

########################################
################################################################
while playing:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pg.sprite.Group()
        mobs = pg.sprite.Group()
        bullets = pg.sprite.Group()
        powerups = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            npc.spawn()
        score = 0
    # timing
    ##################################################
    clock.tick(FPS)
    ##################################################

    # collecting Input
    ##################################################

    # Quiting the game when we hit the x
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                playing = False
            # if event.key == pg.K_SPACE or event.key == pg.K_UP:
            #     player.shoot()
        if event.type == pg.QUIT:
            playing = False


    ##################################################
    # Updates
    ##################################################
    # if the player died and the explosion has finished playing
    if player.lives == 0 and not death_expl.alive():
        game_over = True

    all_sprites.update()


    # check to see if npc hit the player

    hits = pg.sprite.spritecollide(player, npc_group, True, pg.sprite.collide_circle)
    for hit in hits:
        r.choice(expl_sounds).play()
        player.shield -= hit.radius*2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        npc.spawn()
        if player.shield <= 0:
            death_expl = Explosion(player.rect.center, "player")
            all_sprites.add(death_expl)
            player.hide()
            player.shield = 100
            player.lives -= 1

    # check to see if npc hit npc
    hits = pg.sprite.groupcollide(npc_group, npc_group, False, False, pg.sprite.collide_circle)
    if hits:
        npc.speedx = -npc.speedx
    # check to see if bullet hits npc
    hits = pg.sprite.groupcollide(npc_group, bullet_group, True, True)
    for hit in hits:
        score += 50 - hit.radius
        r.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        if r.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        npc.spawn()

    # check to see if player hits powerup
    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += r.randrange(10,30)
            if player.shield >= 100:
                player.shield = 100
            shield_snd.play()
        if hit.type == 'gun':
            player.powerup()


    ##################################################

    # Render
    ##################################################
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # draw HUD
    draw_text(screen, "Score: " + str(score), 18, WIDTH/2,10, WHITE)
    draw_healthbar(screen, 5, 10, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    pg.display.flip()
    ##################################################

pg.quit()

################################################################
#####################