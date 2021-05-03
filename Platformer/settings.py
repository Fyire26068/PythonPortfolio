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
FONT_NAME = 'arial'

HS_FILE = "highscore.txt"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 15

#Starting Platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]
# Colors (R, G, B)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE

