import random

from config import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, spd_x=0, spd_y=0, image=''):
        pygame.sprite.Sprite.__init__(self)
        self.num_img = random.randint(0, len(meteor_images)-1)
        if image != '':
            self.image_orig = image
        else:
            self.image_orig = meteor_images[self.num_img]
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = x
        self.rect.y = y
        self.speedy = spd_y
        self.speedx = spd_x
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += int(self.speedy)
        self.rect.x += int(self.speedx)
        if self.rect.top > HEIGHT + 10 or self.rect.left < 25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
