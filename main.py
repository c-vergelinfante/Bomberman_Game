import pygame
import random
import math

# Initializing the game
pygame.init()

# Create the size of the screen. Based on number of steel walls
x_steel_walls = 3
y_steel_walls = 3
number_of_walls = 12
screen = pygame.display.set_mode((32 + (64*x_steel_walls), 32 + (64*y_steel_walls)))

# Title and Icon
pygame.display.set_caption('Look at all those chickens!')
speed_delay = 90

# Steel Wall
steel_wall_IMG = pygame.image.load('/Users/cmvergel/PycharmProjects/Bomberman/wall.png')

# Wall
wall_IMG = pygame.image.load('/Users/cmvergel/PycharmProjects/Bomberman/white_wall.png')

# Thief
isInverted = 0
thief_IMG_inv = pygame.image.load('/Users/cmvergel/PycharmProjects/Bomberman/thief_inv.png')
thief_IMG = pygame.image.load('/Users/cmvergel/PycharmProjects/Bomberman/thief.png')
thiefX = 0
thiefY = 0
thiefX_change = 0
thiefY_change = 0

# Bomb
bomb_IMG = pygame.image.load('/Users/cmvergel/PycharmProjects/Bomberman/dynamite.png')
bombX = 0
bombY = 0
bomb_state = 'ready'

# Central Fire
central_fire_IMG = pygame.image.load('/Users/cmvergel/PycharmProjects/Bomberman/shockwave.png')
explosion_state = 'off'
explosionX = 0
explosionY = 0

# Fire
fire_IMG = pygame.image.load('/Users/cmvergel/PycharmProjects/Bomberman/fire.png')

# Game Over text
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)


def steel_wall(x, y):
    screen.blit(steel_wall_IMG, (x, y))


def wall(x, y):
    screen.blit(wall_IMG, (x, y))


def bomb(x, y):
    global bomb_state
    bomb_state = 'fire'
    screen.blit(bomb_IMG, (x, y))


def thief(x, y, inverted):
    if inverted == 0:
        screen.blit(thief_IMG, (x, y))
    else:
        screen.blit(thief_IMG_inv, (x,y))


def setup_grid():
    for i in range(x_steel_walls):
        for j in range(y_steel_walls):
            steel_wall(32 + (i*64), 32 + (j*64))


def setup_walls():
    wall(64, 0)
    wall(0, 64)
    if number_of_walls > 2:
        for i in range(number_of_walls - 2):
            # Number of spaces is always x_steel_walls + 1
            # random.randint(min, max)
            x_steel_walls


def isCollision(thiefX, thiefY):

    decX = thiefX//32
    decY = thiefY//32

    if decY % 2 == 0:
        return False
    else:
        if decX % 2 == 0:
            return False
        else:
            return True


def explosion():

    global explosion_state
    screen.blit(central_fire_IMG, (explosionX, explosionY))

    decX = explosionX//32
    decY = explosionY//32

    if decY % 2 == 0:
        screen.blit(fire_IMG, (explosionX + 32, explosionY))
        screen.blit(fire_IMG, (explosionX + 64, explosionY))
        screen.blit(fire_IMG, (explosionX - 32, explosionY))
        screen.blit(fire_IMG, (explosionX - 64, explosionY))
        if decX % 2 == 0:
            screen.blit(fire_IMG, (explosionX, explosionY + 32))
            screen.blit(fire_IMG, (explosionX, explosionY + 64))
            screen.blit(fire_IMG, (explosionX, explosionY - 32))
            screen.blit(fire_IMG, (explosionX, explosionY - 64))
    else:
        screen.blit(fire_IMG, (explosionX, explosionY + 32))
        screen.blit(fire_IMG, (explosionX, explosionY + 64))
        screen.blit(fire_IMG, (explosionX, explosionY - 32))
        screen.blit(fire_IMG, (explosionX, explosionY - 64))

    explosion_state = 'on'


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (32*x_steel_walls, 32*y_steel_walls))


# Game Loop

time_counter = 0
explosion_counter = 0
running = True
Game_Over = 'False'


while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 153, 76))
    pygame.time.delay(speed_delay)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if Game_Over is not 'True':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    thiefX_change = -32
                    isInverted = 0
                if event.key == pygame.K_RIGHT:
                    thiefX_change = 32
                    isInverted = 1
                if event.key == pygame.K_UP:
                    thiefY_change = -32
                if event.key == pygame.K_DOWN:
                    thiefY_change = 32
                if event.key == pygame.K_SPACE:
                    if bomb_state is 'ready':
                        bombX = thiefX
                        bombY = thiefY
                        bomb(thiefX, thiefY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP\
                        or event.key == pygame.K_DOWN:
                    thiefX_change = 0
                    thiefY_change = 0

    thiefX += thiefX_change
    thiefY += thiefY_change

    collision = False
    collision = isCollision(thiefX, thiefY)
    if collision:
        thiefX = thiefX - thiefX_change
        thiefY = thiefY - thiefY_change

    if thiefX <= 0:
        thiefX = 0
    elif thiefX >= 64*x_steel_walls:
        thiefX = 64*x_steel_walls

    if thiefY <= 0:
        thiefY = 0
    elif thiefY >= 64*y_steel_walls:
        thiefY = 64*y_steel_walls

    if bomb_state is 'fire':
        bomb(bombX, bombY)
        time_counter += speed_delay
        if time_counter > 3000:
            time_counter = 0
            explosionX = bombX
            explosionY = bombY
            explosion()
            bomb(-40, -40)
            bomb_state = 'ready'

    if explosion_state is 'on':
        explosion()
        explosion_counter += speed_delay
        if thiefX == explosionX:
            if thiefY == explosionY + 32 or thiefY == explosionY + 64 or thiefY == explosionY - 32 or thiefY == explosionY - 64 or thiefY == explosionY:
                game_over_text()
                Game_Over = 'True'
        if thiefY == explosionY:
            if thiefX == explosionX + 32 or thiefX == explosionX + 64 or thiefX == explosionX - 32 or thiefX == explosionX - 64:
                game_over_text()
                Game_Over = 'True'

        if explosion_counter > 1000:
            explosion_counter = 0
            explosion_state = 'off'

    setup_grid()
    setup_walls()
    thief(thiefX, thiefY, isInverted)
    pygame.display.update()