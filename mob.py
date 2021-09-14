import random

from config import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, spd_x=0, spd_y=0, image=''):
        pygame.sprite.Sprite.__init__(self)
        self.num_img = random.randint(0, len(meteor_images)-1)
        self.image_orig = image if image != '' else meteor_images[self.num_img]
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = x
        self.rect.y = -self.rect.height if y == 0 else y
        self.speed_y = spd_y
        self.speed_x = spd_x
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.y += int(self.speed_y)
        self.rect.x += int(self.speed_x)
        if self.rect.top > HEIGHT + 10 or self.rect.left < 25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)
