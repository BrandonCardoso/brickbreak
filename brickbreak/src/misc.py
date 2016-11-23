import pygame.font

def clamp(n, minimum, maximum):
    return max(minimum, min(n, maximum))

class Colors():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (119, 158, 203)
    GREEN = (119, 190, 119)
    ORANGE = (255, 179, 71)
    Purple = (150, 111, 214)
    YELLOW = (253, 253, 150)
    RED = (255, 120, 120)
    NONE = (0, 0, 0, 0)


class ScreenText():
    def __init__(self, text, font_face, font_size, pos, centered, color = Colors.WHITE, background = Colors.NONE, antialias = True):
        self.render = pygame.font.SysFont(font_face, font_size).render(text, antialias, color, background)
        self.size = self.render.get_size()
        self.font_face = font_face
        self.font_size = font_size
        self.color = color
        self.background = background
        self.antialias = antialias
        if centered:
            self.pos = (pos[0] - self.size[0]/2, pos[1] - self.size[1]/2)
        else:
            self.pos = pos

        self.rect = pygame.Rect(self.pos, self.size)

    def set_text(self, text):
        self.render = pygame.font.SysFont(self.font_face, self.font_size).render(text, self.antialias, self.color, self.background)
        self.size = self.render.get_size()
        self.rect = pygame.Rect(self.pos, self.size)

    def draw(self, surface):
        surface.blit(self.render, self.pos)

    def get_rect(self):
        return self.rect