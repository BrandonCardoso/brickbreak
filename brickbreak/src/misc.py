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
    def __init__(self, text, font_face, font_size, center_pos, color = Colors.WHITE, background = Colors.NONE, antialias = True):
        self.render = pygame.font.SysFont(font_face, font_size).render(text, antialias, color, background)
        self.size = self.render.get_size()
        self.pos = (center_pos[0] - self.size[0]/2, center_pos[1] - self.size[1]/2)

    def draw(self, surface):
        surface.blit(self.render, self.pos)
