import pygame
import random
import math
from pygame import mixer

pygame.init()
# creating our window
# to access all the stuff in pygame
# create screen
screen = pygame.display.set_mode((800, 600))  # width, height

# Caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)
# background
background = pygame.image.load('background.png')

mixer.music.load("background.wav")
mixer.music.play(-1)
# player
playerImage = pygame.image.load('spaceship.png')
playerX = 370
playerY = 500
playerX_change = 0

# enemy
enemyimage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 350))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet
bulletimage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletY_change = 15
bullet_state = 'ready'  # You can't see the bullet, another state = fire state

# score
score_value = 0
font = pygame.font.Font('homework.ttf', 32)
textx = 10
texty = 10

over_font = pygame.font.Font("Homework.ttf", 75)

def game_over_text():
    over = over_font.render("GAME OVER", True,  (255, 255, 255))
    screen.blit(over, (250, 250))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImage, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimage, (x + 16, y + 10))
    # x + 16, y + 10 to ensure that bullet appears at the centre of the spaceship


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    screen.fill((0, 0, 0))  # drawing the screen
    # background image
    screen.blit(background, (0, 0))
    # loop through all the events in the pygame window
    for event in pygame.event.get():
        #  if keystroke is pressed, checked whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            elif event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # get the x coordinate of spaceship
                    bullet_sound = mixer.Sound("Laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # when key is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        # when close button is hit
        if event.type == pygame.QUIT:
            running = False
    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY = bulletY - bulletY_change

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 500
            bullet_state = 'ready'
            score_value += 10

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY)
    show_score(textx, texty)
    pygame.display.update()
