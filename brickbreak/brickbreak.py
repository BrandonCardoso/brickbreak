import pygame
import sys
from src.entities import Ball, Paddle, FPSCounter, Brick, BrickGrid
from src.spatial import SpatialHash
from src.misc import Colors, ScreenText
from src.state import GameState, GameStateRelation, GameStateManager

pygame.init()

pygame.display.set_caption("Brick Break")
pygame.mouse.set_visible(False)

windowSize = width, height = 800, 600
screen = pygame.display.set_mode(windowSize, pygame.DOUBLEBUF)

clock = pygame.time.Clock()

### title screen objects
title_text = ScreenText("BRICK BREAK", "Consolas", 48, (width/2, height/2), Colors.RED)
exit_title_text = ScreenText("Press any key to start", "Consolas", 12, (width/2, height/2 + 100), Colors.WHITE, Colors.NONE, False)

### game objects
fpsCounter = FPSCounter("Consolas", 12, (5, 5), Colors.WHITE)
ball_radius = 5
ball = Ball([screen.get_width()/2 - ball_radius/2, screen.get_height()/2 - ball_radius/2], [0, 2], Colors.WHITE, ball_radius)
paddle = Paddle([0, 550], [60, 8], Colors.WHITE)
brick_grid = BrickGrid([40, 40], 10, 30, screen.get_width() - 80, 200)
brick_hash = SpatialHash(width, height, 10, 10, brick_grid.get_bricks())

### pause screen objects
paused_text = ScreenText("PAUSED", "Consolas", 32, (width/2, height/2), Colors.BLACK, Colors.WHITE)


def clear_screen():
    screen.fill((0,0,0))

def run_title_screen():
    title_text.draw(screen)
    exit_title_text.draw(screen)

def run_game():
    fpsCounter.update(screen, clock)
    paddle.update(screen)
    brick_grid.update(screen)

    bricks_near_ball = brick_hash.get_nearby(ball.get_rect())
    ball.update(screen, paddle, bricks_near_ball)

def run_pause_screen():
    paused_text.draw(screen)

def redraw_bricks():
    brick_grid.update(screen, True)

### state
game_state_manager = GameStateManager(GameState.TITLE)
game_state_manager.add_relation(GameStateRelation("Exit Title Screen", GameState.TITLE, GameState.INGAME))
game_state_manager.add_relation(GameStateRelation("Pause Game", GameState.INGAME, GameState.PAUSED, pygame.K_p))
game_state_manager.add_relation(GameStateRelation("Pause Game", GameState.INGAME, GameState.PAUSED, pygame.K_SPACE))
game_state_manager.add_relation(GameStateRelation("Unpause Game", GameState.PAUSED, GameState.INGAME, pygame.K_p))
game_state_manager.add_relation(GameStateRelation("Unpause Game", GameState.PAUSED, GameState.INGAME, pygame.K_SPACE))

game_state_manager.add_enter_callback(GameState.INGAME, redraw_bricks)

game_state_manager.add_exit_callback(GameState.TITLE, clear_screen)
game_state_manager.add_exit_callback(GameState.PAUSED, clear_screen)

### event handlers
def handle_event(event):
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        game_state_manager.handle_key(event.key, event.mod)
        
while True:
    clock.tick(144) # caps fps at 144

    for event in pygame.event.get():
        handle_event(event)

    game_state = game_state_manager.get_state()

    if game_state == GameState.TITLE:
        run_title_screen()
    elif game_state == GameState.INGAME:
        run_game()
    elif game_state == GameState.PAUSED:
        run_pause_screen()

    pygame.display.flip()

pygame.quit()
