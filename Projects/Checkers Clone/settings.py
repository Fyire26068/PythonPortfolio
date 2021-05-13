import pygame as pg
import random
import os

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
snd_folder = os.path.join(game_folder,"snd")

CROWN = pg.transform.scale(pg.image.load('img/crown.png'), (44, 25))

TITLE = "Checkers"

WIDTH = 800  # width of game window
HEIGHT = 800  # height of game window
FPS = 60  # frames per second

ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
PADDING = 10
OUTLINE = 2

# Colors (R, G, B)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIME = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
GREY = (128,128,128)

