import abc
import pygame


class Entity(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, pos):
        self.pos = pos

    @abc.abstractmethod
    def update():
        return


class FPSCounter(Entity):
    def __init__(self, fontFace, fontSize, pos, color):
        Entity.__init__(self, pos)
        self.font = pygame.font.SysFont(fontFace, fontSize)
        self.color = color

    def draw(self, surface, clock):
        fps = self.font.render(str(int(clock.get_fps())), True, self.color)
        surface.blit(fps, self.pos)

    def update(self, surface, clock):
        self.draw(surface, clock)


class Ball(Entity):
    def __init__(self, pos, velocity, color, radius):
        Entity.__init__(self, pos)
        self.velocity = velocity
        self.color = color
        self.radius = radius

    def move(self, surface, paddle):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.check_paddle_collision(paddle)
        self.check_wall_collision(surface)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(round(self.pos[0], 1)), int(round(self.pos[1], 1))), self.radius)
        #pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 1) # hitbox

    def left(self):
        return self.pos[0] - self.radius

    def top(self):
        return self.pos[1] - self.radius

    def right(self):
        return self.pos[0] + self.radius

    def bottom(self):
        return self.pos[1] + self.radius

    def check_paddle_collision(self, paddle):
        if paddle.get_rect().colliderect(self.get_rect()):
            self.velocity[1] *= -1

    def check_wall_collision(self, screen):
        if self.left() < 0 or self.right() > screen.get_width():
            self.velocity[0] *= -1
        if self.top() < 0 or self.bottom() > screen.get_height():
            self.velocity[1] *= -1

    def get_rect(self):
        return pygame.Rect([self.left(), self.top(), self.radius * 2, self.radius * 2])

    def update(self, surface, paddle):
        self.move(surface, paddle)
        self.draw(surface)


class Paddle(Entity):
    def __init__(self, pos, size, color):
        Entity.__init__(self, pos)
        self.size = size
        self.color = color

    def move(self):
        self.pos[0] = pygame.mouse.get_pos()[0]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.pos + self.size)
        #pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 1) # hitbox

    def get_rect(self):
        return pygame.Rect(self.pos + self.size)

    def update(self, surface):
        self.move()
        self.draw(surface)