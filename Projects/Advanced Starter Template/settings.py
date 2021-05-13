import pygame as pg
import random
import os

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
snd_folder = os.path.join(game_folder,"snd")

TITLE = "template"

WIDTH = 640  # width of game window
HEIGTH = 480  # height of game window
FPS = 60  # frames per second

# Colors (R, G, B)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIME = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)

