import pygame
import sys
from src.entities import Ball, Paddle, FPSCounter, Brick, BrickGrid
from src.spatial import SpatialHash
from src.misc import Colors
from src.state import GameState, GameStateRelation, GameStateManager

pygame.init()

pygame.display.set_caption("Brick Break")
pygame.mouse.set_visible(False)

windowSize = width, height = 800, 600
screen = pygame.display.set_mode(windowSize, pygame.DOUBLEBUF)

clock = pygame.time.Clock()

### title screen objects
title_text = "BRICK BREAK"
title_font = pygame.font.SysFont("Consolas", 48)
title_text_render = title_font.render(title_text, True, Colors.RED)
title_text_size = title_text_render.get_size()
title_text_pos = (width/2 - title_text_size[0]/2, height/2 - title_text_size[1]/2)

### game objects
fpsCounter = FPSCounter("Arial", 12, (5, 5), Colors.WHITE)
ball_radius = 5
ball = Ball([screen.get_width()/2 - ball_radius/2, screen.get_height()/2 - ball_radius/2], [0, 2], Colors.WHITE, ball_radius)
paddle = Paddle([0, 550], [60, 8], Colors.WHITE)
brick_grid = BrickGrid([40, 40], 10, 30, screen.get_width() - 80, 200)
brick_hash = SpatialHash(width, height, 10, 10, brick_grid.get_bricks())

### pause screen objects
paused_text = "PAUSED"
paused_font = pygame.font.SysFont("Consolas", 32)
paused_text_render = paused_font.render(paused_text, True, Colors.BLACK, Colors.WHITE)
paused_text_size = paused_text_render.get_size()
paused_text_pos = (width/2 - paused_text_size[0]/2, height/2 - paused_text_size[1])


def run_title_screen():
    screen.blit(title_text_render, title_text_pos)

def run_game():
    fpsCounter.update(screen, clock)
    paddle.update(screen)
    brick_grid.update(screen)

    bricks_near_ball = brick_hash.get_nearby(ball.get_rect())
    ball.update(screen, paddle, bricks_near_ball)

def run_pause_screen():
    screen.blit(paused_text_render, paused_text_pos)


### state
game_state_manager = GameStateManager(GameState.TITLE)
game_state_manager.add_relation(GameStateRelation("Exit Title Screen", GameState.TITLE, GameState.INGAME))
game_state_manager.add_relation(GameStateRelation("Pause Game", GameState.INGAME, GameState.PAUSED, pygame.K_p))
game_state_manager.add_relation(GameStateRelation("Unpause Game", GameState.PAUSED, GameState.INGAME, pygame.K_ESCAPE))
game_state_manager.add_relation(GameStateRelation("Unpause Game", GameState.PAUSED, GameState.INGAME, pygame.K_p))

### event handlers
def handle_event(event):
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        game_state_manager.handle_key(event.key, event.mod)
        
while True:
    clock.tick(144) # caps fps at 144

    game_state = game_state_manager.get_state()

    for event in pygame.event.get():
        handle_event(event)

    if game_state == GameState.TITLE:
        run_title_screen()
    elif game_state == GameState.INGAME:
        run_game()
    elif game_state == GameState.PAUSED:
        run_pause_screen()

    pygame.display.flip()

pygame.quit()
