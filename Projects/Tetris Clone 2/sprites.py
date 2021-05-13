import pygame as pg
import random
import os
from settings import *


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape, game):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        # self.image = shape_images[shapes.index(shape)]
        #self.image = pg.transform(self.image, (BLOCKSIZE, BLOCKSIZE))
        #self.image =
        self.rotation = 0