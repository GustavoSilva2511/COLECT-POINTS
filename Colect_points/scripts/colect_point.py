import mixer as mixer
import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
pygame.joystick.init()

# screen_size
width = 640
height = 480

# objects_position
x_white = int((width / 2))
y_white = int(430)

x_block = randint(0, 600)
y_block = randint(0, 440)

x_bullet = int(-10)
y_bullet = int(-10)

# screen_creator
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('bala neles')
clock = pygame.time.Clock()

# RGB_colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# texts
font = pygame.font.SysFont('arial', 30, True, False)
points = 0

# contactors
velocity = 15
fire_bullet = 0

# music and songs
pygame.mixer.music.load('BoxCat Games - Mt Fox Shop.wav')
pygame.mixer.music.play(-1)

explosion = pygame.mixer.Sound('explosion_song.wav')
fire = pygame.mixer.Sound('nav_shotter.wav')

# set_volume
pygame.mixer.music.set_volume(0.09)
explosion.set_volume(1)
fire.set_volume(0.3)

while True:
    clock.tick(60)
    screen.fill((0, 0, 0))

    if y_white < 430:
        y_white += 1

    punctuation = f'points: {points}'
    text_format = font.render(punctuation, False, yellow)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        # move_player

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                fire_bullet += 30
                y_bullet = y_white + 20
                x_bullet = x_white + 20

                fire.play()

    if pygame.key.get_pressed()[K_a]:
        x_white -= velocity

    if pygame.key.get_pressed()[K_d]:
        x_white += velocity

    if pygame.key.get_pressed()[K_w]:
        y_white -= velocity

    if pygame.key.get_pressed()[K_s]:
        y_white += velocity

    # objects
    bullet = pygame.draw.rect(screen, yellow, (x_bullet, y_bullet, 10, 10))
    block_white = pygame.draw.rect(screen, white, (x_white, y_white, 50, 50))
    block_blue = pygame.draw.rect(screen, blue, (x_block, y_block, 40, 40))

    # collisions
    if bullet.colliderect(block_blue):
        x_block = randint(0, 600)
        y_block = randint(0, 440)

        points += 1

        explosion.play()

    screen.blit(text_format, (480, 15))

    y_bullet -= fire_bullet
    if y_bullet < 0:
        y_bullet = y_white
        fire_bullet = 0

        x_bullet = int(-10)
        y_bullet = int(-10)

    pygame.display.update()
