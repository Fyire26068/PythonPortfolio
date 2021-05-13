import pygame as pg
import random
import os
vec = pg.math.Vector2

# set up asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
snd_folder = os.path.join(game_folder,"snd")
map_folder = os.path.join(game_folder, "maps")
music_folder = os.path.join(game_folder,"music")

# Colors (R, G, B)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
LIME = (0,255,0)
GREEN = (0,144,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
CYAN = (0,255,255)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
BROWN = (106, 55, 5)

#game settings

TITLE = "tiled"
WIDTH = 1024  # width of game window
HEIGHT = 768  # height of game window
FPS = 60  # frames per second
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE



WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)


# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed' : 400,
                      'bullet_lifetime' : 500,
                      'rate': 800,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 6,
                      'bullet_size': 'sm',
                      'bullet_count': 12}
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10


# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png', 'whitePuff18.png']
FLASH_DURATION = 40
SPLAT = 'splat green.png'
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

#Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.5

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'health_up': 'health_pack.wav'}