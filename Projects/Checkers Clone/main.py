# Pygame Template skeleton for new pygame project
import pygame as pg
import random
import os
from settings import *
from sprites import *
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Checkers')

class Game:
    def __init__(self):
        self.running = True
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

    def new(self):
        self.selected = None
        self.board = Board(self.screen)
        self.turn = RED
        self.valid_moves = {}
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                self.select(row, col)

    def update(self):
        if self.winner() != None:
            print(self.winner())
            run = False
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)

        pg.display.update()

    def winner(self):
        return self.board.winner()

    def reset(self):
        self.new()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pg.draw.circle(self.screen, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col








g = Game()
#g.show_start_screen()
while g.running:
    g.new()
   # g.show_GO_screen()

pg.quit()