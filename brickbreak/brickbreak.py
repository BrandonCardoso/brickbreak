import pygame
import sys
from src.entities import Ball, Paddle, FPSCounter

### COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

pygame.display.set_caption("Brick Break")
pygame.mouse.set_visible(False)

windowSize = width, height = 800, 600
screen = pygame.display.set_mode(windowSize)

clock = pygame.time.Clock()

ball = Ball([screen.get_width()/2, screen.get_height()/2], [1, 1.5], WHITE, 5)

paddle = Paddle([0, 550], [40, 8], WHITE)

fpsCounter = FPSCounter("Arial", 12, (5, 5), WHITE)

while 1:
    clock.tick(144) # caps fps at 144
    fpsCounter.update(screen, clock)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(BLACK)

    paddle.update(screen)

    ball.update(screen, paddle)

    pygame.display.flip()

pygame.quit()