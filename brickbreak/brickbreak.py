import pygame
import sys
from src.entities import Ball, Paddle, FPSCounter, Brick, BrickGrid

### COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

pygame.display.set_caption("Brick Break")
pygame.mouse.set_visible(False)

windowSize = width, height = 800, 600
screen = pygame.display.set_mode(windowSize)

clock = pygame.time.Clock()

ball_radius = 5
ball = Ball([screen.get_width()/2 - ball_radius/2, screen.get_height()/2 - ball_radius/2], [0, 3], WHITE, ball_radius)
paddle = Paddle([0, 550], [60, 8], WHITE)

brick_grid = BrickGrid([40, 40], 10, 30, screen.get_width() - 80, 200)

fpsCounter = FPSCounter("Arial", 12, (5, 5), WHITE)

while True:
    clock.tick(144) # caps fps at 144

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    fpsCounter.update(screen, clock)
    paddle.update(screen)
    brick_grid.update(screen)
    ball.update(screen, paddle, brick_grid.bricks)

    pygame.display.flip()

pygame.quit()