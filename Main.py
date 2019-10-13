from Sprite import *
from pygame.locals import *
from pygame import *
import time
from multiprocessing import *
# from ContinuousGesturePredictor import *
from ball_tracking import *
import random


def main():
    #init
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 15)
    clock = pygame.time.Clock()

    # hyper parameters
    screen_width = 1024
    screen_height = 512

    score_r = 0
    score_g = 0


    # set up
    screen = pygame.display.set_mode((screen_width, screen_height))

    # cursor_g_image = pygame.image.load('cursor_g.gif').convert()
    # cursor_g = Sprite(8,8,[0,0],[0,0],[cursor_g_image], 0,0,screen)

    # cursor_r_image = pygame.image.load('cursor_r.gif').convert()
    # cursor_r = Sprite(8, 8, [0, 0], [0, 0], [cursor_r_image], 0, 0, screen)


    ball_image = pygame.image.load("ball.gif").convert()
    ball = Sprite(64, 64, [random.randint(300,300), random.randint(300,300)], [random.randint(30, 60), random.randint(30, 60)],[ball_image], screen_width / 2, screen_height / 2, screen, Rect(0,0,screen_width, screen_height))

    gimg = pygame.image.load("player_g.gif").convert()
    player_g = Sprite(16, 48, [0,0], [0, 0],[gimg], 1024 * 7/8, 250 , screen, Rect(0,0,screen_width, screen_height))
    rimg = pygame.image.load("player_r.gif").convert()
    player_r = Sprite(16, 48, [0, 0], [0, 0], [rimg], 1024/8, 250, screen, Rect(0, 0, screen_width, screen_height))



    # game loop




    memory = 0
    write_end, read_end = Pipe()
    green_proc = Process(target=main_a, args=(write_end,))
    green_proc.start()

    cursor_loc = (1024 * 7/8,250,1024/8,250)

    collide1 = False
    collide2 = False

    collide_l = False
    collide_r = False
    time.sleep(5)
    while(True):

        event = pygame.event.poll()


        if(event.type == QUIT):
            sys.exit()
        if(event.type == KEYDOWN):
            if(event.key == K_q):
                break

        if(read_end.poll()):
            msg = read_end.recv()
            if(msg == "OVER"):
                exit(0)
            cursor_loc = msg

        player_g.relocate(player_g.x, cursor_loc[1] * screen_height)
        player_r.relocate(player_r.x, cursor_loc[3] * screen_height)

        time_passed = clock.tick()
        seconds = time_passed / 1000.0
        ball.move(seconds)
        if (ball.collision(player_r) and not collide1):
            collide1 = True
            ball.speed_x = - ball.speed_x
            ball.speed_y = - ball.speed_y
        else:
            collide1 = False

        if (ball.collision(player_g) and not collide2):
            collide2 = True
            ball.speed_x = - ball.speed_x
            ball.speed_y = - ball.speed_y
        else:
            collide2 = False

        if (ball.x <= 0):
            ball.x = 0
            if (not collide_l):
                score_g += 1
                collide_l = True
        else:
            collide_l = False

        if (ball.x + ball.width >= screen_width):
            ball.x = screen_width - ball.width
            if (not collide_r):
                score_r += 1
                collide_r = True
        else:
            collide_r = False
        if (ball.x <= 0 or ball.x + ball.width >= screen_width ):
            ball.speed_x = -ball.speed_x




        if(ball.y <= 0 or ball.y + ball.height >= screen_height):
            ball.y = min(max(0, ball.y), screen_height - ball.height)
            ball.speed_y = -ball.speed_y

        screen.fill((255,255,255))
        ball.render()
        player_g.render()
        player_r.render()
        g_text = myfont.render("R Score: " + str(score_g), False, (255, 0, 0))
        r_text = myfont.render("G Score: " + str(score_r), False, (0, 255, 0))
        screen.blit(g_text, (128, 30))
        screen.blit(r_text, (764, 30))

        pygame.display.update()
        time.sleep(0.001)


    # green_proc.join()


if __name__ == "__main__":
    main()