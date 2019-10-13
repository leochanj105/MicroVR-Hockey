
import sys, pygame
from pygame.locals import *
def normal_obstacles(split):
    return None


class Sprite:
    fps = 0.04
    max_speed = 900
    def __init__(self, width, height, speed, acceleration, images, x, y, screen, bound):
        self.width = width
        self.height = height
        self.speed_x = speed[0]
        self.speed_y = speed[1]
        self.acc_x = acceleration[0]
        self.acc_y = acceleration[1]
        self.images = []
        for image in images:
            self.images.append(pygame.transform.scale(image, (int(width), int(height) )))
        self.x = x
        self.y = y
        self.screen = screen
        self.current_frame = 0
        self.frame_count = len(images)
        self.cum_secs = 0.0
        self.lock = True
        self.bound = bound
    def render(self):
        self.screen.blit(self.images[self.current_frame], (self.x, self.y), (0, 0, self.width, self.height))

    def collision(self, other):
        min_x = min(self.x, other.x)
        max_x = max(self.x + self.width, other.x + other.width)
        min_y = min(self.y, other.y)
        max_y = max(self.y + self.height, other.y + other.height)
        return ((max_x - min_x) < self.width + other.width) and ((max_y - min_y) < self.height + other.height)
    def move(self, interval):
        self.speed_x += self.acc_x * interval
        self.speed_y += self.acc_y * interval

        self.x += self.speed_x * interval
        self.y += self.speed_y * interval


        # if(self.speed_x >= Sprite.max_speed or self.speed_x <= 0):
        #     self.acc_x = 0
        # if (self.speed_y >= Sprite.max_speed or self.speed_y <= 0):
        #     self.acc_ya = 0
        if(not self.lock):
            self.cum_secs += interval
            if(self.cum_secs >= Sprite.fps):
                self.cum_secs = 0
                self.current_frame = (self.current_frame + 1) % self.frame_count

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0
        self.acc_x = 0
        self.acc_y = 0
    def setLock(self):
        self.lock = True
    def releaseLock(self):
        self.lock = False
    def relocate(self, x, y):
        self.x = x
        self.y = y

    def scale(self, scale):
        self.width = self.width * scale
        self.height = self.height * scale





