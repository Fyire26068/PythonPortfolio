# Pygame Template skeleton for new pygame project
import pygame as pg
import random
import os
from settings import *
from sprites import *

class Game(object):

    def __init__(self):
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGTH))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()



    def new(self):
        # start a new game

        # create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        # create game objects
        self.player = Player()

        # add game objects to groups
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # Game Loop
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

    def update(self):
        # Game Loop - update
        self.all_sprites.update()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_GO_screen(self):
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_GO_screen()

pg.quit()