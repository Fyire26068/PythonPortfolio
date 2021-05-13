import pygame as pg
import random
import os
vec = pg.math.Vector2

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
snd_folder = os.path.join(game_folder,"snd")

TITLE = "PROJECT LEGION"

WIDTH = 1280  # width of game window
HEIGHT = 960  # height of game window
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
LIGHTBLUE = (0, 155, 155)
GREEN = (0, 155, 0)

# Player properties
PLAYER_ACC = 1.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 200
PLAYER_HEIGHT = 100
PLAYER_WIDTH = 75
PLAYER_HEALTH = 100
PLAYER_IMAGE = 'MitheralKnight.png'
IFRAMES = 100

#MOB PROPERTIES
MOB_DAMAGE = 25

# layers properties
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
MOB_LAYER = 2
EFFECTS_LAYER = 3

# weapon properties
WEAPON_EFFECT = ''
WEAPONS = {}
WEAPONS['sword'] = {'rate': 250,
                    'knockback': 200,
                    'damage': 15,
                    'crit_chance': 5,
                    'offset': vec(PLAYER_WIDTH - PLAYER_WIDTH * 1/4, PLAYER_HEIGHT / 2 - PLAYER_HEIGHT),
                    'reach': (PLAYER_WIDTH*2, PLAYER_HEIGHT/8)}

