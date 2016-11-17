import pygame
import sys
from src.entities import Ball, Paddle, FPSCounter, Brick, BrickGrid
from src.spatial import SpatialHash

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
ball = Ball([screen.get_width()/2 - ball_radius/2, screen.get_height()/2 - ball_radius/2], [0, 2], WHITE, ball_radius)
paddle = Paddle([0, 550], [60, 8], WHITE)

brick_grid = BrickGrid([40, 40], 10, 30, screen.get_width() - 80, 200)

fpsCounter = FPSCounter("Arial", 12, (5, 5), WHITE)

brick_hash = SpatialHash(width, height, 10, 10, brick_grid.get_bricks())

while True:
    clock.tick(144) # caps fps at 144

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    fpsCounter.update(screen, clock)
    paddle.update(screen)
    brick_grid.update(screen)

    bricks_near_ball = brick_hash.get_nearby(ball.get_rect())
    ball.update(screen, paddle, bricks_near_ball)

    pygame.display.flip()

pygame.quit()
