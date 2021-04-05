import pygame as pg
import random
import os

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
snd_folder = os.path.join(game_folder,"snd")

TITLE = "Jump."

WIDTH = 480  # width of game window
HEIGHT = 600  # height of game window
FPS = 60  # frames per second

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12


# Colors (R, G, B)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)

