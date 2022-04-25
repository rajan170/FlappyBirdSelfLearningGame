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
        self.tick_count += 1  # Movement per frame in seconds

        displacement = self.vel * self.tick_count + 1.5 * \
            self.tick_count**2  # Calculates moving up and down
        # -10.5   *     1           + 1.5 * 1**2= -9, meaning move 9 units up when 1 sec elapses
        if displacement >= 16:
            displacement = 16
        if displacement < 0:
            displacement = -2
        self.y = self.y + displacement

        # when tilting the bird upwards
        # used to determine the tilt of the bird face when going up and down, from the starting point
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:  # tilt the bird only if the current tilt is less than the max allowed rotation/tilt
                # limit the tilt so we dont tilt or rotate the bird by a larger degree
                self.tilt = self.MAX_ROTATION
        else:  # when the bird is being tilted downwards
            if self.tilt > -90:  # we want to show the bird tilt downwards at a 90 deg to show it in a free fall
                self.tilt -= self.ROTATIONAL_VEL

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
