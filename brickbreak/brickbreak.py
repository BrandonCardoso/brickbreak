import pygame

### COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class FPSCounter():
    def __init__(self, fontFace, fontSize, pos):
        self.pos = pos;
        self.font = pygame.font.SysFont(fontFace, fontSize)

    def draw(self, surface):
        fps = self.font.render(str(int(clock.get_fps())), True, WHITE)
        surface.blit(fps, self.pos)


class Ball():
    def __init__(self, pos, velocity, color, radius):
        self.pos = pos
        self.velocity = velocity
        self.color = color
        self.radius = radius

    def move(self, screen):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        if self.left() < 0 or self.right() > screen.get_width():
            self.velocity[0] *= -1
        if self.top() < 0 or self.bottom() > screen.get_height():
            self.velocity[1] *= -1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(round(self.pos[0], 1)), int(round(self.pos[1], 1))), self.radius)

    def left(self):
        return self.pos[0] - self.radius

    def top(self):
        return self.pos[1] - self.radius

    def right(self):
        return self.pos[0] + self.radius

    def bottom(self):
        return self.pos[1] + self.radius

pygame.init()

pygame.display.set_caption("Brick Break")
windowSize = width, height = 800, 600
screen = pygame.display.set_mode(windowSize)

clock = pygame.time.Clock()

ball = Ball([screen.get_width()/2, screen.get_height()/2], [0.1, 3], WHITE, 5)

fpsCounter = FPSCounter("Arial", 12, (5, 5))

while 1:
    clock.tick(144) # caps fps at 144

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(BLACK)

    ball.move(screen)
    ball.draw(screen)
    
    fpsCounter.draw(screen)

    pygame.display.flip()

pygame.quit()