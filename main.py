import random

import pygame

# Initialization of PyGame
pygame.init()

screen = pygame.display.set_mode((800, 600))

# Renaming the window Title
pygame.display.set_caption("SpaceInvaders")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Background config
backgroundImage = pygame.image.load("background.png")
backgroundImage = pygame.transform.scale(backgroundImage, (800, 600))

# Score
scoreValue = -1
font = pygame.font.Font("freesansbold.ttf", 32)
testX = 10
testY = 10


def showScore(x, y):
    screen.blit(backgroundImage, (x, y))
    score = font.render("Score :" + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Player config
playerImg = pygame.image.load("player.png")
playerSize = (200, 200)
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerMove = 0

# Bullet config
bulletImg = pygame.image.load("bullet.png")
bulletImg = pygame.transform.scale(bulletImg, (32, 32))
bulletRect = pygame.Rect(0, 0, 32, 32)
bulletX = 0
bulletY = 480
bulletState = "ready"
bulletSpeed = 10
isFiring = False

# Enemy1
enemy1Image = pygame.image.load("enemy1.png")
enemy1Image = pygame.transform.scale(enemy1Image, (48, 48))
enemy1Img = []
enemy1Rect = []
enemyX = []
enemyY = []
enemyMove = []
numberOfEnemies = 6

for i in range(numberOfEnemies):
    enemy1Img.append(pygame.transform.scale(enemy1Image, (48, 48)))
    enemy1Rect.append(pygame.Rect(0, 0, 48, 48))
    enemyX.append(50 * i)
    enemyY.append(50)
    enemyMove.append(5)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemy1Img[i], (x, y))


def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Running the game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Position matters
    screen.blit(backgroundImage, (0, 0))
    showScore(testX, testY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerMove = -5
            if event.key == pygame.K_RIGHT:
                playerMove = 5
            if event.key == pygame.K_SPACE:
                isFiring = True
                if bulletState == "ready":
                    bulletX = playerX
                    fireBullet(playerX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerMove = 0
            if event.key == pygame.K_SPACE:
                isFiring = False

    playerX += playerMove
    if playerX > screen.get_width() - 65:
        playerX -= playerMove
    elif playerX < 2:
        playerX -= playerMove
    for i in range(numberOfEnemies):
        enemyX[i] += enemyMove[i]
        if enemyX[i] > screen.get_width() - 65:
            enemyMove[i] = -5
            enemyY[i] += 40
        elif enemyX[i] < 2:
            enemyMove[i] = 5
            enemyY[i] += 40
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletSpeed
    for i in range(numberOfEnemies):

        enemy1Rect[i].update(enemyX[i] - 24, enemyY[i] - 24, 48, 48)
        if enemy1Rect[i].colliderect(bulletRect):
            bulletY = 480
            enemyY[i] = 0
            enemyX[i] = random.randint(8, 300)
            if bulletState == "fire":
                scoreValue += 1
                print(scoreValue)
            bulletState = "ready"

        enemy(enemyX[i], enemyY[i], i)

    bulletRect.update(bulletX, bulletY, 32, 32)

    player(playerX, playerY)

    pygame.display.update()
