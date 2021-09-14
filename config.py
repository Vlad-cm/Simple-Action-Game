import os

import pygame

WIDTH = 480
HEIGHT = 600
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MOB_MAX_SPEED = 2
PLAYER_MAX_SPEED = 3

BAR_LENGTH = 100
BAR_HEIGHT = 10

pygame.init()
pygame.mixer.init()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
snd_folder = os.path.join(game_folder, 'sounds')

background = pygame.image.load(os.path.join(img_folder, 'stars.webp'))
player_img = pygame.image.load(os.path.join(img_folder, "ship.png"))
player_sm_img = pygame.transform.scale(player_img, (25, 19))
player_sm_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(os.path.join(img_folder, "bul.png"))
shoot_sound = pygame.mixer.Sound(os.path.join(snd_folder, 'pew.wav'))

power_up_images = {'shield': pygame.image.load(os.path.join(img_folder, 'shield_gold.png')),
                   'gun': pygame.image.load(os.path.join(img_folder, 'thd.png'))}

explosion_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    explosion_sounds.append(pygame.mixer.Sound(os.path.join(snd_folder, snd)))

pygame.mixer.music.load(os.path.join(snd_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.3)

background_rect = background.get_rect()
meteor_list = ['mbb1.png', 'mbm1.png', 'mbm3.png', 'mbs1.png', 'mbs2.png', 'mbt1.png']

explosion_anim = {'lg': [], 'sm': [], 'player': []}
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename))
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename))
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

meteor_images = []
for i in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, i)))

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
