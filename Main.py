from Sprite import *
from pygame.locals import *
import time
#init
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

# hyper parameters
screen_width = 1024
screen_height = 768
size = screen_width, screen_height
speed = 0
gravity = 700
jump_speed = gravity * 0.6
game_speed = 400
black =(0,0,0)
white = (255,255,255)

floor_height = screen_height / 15
base = screen_height / 2
health = 3
# set up
screen = pygame.display.set_mode(size)

x = screen_width / 4
y = base - 100

player_image = pygame.image.load("player.gif").convert()
player_image2 = pygame.image.load("player2.gif").convert()
player = Sprite(70, 100, [0, 0], [0, 0], [player_image, player_image2], x, y , screen)

clock = pygame.time.Clock()

jumping = False
collapsing = False

floor_image = pygame.image.load('background.gif').convert()
floor = Sprite(screen_width, floor_height, [0, 0], [0, 0], [floor_image], 0, base , screen)



obstacles = []
obstacles

block_image = pygame.image.load("obstacle.gif").convert()
block = Sprite(40, 60, [-game_speed, 0], [0, 0],[block_image], screen_width, base - 60 , screen)
# game loop
while(True):
    event = pygame.event.poll()

    # print(event)
    if(event.type == QUIT):
        sys.exit()
    if(event.type == KEYDOWN):
        if(event.key == K_SPACE):
            if(not jumping):
                player.speed_y = -jump_speed
                player.acc_y = gravity
                jumping = True
                player.setLock()
        elif(event.key == K_q):
            sys.exit()
    elif(event.type == KEYUP):
        1                               #nothing yet
    time_passed = clock.tick()
    seconds = time_passed / 1000.0

    player.move(seconds)
    block.move(seconds)



    if(block.x + block.width < 0):
        block.x = screen_width
    if(player.collision(floor)):
        player.y = base - player.height
        jumping = False
        player.speed_y = 0
        player.acc_y = 0
        player.releaseLock()
    if(player.collision(block) and not collapsing):
        collapsing = True
        health -= 1
    elif(not player.collision(block)):
        collapsing = False

    if(health == 0): break
    screen.fill(white)
    floor.render()
    block.render()
    player.render()

    health_text = myfont.render('Health: ' + str(health), False, (0, 0, 255))
    screen.blit(health_text,(100, 100))
    pygame.display.update()
    time.sleep(0.01)


screen.fill(black)
over = myfont.render("Game Over", False, (255,0 ,0))
screen.blit(over, (screen_width / 2 - 30 , screen_height / 2))
pygame.display.update()



while(True):
    event = pygame.event.poll()
    if (event.type == QUIT):
        sys.exit()
    if (event.type == KEYDOWN):
        if (event.key == K_q):
            break