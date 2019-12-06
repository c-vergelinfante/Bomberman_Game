import pygame
import os, sys
import random
import math

# Initializing the game
pygame.init()

# Create the size of the screen. Based on number of steel walls
x_steel_walls = 3
y_steel_walls = 3
number_of_walls = 12
screen = pygame.display.set_mode((32 + (64 * x_steel_walls), 32 + (64 * y_steel_walls)))

x_places = (x_steel_walls * 2) + 1
y_places = (y_steel_walls * 2) + 1

# Setting the folder with the Figures
Figures_folder = os.path.abspath(os.path.dirname(sys.argv[0])) + '/Figures/'

# Title and Icon
pygame.display.set_caption('Look at all those chickens!')
speed_delay = 90

# Steel Wall
steel_wall_IMG = pygame.image.load(Figures_folder + 'wall.png')

# Wall
wall_IMG = pygame.image.load(Figures_folder + 'white_wall.png')

# Thief
isInverted = 0
thief_IMG_inv = pygame.image.load(Figures_folder + 'thief_inv.png')
thief_IMG = pygame.image.load(Figures_folder + 'thief.png')
thiefX = 0
thiefY = 0
thiefX_change = 0
thiefY_change = 0

# Bomb
bomb_IMG = pygame.image.load(Figures_folder + 'dynamite.png')
bombX = 0
bombY = 0
bomb_state = 'ready'

# Doors
door_closed_IMG = pygame.image.load(Figures_folder + 'door_closed.png')
door_open_IMG = pygame.image.load(Figures_folder + 'door_open.png')
door_location = -40
door_state = ''  # closed, open

# Central Fire
central_fire_IMG = pygame.image.load(Figures_folder + 'shockwave.png')
explosion_state = 'off'
explosionX = 0
explosionY = 0

# Key
key_IMG = pygame.image.load(Figures_folder + 'key.png')
key_location = - 40
key_state = ''

# Fire
fire_IMG = pygame.image.load(Figures_folder + 'fire.png')

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
        screen.blit(thief_IMG_inv, (x, y))


def door(location):
    if door_state == 'closed':
        screen.blit(door_closed_IMG, (fromNumber_toLocation(location)[0], fromNumber_toLocation(location)[1]))
    elif door_state == 'open':
        screen.blit(door_open_IMG, (fromNumber_toLocation(location)[0], fromNumber_toLocation(location)[1]))


def key(location):
    screen.blit(key_IMG, (fromNumber_toLocation(location)[0], fromNumber_toLocation(location)[1]))


def setup_grid():
    for i in range(x_steel_walls):
        for j in range(y_steel_walls):
            steel_wall(32 + (i * 64), 32 + (j * 64))


def setup_walls():
    for x in walls:
        wall(fromNumber_toLocation(x)[0], fromNumber_toLocation(x)[1])


def isCollision(thiefX, thiefY):
    decX = thiefX // 32
    decY = thiefY // 32

    if decY % 2 == 0:
        return False
    else:
        if decX % 2 == 0:
            return False
        else:
            return True


to_remove = []
fire_cells = []


def explosion():
    global explosion_state
    screen.blit(central_fire_IMG, (explosionX, explosionY))
    loc_explosion = fromLocation_toNumber(explosionX, explosionY)

    if loc_explosion not in fire_cells:
        fire_cells.append(loc_explosion)

    if isSteelWall(fromLocation_toNumber(explosionX + 32, explosionY)) is False:
        screen.blit(fire_IMG, (explosionX + 32, explosionY))
        if fromLocation_toNumber(explosionX + 32, explosionY) not in fire_cells:
            fire_cells.append(fromLocation_toNumber(explosionX + 32, explosionY))
        if fromLocation_toNumber(explosionX + 32, explosionY) not in walls:
            screen.blit(fire_IMG, (explosionX + 64, explosionY))
            if fromLocation_toNumber(explosionX + 64, explosionY) not in fire_cells:
                fire_cells.append(fromLocation_toNumber(explosionX + 64, explosionY))
            if fromLocation_toNumber(explosionX + 64, explosionY) in walls and fromLocation_toNumber(explosionX + 32,
                                                                                                     explosionY) not in to_remove:
                to_remove.append(fromLocation_toNumber(explosionX + 64, explosionY))
        elif fromLocation_toNumber(explosionX + 32, explosionY) not in to_remove:
            to_remove.append(fromLocation_toNumber(explosionX + 32, explosionY))

    if isSteelWall(fromLocation_toNumber(explosionX - 32, explosionY)) is False:
        screen.blit(fire_IMG, (explosionX - 32, explosionY))
        if fromLocation_toNumber(explosionX - 32, explosionY) not in fire_cells:
            fire_cells.append(fromLocation_toNumber(explosionX - 32, explosionY))
        if fromLocation_toNumber(explosionX - 32, explosionY) not in walls:
            screen.blit(fire_IMG, (explosionX - 64, explosionY))
            if fromLocation_toNumber(explosionX - 64, explosionY) not in fire_cells:
                fire_cells.append(fromLocation_toNumber(explosionX - 64, explosionY))
            if fromLocation_toNumber(explosionX - 64, explosionY) in walls and fromLocation_toNumber(explosionX - 32,
                                                                                                     explosionY) not in to_remove:
                to_remove.append(fromLocation_toNumber(explosionX - 64, explosionY))
        elif fromLocation_toNumber(explosionX - 32, explosionY) not in to_remove:
            to_remove.append(fromLocation_toNumber(explosionX - 32, explosionY))

    if isSteelWall(fromLocation_toNumber(explosionX, explosionY + 32)) is False:
        screen.blit(fire_IMG, (explosionX, explosionY + 32))
        if fromLocation_toNumber(explosionX, explosionY + 32) not in fire_cells:
            fire_cells.append(fromLocation_toNumber(explosionX, explosionY + 32))
        if fromLocation_toNumber(explosionX, explosionY + 32) not in walls:
            screen.blit(fire_IMG, (explosionX, explosionY + 64))
            if fromLocation_toNumber(explosionX, explosionY + 64) not in fire_cells:
                fire_cells.append(fromLocation_toNumber(explosionX, explosionY + 64))
            if fromLocation_toNumber(explosionX, explosionY + 64) in walls and fromLocation_toNumber(explosionX,
                                                                                                     explosionY + 64) not in to_remove:
                to_remove.append(fromLocation_toNumber(explosionX, explosionY + 64))
        elif fromLocation_toNumber(explosionX, explosionY + 32) not in to_remove:
            to_remove.append(fromLocation_toNumber(explosionX, explosionY + 32))

    if isSteelWall(fromLocation_toNumber(explosionX, explosionY - 32)) is False:
        screen.blit(fire_IMG, (explosionX, explosionY - 32))
        if fromLocation_toNumber(explosionX, explosionY - 32) not in fire_cells:
            fire_cells.append(fromLocation_toNumber(explosionX, explosionY - 32))
        if fromLocation_toNumber(explosionX, explosionY - 32) not in walls:
            screen.blit(fire_IMG, (explosionX, explosionY - 64))
            if fromLocation_toNumber(explosionX, explosionY - 64) not in fire_cells:
                fire_cells.append(fromLocation_toNumber(explosionX, explosionY - 64))
            if fromLocation_toNumber(explosionX, explosionY - 64) in walls and fromLocation_toNumber(explosionX,
                                                                                                     explosionY - 64) not in to_remove:
                to_remove.append(fromLocation_toNumber(explosionX, explosionY - 64))
        elif fromLocation_toNumber(explosionX, explosionY - 32) not in to_remove:
            to_remove.append(fromLocation_toNumber(explosionX, explosionY - 32))

    explosion_state = 'on'


def fromNumber_toLocation(position):
    x_position = - 32
    y_position = - 32

    if 0 <= position < x_places * y_places:
        x_position = position - (x_places * (position // x_places))
        y_position = position // x_places

    return x_position * 32, y_position * 32


def fromLocation_toNumber(x_position, y_position):
    if 0 <= x_position < x_places * 32 and 0 <= y_position < y_places * 32:
        return ((y_position / 32) * x_places) + (x_position / 32)
    else:
        return - 40


def isSteelWall(position):
    n_vertical = position // x_places

    if n_vertical % 2 == 0:
        return False
    else:
        if (position - (x_places * (position // x_places))) % 2 == 0:
            return False
        else:
            return True


walls = []


def setting_all_walls():
    not_allowed = [0, 1, 2, x_places, 2 * x_places]
    walls.append(2)
    walls.append(2 * x_places)
    global number_of_walls

    if number_of_walls < 4:
        number_of_walls = 4

    while len(walls) < number_of_walls:
        a = random.randint(3, x_places * y_places)
        if (a not in not_allowed) and (a not in walls) and isSteelWall(a) is False:
            walls.append(a)
            if len(walls) == 3:
                global door_location
                door_location = a
            if len(walls) == 4:
                global key_location
                key_location = a


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (32 * x_steel_walls, 32 * y_steel_walls))


# Game Loop

time_counter = 0
explosion_counter = 0
running = True
Game_Over = 'False'

setting_all_walls()

while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 153, 76))
    pygame.time.delay(speed_delay)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if Game_Over is not 'True':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and (fromLocation_toNumber(thiefX - 32, thiefY) not in walls):
                    thiefX_change = -32
                    isInverted = 0
                if event.key == pygame.K_RIGHT and (fromLocation_toNumber(thiefX + 32, thiefY) not in walls):
                    thiefX_change = 32
                    isInverted = 1
                if event.key == pygame.K_UP and (fromLocation_toNumber(thiefX, thiefY - 32) not in walls):
                    thiefY_change = -32
                if event.key == pygame.K_DOWN and (fromLocation_toNumber(thiefX, thiefY + 32) not in walls):
                    thiefY_change = 32
                if event.key == pygame.K_SPACE:
                    if bomb_state is 'ready':
                        bombX = thiefX
                        bombY = thiefY
                        bomb(thiefX, thiefY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP \
                        or event.key == pygame.K_DOWN:
                    thiefX_change = 0
                    thiefY_change = 0

        thiefX += thiefX_change
        thiefY += thiefY_change

    setup_walls()
    collision = False
    collision = isCollision(thiefX, thiefY)
    if collision:
        thiefX = thiefX - thiefX_change
        thiefY = thiefY - thiefY_change

    if thiefX <= 0:
        thiefX = 0
    elif thiefX >= 64 * x_steel_walls:
        thiefX = 64 * x_steel_walls

    if thiefY <= 0:
        thiefY = 0
    elif thiefY >= 64 * y_steel_walls:
        thiefY = 64 * y_steel_walls

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

        if fromLocation_toNumber(thiefX, thiefY) in fire_cells:
            game_over_text()
            Game_Over = 'True'

        if explosion_counter > 1000:
            explosion_counter = 0
            explosion_state = 'off'
            for x in to_remove:
                if x in walls:
                    walls.remove(x)
                    if x == door_location:
                        door_state = 'closed'
                    if x == key_location:
                        key_state = 'found'
            fire_cells = []

    if key_state is 'found':
        key(key_location)
        if fromLocation_toNumber(thiefX, thiefY) == key_location:
            key_state = ''
            door_state = 'open'

    door(door_location)
    setup_grid()
    thief(thiefX, thiefY, isInverted)
    pygame.display.update()
