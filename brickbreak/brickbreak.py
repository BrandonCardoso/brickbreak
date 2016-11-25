import pygame
import sys
from src.entities import Ball, Paddle, Brick, BrickGrid
from src.spatial import SpatialHash
from src.misc import Colors, ScreenText
from src.state import GameState, GameStateRelation, GameStateManager
from src.level import LevelManager

pygame.init()
pygame.display.set_caption("Brick Break")
pygame.mouse.set_visible(False)

windowSize = width, height = 800, 600
screen = pygame.display.set_mode(windowSize, pygame.DOUBLEBUF)
dirty_rects = []

clock = pygame.time.Clock()

def clear_screen():
    screen.fill((0,0,0))
    dirty_rects.append(pygame.Rect(0, 0, width, height))

def set_level(level):
    global ball, paddle, brick_grid, brick_hash, lives, lives_text, current_level, level_text
    current_level = level
    level_text = ScreenText(str(current_level), "Consolars", 12, (width - 20, 5), False, Colors.WHITE, Colors.NONE, False)
    ball = Ball([screen.get_width()/2 - ball_radius/2, screen.get_height()/2 - ball_radius/2], [0, -2], Colors.WHITE, ball_radius)
    paddle = Paddle([0, 550], [60, 8], Colors.WHITE)
    brick_grid = BrickGrid(level_manager.get_level_layout(current_level), [40, 40], screen.get_width() - 80, 200)
    brick_hash = SpatialHash(width, height, 5, 5, brick_grid.get_bricks())
    clear_screen()

def reset_game():
    global lives, lives_text
    lives = 3
    lives_text = ScreenText("Lives: " + str(lives), "Consolas", 12, (5, height - 12 - 5), False, Colors.WHITE, Colors.NONE, False)
    set_level(1)

def next_level():
    global current_level
    set_level(current_level + 1)

### title screen objects
title_text = ScreenText("BRICK BREAK", "Consolas", 48, (width/2, height/2), True, Colors.RED)
exit_title_text = ScreenText("Press any key to start", "Consolas", 12, (width/2, height/2 + 100), True, Colors.WHITE, Colors.NONE, False)

### game objects
fps_counter = ScreenText(0, "Consolas", 12, (5, 5), False, Colors.WHITE, Colors.NONE, False)
ball_radius = 5
level_manager = LevelManager("\src\levels.json")
reset_game()

### pause screen objects
paused_text = ScreenText("PAUSED", "Consolas", 32, (width/2, height/2), True, Colors.BLACK, Colors.WHITE)

### game over objects
game_over_text = ScreenText("GAME OVER", "Consolas", 48, (width/2, height/2), True, Colors.RED)
reset_text = ScreenText("Press any key to restart", "Consolas", 12, (width/2, height/2 + 100), True, Colors.WHITE, Colors.NONE, False)

### cleared/victory screen objects
victory_text = ScreenText("CLEARED", "Consolas", 48, (width/2, height/2), True, Colors.BLUE)
# reset_tex

def run_title_screen():
    global dirty_rects
    title_text.draw(screen)
    exit_title_text.draw(screen)
    dirty_rects.extend([title_text.get_rect(),
                        exit_title_text.get_rect()])

def run_game():
    level_text.draw(screen)
    lives_text.draw(screen)
    dirty_rects.extend([lives_text.get_rect(),
                        level_text.get_rect()])

    dirty_rects.extend([paddle.get_rect(), ball.get_rect()])
    paddle.update(screen)

    brick_grid.update(screen)

    bricks_near_ball = brick_hash.get_nearby(ball.get_rect())
    ball.update(screen, paddle, bricks_near_ball)

    dirty_rects.extend([paddle.get_rect(), ball.get_rect()])
    dirty_rects.extend(brick_grid.get_dirty())

    if ball.get_rect().bottom >= height:
        global lives
        lives -= 1
        lives_text.set_text("Lives: " + str(lives))
        ball.reset()
        if lives <= 0:
            game_state_manager.set_state(GameState.GAMEOVER)

    if len(brick_grid.get_bricks()) <= 0:
        game_state_manager.set_state(GameState.CLEARED)

def run_pause_screen():
    paused_text.draw(screen)
    dirty_rects.append(paused_text.get_rect())

def run_game_over_screen():
    game_over_text.draw(screen)
    reset_text.draw(screen)
    dirty_rects.extend([game_over_text.get_rect(),
                        reset_text.get_rect()])

def run_victory_screen():
    victory_text.draw(screen)
    reset_text.draw(screen)
    dirty_rects.extend([victory_text.get_rect(),
                        reset_text.get_rect()])

def unpause():
    clear_screen()
    redraw_bricks()

def redraw_bricks():
    brick_grid.update(screen, True)


### state
game_state_manager = GameStateManager(GameState.TITLE)
game_state_manager.add_relation(GameStateRelation("Exit Title Screen",
                                                  GameState.TITLE, GameState.INGAME,
                                                  None, None, clear_screen))
game_state_manager.add_relation(GameStateRelation("Pause Game",
                                                  GameState.INGAME, GameState.PAUSED,
                                                  pygame.K_p, None, clear_screen))
game_state_manager.add_relation(GameStateRelation("Pause Game",
                                                  GameState.INGAME, GameState.PAUSED,
                                                  pygame.K_SPACE))
game_state_manager.add_relation(GameStateRelation("Unpause Game",
                                                  GameState.PAUSED, GameState.INGAME,
                                                  pygame.K_p, None, unpause))
game_state_manager.add_relation(GameStateRelation("Unpause Game",
                                                  GameState.PAUSED, GameState.INGAME,
                                                  pygame.K_SPACE, None, unpause))
game_state_manager.add_relation(GameStateRelation("Restart Game",
                                                  GameState.GAMEOVER, GameState.INGAME,
                                                  None, None, reset_game))
game_state_manager.add_relation(GameStateRelation("Next Level",
                                                  GameState.CLEARED, GameState.INGAME,
                                                  None, None, next_level))

### event handlers
def handle_event(event):
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        game_state_manager.handle_key(event.key, event.mod)
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if game_state_manager.get_state() == GameState.INGAME:
            ball.launch(paddle)

while True:
    screen.fill(Colors.BLACK)
    clock.tick(144) # caps fps at 144

    dirty_rects = [] # clear dirty rectangles

    fps_counter.set_text(str(int(clock.get_fps())))
    fps_counter.draw(screen)
    dirty_rects.append(fps_counter.get_rect())

    for event in pygame.event.get():
        handle_event(event)

    game_state = game_state_manager.get_state()

    if game_state == GameState.TITLE:
        run_title_screen()
    elif game_state == GameState.INGAME:
        run_game()
    elif game_state == GameState.PAUSED:
        run_pause_screen()
    elif game_state == GameState.GAMEOVER:
        run_game_over_screen()
    elif game_state == GameState.CLEARED:
        run_victory_screen()

    if len(dirty_rects) > 0:
        pygame.display.update(dirty_rects)

pygame.quit()
