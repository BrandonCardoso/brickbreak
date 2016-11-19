import abc
import pygame
import random
import src.geometry as geometry
from src.misc import Colors, clamp

class Entity(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, pos):
        self.pos = pos

    def get_rect(self):
        return pygame.Rect(self.pos, self.size)

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
        size = fps.get_size()
        pygame.draw.rect(surface, (0, 0, 0), self.pos + size)
        surface.blit(fps, self.pos)

    def update(self, surface, clock):
        self.draw(surface, clock)

class Ball(Entity):
    def __init__(self, pos, velocity, color, radius):
        Entity.__init__(self, pos)
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.max_speed = 3

    def move(self):
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

    def draw(self, surface, color):
        pygame.draw.circle(surface, color, (int(round(self.pos[0], 1)) + self.radius, int(round(self.pos[1], 1))+ self.radius), self.radius)
        #pygame.draw.rect(surface, (255, 0, 0), self.get_rect(), 1) # hitbox

    def left(self):
        return self.pos[0]

    def top(self):
        return self.pos[1]

    def right(self):
        return self.pos[0] + self.radius * 2

    def bottom(self):
        return self.pos[1] + self.radius * 2

    def center(self):
        return (self.pos[0] + self.radius, self.pos[1] + self.radius)

    def get_collision_point(self, rect):
        nearest_point = geometry.nearest_point_on_rect(self.center(), rect)
        dist = geometry.dist(self.center(), nearest_point)

        if (dist[0] ** 2) + (dist[1] ** 2) < self.radius**2:
            return nearest_point
        else:
            return None

    def check_paddle_collision(self, paddle):
        point = self.get_collision_point(paddle.get_rect())

        if point:
            self.velocity[0] = clamp(self.velocity[0] + paddle.velocity_x * paddle.friction,
                                     -1 * self.max_speed, self.max_speed)
            self.bounce(point)

    def check_wall_collision(self, screen):
        if self.left() < 0 or self.right() > screen.get_width():
            self.velocity[0] *= -1
        if self.top() < 0 or self.bottom() > screen.get_height():
            self.velocity[1] *= -1

    def check_brick_collisions(self, bricks):
        for brick in bricks:
            if not brick.hit:
                collision_point = self.check_brick_collision(brick)
                if collision_point:
                    brick.was_hit()
                    self.bounce(collision_point)
                    return

    def check_brick_collision(self, brick):
        return self.get_collision_point(brick.get_rect())

    def get_rect(self):
        return pygame.Rect(self.pos, (self.radius * 2, self.radius * 2))

    def update(self, surface, paddle, bricks):
        self.check_paddle_collision(paddle)
        self.check_wall_collision(surface)
        self.check_brick_collisions(bricks)
        self.erase(surface)
        self.move()
        self.draw(surface, self.color)

    def erase(self, surface):
        self.draw(surface, (0, 0, 0))

    def bounce(self, point):
        middle_x = self.left() + self.radius
        middle_y = self.top() + self.radius

        if middle_x == point[0]:
            self.velocity[1] *= -1
        elif middle_y == point[1]:
            self.velocity[0] *= -1

class Paddle(Entity):
    def __init__(self, pos, size, color):
        Entity.__init__(self, pos)
        self.size = size
        self.color = color
        self.velocity_x = 0
        self.friction = 0.2

    def move(self):
        old_x = self.pos[0]
        self.pos[0] = pygame.mouse.get_pos()[0] - self.size[0] / 2
        self.velocity_x = self.pos[0] - old_x

    def draw(self, surface, color):
        pygame.draw.rect(surface, color, self.get_rect())
        #pygame.draw.rect(screen, (255, 0, 0), self.get_rect(), 1) # hitbox

    def update(self, surface):
        self.erase(surface)
        self.move()
        self.draw(surface, self.color)

    def erase(self, surface):
        self.draw(surface, (0, 0, 0))

class Brick(Entity):
    def __init__(self, pos, size, color):
        Entity.__init__(self, pos)
        self.size = size
        self.color = color
        self.border_color = map(lambda x: x * 0.9, self.color)
        self.hit = False
        self.need_update = True
        self.remove = False

    def was_hit(self):
        self.hit = True
        self.need_update = True

    def erase(self, surface):
        pygame.draw.rect(surface, (0,0,0), self.get_rect())

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.get_rect())
        pygame.draw.rect(surface, self.border_color, self.get_rect(), 1)
        #pygame.draw.rect(surface, (255, 0, 0), self.get_rect(), 1) # hitbox

    def update(self, surface, force_redraw = False):

        if self.need_update or force_redraw:
            if self.hit:
                self.erase(surface)
                self.remove = True
            else:
                self.draw(surface)

            self.need_update = False

class BrickGrid():
    def __init__(self, pos, rows, cols, width, height):
        self.bricks = []
        for i in range(0, rows):
            for j in range(0, cols):            
                self.bricks.append(Brick([j * width / cols + pos[1], i * height / rows + pos[0]],
                    [width / cols, height / rows],
                    Colors.WHITE))

    def update(self, surface, force_redraw = False):
        self.bricks = filter(lambda x: not x.remove, self.bricks) # remove hit bricks

        for brick in self.bricks:
            brick.update(surface, force_redraw)

    def get_bricks(self):
        return self.bricks
