# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import random
import time

import mob
from config import *
from expl import Explosion
from player import Player
from updates import Pow

random.seed(time.time())
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire, F to save, 1 to load", 20, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press the any button to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def new_mob(x_pos: int = 0, y_pos: int = 0, sprite_image: str = ''):
    if x_pos == 0:
        x_pos = random.randint(-5, WIDTH + 5)
    m = mob.Mob(x_pos, y_pos, 0, 0, sprite_image)
    all_sprites.add(m)
    mobs.add(m)


pygame.mixer.music.play(loops=-1)
game_over = True
running = True
load_save = False
save = []
mobs = pygame.sprite.Group()
power_up = pygame.sprite.Group()
score = 0

while running:
    key_state = pygame.key.get_pressed()
    clock.tick(FPS)
    all_sprites.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if key_state[pygame.K_1]:
        load_save = True

    if key_state[pygame.K_f]:
        with open("save.sav", "w") as file:
            for sprite in all_sprites:
                if isinstance(sprite, mob.Mob):
                    file.write(f'{str(sprite.rect.x)},{str(sprite.rect.y)},{str(sprite.num_img)}\n')
            file.write(f'{str(player.rect.x)},{str(player.rect.y)},{str(player.angle)},{int(score)},'
                       f'{str(player.shield)},{str(player.lives)}\n')
            file.flush()
            file.close()

    if game_over:
        score = 0
        for i in all_sprites:
            i.kill()
        game_over = False
        player = Player()
        all_sprites.add(player)
        show_go_screen()
        if not load_save:
            for _ in range(8):
                new_mob()

    if load_save:
        load_save = False
        for sprite in all_sprites:
            sprite.kill()
        with open("save.sav", "r") as file:
            lines = file.readlines()
            for line in lines[:len(lines) - 1]:
                x, y, image = map(int, line.split(","))
                new_mob(x, y, meteor_images[image])
            player = Player()
            all_sprites.add(player)
            player.rect.x, player.rect.y, player.angle, player.score, player.shield, player.lives = map(int,
                                                                                                        lines[-1].split(
                                                                                                            ','))
            file.close()

    for sprite in all_sprites:
        if player.rect.y < HEIGHT:
            score += 0.001
            if isinstance(sprite, mob.Mob):
                if sprite.speed_y <= MOB_MAX_SPEED:
                    sprite.speed_y += 0.1

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(explosion_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            power_up.add(pow)
        new_mob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        new_mob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pygame.sprite.spritecollide(player, power_up, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.power_up()

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    draw_text(screen, str(round(score)), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_sm_img)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
