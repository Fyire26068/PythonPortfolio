# Pygame Template skeleton for new pygame project
import pygame as pg
import random
import os
from os import path
from settings import *
from sprites import *

class Game(object):

    def __init__(self, win):
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.top_left_x = (WIDTH - PLAYWIDTH) // 2
        self.top_left_y = HEIGHT - PLAYHEIGHT
        self.locked_positions = {}
        self.grid = self.create_grid(self.locked_positions)
        self.change_piece = False
        self.run = True
        self.current_piece = self.get_shape()
        self.next_piece = self.get_shape()
        self.clock = pg.time.Clock()
        self.fall_time = 0
        self.win = win
    #    self.shape_images = []
    #     self.load_data()
    #
    # def load_data(self):
    #
    #     for img in SHAPEIMAGES:
    #         self.shape_images.append(pg.image.load(path.join(img_folder, img)).convert())

    def new(self):
        # start a new game

        # create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.enemy_group = pg.sprite.Group()

        # create game objects

        # add game objects to groups
        self.all_sprites.add(self.player)
        self.run()

    # def run(self):
    #     # Game Loop
    #     self.playing = True
    #     while self.playing:
    #         self.clock.tick(FPS)
    #         self.events()
    #         self.update()
    #         self.draw()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.run = False
                pg.display.quit()
                self.playing = False
                self.running = False
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.run = False
                    pg.display.quit()
                    self.playing = False
                    self.running = False
                    quit()
                if event.key == pg.K_LEFT:
                    self.current_piece.x -= 1
                    if not self.valid_space(self.current_piece, self.grid):
                        self.current_piece.x += 1

                elif event.key == pg.K_RIGHT:
                    self.current_piece.x += 1
                    if not self.valid_space(self.current_piece, self.grid):
                        self.current_piece.x -= 1
                elif event.key == pg.K_UP:
                    # rotate shape
                    self.current_piece.rotation = self.current_piece.rotation + 1 % len(self.current_piece.shape)
                    if not self.valid_space(self.current_piece, self.grid):
                        self.current_piece.rotation = self.current_piece.rotation - 1 % len(self.current_piece.shape)

                if event.key == pg.K_DOWN:
                    # move shape down
                    self.current_piece.y += 1
                    if not self.valid_space(self.current_piece, self.grid):
                        self.current_piece.y -= 1

    def update(self):
        # Game Loop - update
        while self.run:
            self.grid = self.create_grid(self.locked_positions)
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            #falling
            if self.fall_time/1000 >= FALLSPEED:
                self.fall_time = 0
                self.current_piece.y += 1
                if not (self.valid_space(self.current_piece, self.grid)) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    self.change_piece = True

            self.events()

            shape_pos = self.convert_shape_format(self.current_piece)

            # add piece to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    self.grid[y][x] = self.current_piece.color

            # IF PIECE HIT GROUND
            if self.change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    self.locked_positions[p] = self.current_piece.color
                self.current_piece = self.next_piece
                self.next_piece = self.get_shape()
                self.change_piece = False

                # call four times to check for multiple clear rows
                self.clear_rows(self.grid, self.locked_positions)

            self.draw_window(self.win)
            self.draw_next_shape(self.next_piece, self.win)
            pg.display.update()

            # Check if user lost
            if self.check_lost(self.locked_positions):
                self.run = False

        self.draw_text_middle("You Lost", 40, (255, 255, 255), self.win)
        self.pygame.display.update()
        pg.time.delay(2000)

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def create_grid(self, locked_positions={}):
        grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_positions:
                    c = locked_positions[(j, i)]
                    grid[i][j] = c
        return grid

    def convert_shape_format(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def valid_space(self, shape, grid):
        accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = self.convert_shape_format(shape)

        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False

        return True

    def check_lost(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def get_shape(self):

        return Piece(5, 0, random.choice(shapes), self)

    def draw_text_middle(self, text, size, color, surface):
        font = pg.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)

        surface.blit(label, (self.top_left_x + PLAYWIDTH / 2 - (label.get_width() / 2),
                             self.top_left_y + PLAYHEIGHT / 2 - label.get_height() / 2))

    def draw_grid(self, surface, row, col):
        sx = self.top_left_x
        sy = self.top_left_y
        for i in range(row):
            pg.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                             (sx + PLAYWIDTH, sy + i * 30))  # horizontal lines
            for j in range(col):
                pg.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                                 (sx + j * 30, sy + PLAYHEIGHT))  # vertical lines

    def clear_rows(self, grid, locked):
        # need to see if row is clear the shift every other row above down one

        inc = 0
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                # add positions to remove from locked
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

    def draw_next_shape(self, shape, surface):
        font = pg.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255, 255, 255))

        sx = self.top_left_x + PLAYWIDTH + 50
        sy = self.top_left_y + PLAYHEIGHT / 2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pg.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)

        surface.blit(label, (sx + 10, sy - 30))

    def draw_window(self, surface):
        surface.fill((0, 0, 0))
        # Tetris Title
        font = pg.font.SysFont('comicsans', 60)
        label = font.render('TETRIS', 1, (255, 255, 255))

        surface.blit(label, (self.top_left_x + PLAYWIDTH / 2 - (label.get_width() / 2), 30))

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pg.draw.rect(surface, self.grid[i][j], (self.top_left_x + j * 30,
                                                        self.top_left_y + i * 30, 30, 30), 0)

        # draw grid and border
        self.draw_grid(surface, 20, 10)
        pg.draw.rect(surface, (255, 0, 0), (self.top_left_x, self.top_left_y, PLAYWIDTH, PLAYHEIGHT), 5)
        # pygame.display.update()

    def main_menu(self):
        self.run = True
        while self.run:
            self.win.fill((0, 0, 0))
            self.draw_text_middle('Press any key to begin.', 60, (255, 255, 255), self.win)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False

                if event.type == pg.KEYDOWN:
                    self.update()
        pg.quit()

win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Tetris')


g = Game(win)
g.main_menu()

