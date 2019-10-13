from Sprite import *
from pygame.locals import *
import time
from multiprocessing import *
# from ContinuousGesturePredictor import *
from ball_tracking import *

if __name__ == "__main__": 
    #init
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    clock = pygame.time.Clock()

    # hyper parameters
    screen_width = 1024
    screen_height = 768
    gravity = 700
    jump_speed = gravity * 0.6
    game_speed = 400
    black =(0,0,0)
    white = (255,255,255)

    floor_height = screen_height / 15
    base = screen_height / 2
    health = 100

    # set up
    screen = pygame.display.set_mode((screen_width, screen_height))

    x = screen_width / 4
    y = base - 100

    player_image = pygame.image.load("player.gif").convert()
    player_image2 = pygame.image.load("player2.gif").convert()
    player = Sprite(70, 100, [0, 0], [0, 0], [player_image, player_image2], x, y , screen)



    jumping = False
    collapsing = False

    floor_image = pygame.image.load('background.gif').convert()
    floor = Sprite(screen_width, floor_height, [0, 0], [0, 0], [floor_image], 0, base , screen)

    cursor_g_image = pygame.image.load('cursor_g.gif').convert()
    cursor_g = Sprite(8,8,[0,0],[0,0],[cursor_g_image], 0,0,screen)

    cursor_r_image = pygame.image.load('cursor_r.gif').convert()
    cursor_r = Sprite(8, 8, [0, 0], [0, 0], [cursor_r_image], 0, 0, screen)

    obstacles = []
    obstacles

    block_image = pygame.image.load("obstacle.gif").convert()
    block = Sprite(40, 60, [-game_speed, 0], [0, 0],[block_image], screen_width, base - 60 , screen)
    # game loop


    memory = 0
    write_end, read_end = Pipe()
    green_proc = Process(target=main_a, args=(write_end,))
    green_proc.start()
    # detector_proc = Process(target = detector, args = (write_end,))
    # detector_proc.start()

    cursor_loc = (0,0,0,0)


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
            1
        #     1                               #nothing yet

        # msg = read_end.recv()
        # if(msg == "OVER"):
        # 	exit(0)
        # elif(msg != memory):
        #     memory = msg
        #     if(msg == 2):
        #         if(not jumping):
        #             player.speed_y = -jump_speed
        #             player.acc_y = gravity
        #             jumping = True
        #             player.setLock()
        if(read_end.poll()):
            msg = read_end.recv()
            if(msg == "OVER"):
                exit(0)
            cursor_loc = msg



        cursor_g.relocate(cursor_loc[0] * screen_width, cursor_loc[1] * screen_height)
        cursor_r.relocate(cursor_loc[2] * screen_width, cursor_loc[3] * screen_height)

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
        cursor_g.render()
        cursor_r.render()

        health_text = myfont.render('Health: ' + str(health), False, (0, 0, 255))
        print(cursor_loc[0], cursor_loc[1])
        # cursor_text = myfont.render('Loc: ' + str(int(cursor_loc[0]*screen_width)) + " , " + str(int(cursor_loc[1]*screen_height)), False, (0, 0, 255))
        screen.blit(health_text,(100, 100))
        # screen.blit(cursor_text, (100, 150))
        pygame.display.update()
        time.sleep(0.001)


    green_proc.join()
    # screen.fill(black)
    # over = myfont.render("Game Over", False, (255,0 ,0))
    # screen.blit(over, (screen_width / 2 - 30 , screen_height / 2))
    # pygame.display.update()
    #
    #
    #
    # while(True):
    #     event = pygame.event.poll()
    #     if (event.type == QUIT):
    #         sys.exit()
    #     if (event.type == KEYDOWN):
    #         if (event.key == K_q):
    #             break