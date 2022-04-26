import pygame
import time
import neat
import os
import random

WINDOW_WIDTH = 575
WINDOW_HEIGHT = 775

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
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:  # tilt the bird only if the current tilt is less than the max allowed rotation/tilt
                # limit the tilt so we dont tilt or rotate the bird by a larger degree
                self.tilt = self.MAX_ROTATION
        else:  # when the bird is being tilted downwards
            if self.tilt > -90:  # we want to show the bird tilt downwards at a 90 deg to show it in a free fall
                self.tilt -= self.ROTATIONAL_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:  # Bird flapping animation
            self.img = self.IMGS[0]  # bird's wing flappig images are rotated
        elif self.img_count < self.ANIMATION_TIME * 2:  # to animate the flapping motion of the bird
            self.img = self.IMGS[1]  # based on the time
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, bird, pipes, base, score):
    # draw background image at origin at the top left corner
    win.blit(BACKGROUND_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    bird.draw(win)
    pygame.display.update()


class Pipe:
    GAP = 200
    VEL = 5  # movement of pipes relative to the bird

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(
            PIPE_IMG, False, True)  # flip the pipe vertically
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False  # to keep count of pipes passed by the bird
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height-self.PIPE_TOP.get_height()
        self.bottom = self.height+self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        # top and bottom masks used to figure out the collision of two boxes,ex. bird with the pipe
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x-bird.x, self.top-round(bird.y))
        bottom_offset = (self.x-bird.x, self.bottom-round(bird.y))

        # to detect overlap/collision of two different boxes
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if bottom_point or top_point:  # returns true on collision over overlap of pixels
            return True
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1+self.WIDTH < 0:
            self.x1 = self.x2+self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1+self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    run = True

    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move()

        add_pipe = False
        removed_pipes = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed_pipes.append(pipe)

            if not pipe.passed and pipe.x < bird.x:  # bird hasn't passed the pipe yet
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        for r in removed_pipes:
            pipes.remove(r)

        if bird.y+bird.img.get_height() >= 730:
            pass

        base.move()
        draw_window(win, bird, pipes, base)
    pygame.quit()
    quit()


main()
