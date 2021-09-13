import math

from bullet import Bullet
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.speed = 0
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(player_img, (50, 38))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.speed = 0
        self.angle = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update_image(self):
        new_image = pygame.transform.rotate(self.image_orig, self.angle).copy()
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 3000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.angle += 5 % 360
            self.update_image()
        if keystate[pygame.K_RIGHT]:
            self.angle -= 5 % 360
            self.update_image()

        if keystate[pygame.K_DOWN]:
            self.speed -= 0.2
        if keystate[pygame.K_UP]:
            self.speed += 0.4
        if not keystate[pygame.K_UP] and not keystate[pygame.K_DOWN]:
            if self.speed <= 0:
                self.speed = 0
            else:
                self.speed -= 0.1
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x -= self.speed * math.sin(math.radians(self.angle))
        self.rect.y -= self.speed * math.cos(math.radians(self.angle))

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top > HEIGHT:
            self.rect.top = HEIGHT
        if self.rect.bottom < 0:
            self.rect.bottom = 0

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

        if self.power >= 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery, self.angle)
            bullet2 = Bullet(self.rect.right, self.rect.centery, self.angle)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
