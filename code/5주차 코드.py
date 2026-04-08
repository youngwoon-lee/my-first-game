import pygame
import random
import sys
import os

pygame.init()

# 1. 경로 설정
current_path = os.path.dirname(__file__) 
image_path = os.path.join(current_path, "apple.png")

def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)

WIDTH, HEIGHT = 800, 720 
GAME_TOP = 80
CELL = 40 
FPS = 10

TOTAL_CELLS = (WIDTH // CELL) * ((HEIGHT - GAME_TOP) // CELL)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
DARK = (30, 150, 30)
RED = (220, 50, 50)
PURPLE = (160, 32, 240)
GRAY = (40, 40, 40)
HUD_COLOR = (25, 25, 25)
GOLD = (255, 215, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Big Pixel Mode")
clock = pygame.time.Clock()
font_small = get_korean_font(28)
font_mid = get_korean_font(36)
font_big = get_korean_font(72)

try:
    apple_img = pygame.image.load(image_path)
    apple_img = pygame.transform.scale(apple_img, (CELL, CELL))
except Exception as e:
    apple_img = pygame.Surface((CELL, CELL))
    apple_img.fill(RED)

LEVELS = {
    1: {"speed": 6, "label": "Classic: Easy"},
    2: {"speed": 10, "label": "Classic: Normal"},
    3: {"speed": 15, "label": "Classic: Hard"},
    4: {"speed": 10, "label": "Reverse Mode"},
    5: {"speed": 10, "label": "Special Food"},
}

def new_food(snake, existing_foods=None):
    if existing_foods is None: existing_foods = []
    if len(snake) + len(existing_foods) >= TOTAL_CELLS: return None
    while True:
        pos = (random.randrange(0, WIDTH // CELL) * CELL,
               random.randrange(GAME_TOP // CELL, HEIGHT // CELL) * CELL)
        if pos not in snake and pos not in existing_foods: return pos

def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (35, 35, 35), (x, GAME_TOP), (x, HEIGHT))
    for y in range(GAME_TOP, HEIGHT, CELL):
        pygame.draw.line(screen, (35, 35, 35), (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, seg in enumerate(snake):
        color = DARK if i == 0 else GREEN
        pygame.draw.rect(screen, color, (*seg, CELL, CELL))
        pygame.draw.rect(screen, BLACK, (*seg, CELL, CELL), 1)

def draw_hud(score, speed, level_label, length):
    pygame.draw.rect(screen, HUD_COLOR, (0, 0, WIDTH, GAME_TOP))
    pygame.draw.line(screen, GREEN, (0, GAME_TOP), (WIDTH, GAME_TOP), 3)
    score_txt = font_small.render(f"SCORE: {score}", True, WHITE)
    progress_txt = font_small.render(f"FILL: {length}/{TOTAL_CELLS}", True, GOLD)
    mode_txt = font_small.render(f"MODE: {level_label}", True, GREEN)
    screen.blit(score_txt, (30, GAME_TOP // 2 - score_txt.get_height() // 2))
    screen.blit(progress_txt, (WIDTH // 2 - progress_txt.get_width() // 2, GAME_TOP // 2 - progress_txt.get_height() // 2))
    screen.blit(mode_txt, (WIDTH - mode_txt.get_width() - 30, GAME_TOP // 2 - mode_txt.get_height() // 2))

def end_screen(score, win=False):
    screen.fill(BLACK)
    if win:
        msg = font_big.render("YOU WIN!", True, GOLD)
        sub_msg = font_mid.render("Map Fully Conquered!", True, WHITE)
    else:
        msg = font_big.render("GAME OVER", True, RED)
        sub_msg = font_mid.render(f"Final Score: {score}", True, WHITE)
    retry_msg = font_small.render("Press 'R' to Restart or 'Q' to Menu", True, (150, 150, 150))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(sub_msg, (WIDTH // 2 - sub_msg.get_width() // 2, HEIGHT // 2))
    screen.blit(retry_msg, (WIDTH // 2 - retry_msg.get_width() // 2, HEIGHT // 2 + 80))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return "RESTART"
                if e.key == pygame.K_q: return "MENU"

def sub_level_select():
    screen.fill(GRAY)
    title = font_mid.render("SELECT DIFFICULTY", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))
    opts = ["1: Easy", "2: Normal", "3: Hard"]
    for i, opt in enumerate(opts):
        txt = font_mid.render(opt, True, WHITE)
        screen.blit(txt, (WIDTH // 2 - 80, 260 + i * 50))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: return 1
                if e.key == pygame.K_2: return 2
                if e.key == pygame.K_3: return 3
                if e.key == pygame.K_ESCAPE: return None

def main_menu():
    screen.fill(GRAY)
    title = font_big.render("SNAKE WORLD", True, GREEN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 140))
    modes = ["1: Classic Mode", "2: Reverse Mode", "3: Special Food Mode"]
    for i, mode in enumerate(modes):
        txt = font_mid.render(mode, True, WHITE)
        screen.blit(txt, (WIDTH // 2 - 120, 280 + i * 50))
    
    # 종료 안내 문구 추가
    quit_txt = font_small.render("Press ESC to Quit Game", True, RED)
    screen.blit(quit_txt, (WIDTH // 2 - quit_txt.get_width() // 2, 500))
    
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    res = sub_level_select()
                    return res if res else main_menu()
                if e.key == pygame.K_2: return 4
                if e.key == pygame.K_3: return 5
                if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

def main():
    while True:
        selected_level = main_menu()
        keep_playing = True
        while keep_playing:
            snake = [(WIDTH // 2 // CELL * CELL, (HEIGHT + GAME_TOP) // 2 // CELL * CELL)]
            direction = (CELL, 0)
            food = new_food(snake)
            portals, score, current_level = [], 0, selected_level
            speed = LEVELS[current_level]["speed"]
            game_running = True
            while game_running:
                clock.tick(speed)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_UP and direction != (0, CELL): direction = (0, -CELL)
                        elif e.key == pygame.K_DOWN and direction != (0, -CELL): direction = (0, CELL)
                        elif e.key == pygame.K_LEFT and direction != (CELL, 0): direction = (-CELL, 0)
                        elif e.key == pygame.K_RIGHT and direction != (-CELL, 0): direction = (CELL, 0)
                head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
                if (head[0] < 0 or head[0] >= WIDTH or head[1] < GAME_TOP or head[1] >= HEIGHT or head in snake):
                    result = end_screen(score, win=False)
                    game_running = False
                    if result == "MENU": keep_playing = False
                    break
                snake.insert(0, head)
                if len(snake) >= TOTAL_CELLS:
                    result = end_screen(score, win=True)
                    game_running = False
                    if result == "MENU": keep_playing = False
                    break
                if head == food:
                    score += 10
                    if current_level == 5 and random.random() < 0.1:
                        p1 = new_food(snake)
                        p2 = new_food(snake, [p1]) if p1 else None
                        portals = [p1, p2] if p1 and p2 else []
                        food = None
                    else:
                        food = new_food(snake)
                        portals = []
                    if current_level == 4 and len(snake) > 1:
                        snake.reverse()
                        if len(snake) >= 2: direction = (snake[0][0] - snake[1][0], snake[0][1] - snake[1][1])
                elif portals and head in portals:
                    score += 10
                    target = portals[1] if head == portals[0] else portals[0]
                    snake[0] = target
                    portals, food = [], new_food(snake)
                else:
                    snake.pop()
                screen.fill(GRAY)
                draw_grid()
                draw_hud(score, speed, LEVELS[current_level]["label"], len(snake))
                if food: screen.blit(apple_img, food)
                for p in portals: pygame.draw.rect(screen, PURPLE, (*p, CELL, CELL))
                draw_snake(snake)
                pygame.display.flip()

if __name__ == "__main__":
    main()