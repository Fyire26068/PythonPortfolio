# Pygame Template skeleton for new pygame project
import pygame as pg
import random
import os
from os import path
from settings import *
from sprites import *

def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 40
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game(object):

    def __init__(self):
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        self.title_font = path.join(img_folder, 'evilempire.ttf')

        self.player_sheet = pg.image.load(path.join(img_folder, PLAYER_IMAGE)).convert_alpha()


    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def new(self):
        # start a new game

        # create sprite groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player_group = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.attacks = pg.sprite.Group()

        # create game objects
        self.player = Player(self)

        self.ground = Platform(self, 0, HEIGHT - 50, WIDTH, HEIGHT)

        self.enemy1 = Mob(self, WIDTH/2, HEIGHT - 50 - 75)


        self.run()

    def run(self):
        # Game Loop
        # IMPLEMENT MUSIC LOOP HERE
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def update(self):
        # Game Loop - update
        self.all_sprites.update()

        # hit mobs?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            if not self.player.iframes > 0:
                self.player.health -= MOB_DAMAGE
                self.player.iframes = IFRAMES
            else:
                self.player.iframes -= 1

        if self.player.iframes > 0:
            self.player.iframes -= 1


        # weapon attacks mob
        hits = pg.sprite.groupcollide(self.mobs, self.attacks, False, False)
        for mob in hits:
            for attack in hits[mob]:
                #mob.health -= WEAPONS[self.player.weapon]['damage']
                mob.kill()

            # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False

        if self.player.rect.right >= WIDTH *3 / 4:
            self.player.pos.x -= max(abs(self.player.vel.x), 2)

            for mob in self.mobs:
                mob.rect.x -= max(abs(self.player.vel.x), 2)

            for plat in self.platforms:
                plat.rect.x -= max(abs(self.player.vel.x), 2)
                if plat.rect.right <= 0:
                    plat.kill()






        while random.random() < 0.3 and len(self.platforms) < 4:
            width = random.randrange(50, 100)
            p = Platform(self, WIDTH, random.randrange(-HEIGHT + 150, HEIGHT - 150), width, 25)






        if self.player.health <= 0:
            self.playing = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("Project Legion", self.title_font, 100, YELLOW, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def show_GO_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to restart", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_GO_screen()

pg.quit()