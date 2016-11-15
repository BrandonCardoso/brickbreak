import pygame
import sys
import random
from src.entities import Ball, Paddle, FPSCounter, Brick

### COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 120, 120)
PURPLE = (150, 111, 214)
GREEN = (119, 190, 119)
BLUE = (119, 158, 203)
YELLOW = (253, 253, 150)
ORANGE = (255, 179, 71)

brick_colors = {
    0: BLUE,
    1: GREEN,
    2: ORANGE,
    3: PURPLE,
    4: YELLOW,
    5: RED
}
num_brick_colors = len(brick_colors)

def generate_bricks(pos, rows, cols, grid_width, grid_height):
    bricks = []
    for i in range(0, rows):
        for j in range(0, cols):            
            bricks.append(Brick([j * grid_width / cols + pos[1], i * grid_height / rows + pos[0]],
                                [grid_width / cols, grid_height / rows],
                                brick_colors[random.randint(0, num_brick_colors - 1)]))
    return bricks

pygame.init()

pygame.display.set_caption("Brick Break")
pygame.mouse.set_visible(False)

windowSize = width, height = 800, 600
screen = pygame.display.set_mode(windowSize)

clock = pygame.time.Clock()

ball = Ball([screen.get_width()/2, screen.get_height()/2], [1, 1.5], WHITE, 5)
paddle = Paddle([0, 550], [40, 8], WHITE)

bricks = generate_bricks([40, 40], 10, 30, screen.get_width() - 80, 200)

fpsCounter = FPSCounter("Arial", 12, (5, 5), WHITE)

while 1:
    clock.tick(144) # caps fps at 144

    fpsCounter.update(screen, clock)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    paddle.update(screen)

    for brick in bricks:
        brick.update(screen)

    ball.update(screen, paddle, bricks)

    bricks = filter(lambda x: not x.remove, bricks) # remove hit bricks

    pygame.display.flip()

pygame.quit()