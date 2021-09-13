# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney.nl
import random

import mob
from config import *
from expl import Explosion
from player import Player
from updates import Pow

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
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
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
    draw_text(screen, "Arrow keys move, Space to fire, F to save, 1 to load", 20,
              WIDTH / 2, HEIGHT / 2)
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


pygame.mixer.music.play(loops=-1)

game_over = True

running = True
save = []


def newmob(x=random.randint(0, WIDTH), y=random.randint(0, HEIGHT // 2), image=''):
    m = mob.Mob(x, y, 0, 0, image)
    all_sprites.add(m)
    mobs.add(m)


load_save = False
score = 0
while running:
    keystate = pygame.key.get_pressed()

    clock.tick(FPS)
    if keystate[pygame.K_1]:
        load_save = True
    if game_over:
        for i in all_sprites:
            i.kill()
        game_over = False
        player = Player()
        mobs = pygame.sprite.Group()
        all_sprites.add(player)
        powerups = pygame.sprite.Group()
        score = 0
        show_go_screen()
        if not load_save:
            for sprite in range(8):
                newmob()

    if load_save:
        load_save = False
        for sprite in all_sprites:
            sprite.kill()
        with open(".\save.sav", "r") as file:
            lines = file.readlines()
            for line in lines[:len(lines) - 1]:
                x, y, image = map(int, line.split(","))
                newmob(x, y, meteor_images[image])
            player = Player()
            all_sprites.add(player)
            player.rect.x, player.rect.y, player.angle, player.score, player.shield, player.lives = map(int, lines[-1].split(','))
            file.close()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for a in all_sprites:
        if player.rect.y <= 150:
            score += 0.003
            if isinstance(a, mob.Mob):
                a.speedy += 0.2
        elif player.rect.y <= 350:
            score += 0.005
            if isinstance(a, mob.Mob):
                a.speedy += 0.5
        elif player.rect.y <= 450:
            score += 0.001
            if isinstance(a, mob.Mob):
                a.speedy += 0.1
        else:
            for c in all_sprites:
                if isinstance(c, mob.Mob):
                    c.speedy = 0

    if keystate[pygame.K_f]:
        with open(".\save.sav", "w") as file:
            for sprite in all_sprites:
                if isinstance(sprite, mob.Mob):
                    file.write(f'{str(sprite.rect.x)},{str(sprite.rect.y)},{str(sprite.num_img)}\n')
            file.write(
                f'{str(player.rect.x)},{str(player.rect.y)},{str(player.angle)},{int(score)},{str(player.shield)},{str(player.lives)}\n')
            file.close()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_sm_img)
    pygame.display.flip()

pygame.quit()
