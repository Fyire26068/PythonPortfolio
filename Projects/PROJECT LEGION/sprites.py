import pygame as pg
import random
import os
from random import choice, randrange
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0

        # self.load_images()
        # self.image = self.standing_frames[0]
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(YELLOW)
        self.image.set_colorkey(BLACK)

        self.health = PLAYER_HEALTH
        self.weapon = 'sword'
        self.iframes = 0

        #self.load_images()
        #self.image = self.standing_frames[0]
        # self.image = player_img

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 100)

        self.pos = vec(40,  HEIGHT - 100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.last_attack = pg.time.get_ticks()

    # def load_images(self):
    #     self.standing_frames = [self.game.player_sheet.get_image(5, 11, 0, 31),
    #                             self.game.player_sheet.get_image(38, 55, 0, 31)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(WHITE)
        # self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
        #                       self.game.spritesheet.get_image(692, 1458, 120, 207)]
        # self.walk_frames_l = []
        # for frame in self.walk_frames_r:
        #     frame.set_colorkey(BLACK)
        #     self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        # self.jump_frame = self.game.spritesheet.get_image(382, 763, 150, 181)
        # self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        # jump only if standing on platforms
        self.rect.x += 15
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 15
        if hits and not self.jumping:
            #self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP]:
            pass
        if keys[pg.K_DOWN]:
           self.crouch()
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_z]:
            self.attack()

    def attack(self):
        now = pg.time.get_ticks()
        if now - self.last_attack > WEAPONS[self.weapon]['rate']:
            self.last_attack = now
            pos = self.pos + vec(WEAPONS[self.weapon]['offset'])

            Weapon(self.game, pos, self.weapon)

    def crouch(self):
        pass


    def update(self):
        # self.animate()
        self.acc = vec(0, PLAYER_GRAVITY)
        self.get_keys()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x  = WIDTH + self.rect.width / 2

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((width, height))
        self.image.fill(LIME)
        self.image.set_colorkey(BLACK)
        # images =  [self.game.spritesheet.get_image(0, 288, 380, 94),
        #            self.game.spritesheet.get_image(213, 1662, 201, 100)]
        # for image in images:
        #     image.set_colorkey(BLACK)
        #self.image = choice(images)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((75, 75))
        self.image.fill(RED)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 100

        self.vx = 0
        self.vy = 0
        self.dy = 0.5

    def update(self):
        pass

class Weapon(pg.sprite.Sprite):
    def __init__(self, game, attack_pos, type):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.attacks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.image = pg.Surface((WEAPONS[type]['reach']))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.pos = vec(attack_pos)
        self.rect.center = attack_pos
        self.spawntime = pg.time.get_ticks()
        self.damage = WEAPONS[type]['damage']

    def update(self):
        if pg.time.get_ticks() - self.spawntime > WEAPONS[self.type]['rate'] / 2:
            self.kill()

