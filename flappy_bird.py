import pygame
import time
import neat
import os
import random

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 850

BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(
                os.path.join("imgs", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUND_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png")))


class Bird:
    IMGS = BIRD_IMG
    MAX_ROTATION = 25
    ROTATIONAL_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5  # Negative velocity to make the bird jump because in pygame
        # the coordinate sysem's origin is at the top left corner of the screen,
        # so to make something go down we need negative velocity.
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1  # Movement per frame

    def
