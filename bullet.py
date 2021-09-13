import math

from config import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 10))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.angle = angle
        self.rect.centerx = x - 20 * math.sin(math.radians(self.angle))
        self.rect.centery = y - 20 * math.cos(math.radians(self.angle))
        self.speedy = -10

    def update(self):
        self.rect.x += self.speedy * math.sin(math.radians(self.angle))
        self.rect.y += self.speedy * math.cos(math.radians(self.angle))

        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.kill()
