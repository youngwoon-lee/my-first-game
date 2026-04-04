import pygame
import random
import sys

pygame.init()

def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)

WIDTH, HEIGHT = 800, 600
CELL = 20
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
DARK = (30, 150, 30)
RED = (220, 50, 50)
GRAY = (40, 40, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

LEVELS = {
    1: {"speed": 8, "label": "Easy"},
    2: {"speed": 12, "label": "Normal"},
    3: {"speed": 18, "label": "Hard"},
}

def new_food(snake):
    while True:
        pos = (
            random.randrange(0, WIDTH // CELL) * CELL,
            random.randrange(0, HEIGHT // CELL) * CELL,
        )
        if pos not in snake:
            return pos

def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (20, 20, 20), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (20, 20, 20), (0, y), (WIDTH, y))

def draw_snake(snake):
    for i, seg in enumerate(snake):
        color = DARK if i == 0 else GREEN
        pygame.draw.rect(screen, color, (*seg, CELL, CELL))
        pygame.draw.rect(screen, BLACK, (*seg, CELL, CELL), 1)

def draw_hud(score, level_label):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Level: {level_label}", True, WHITE), (10, 40))

def game_over_screen(score):
    screen.fill(GRAY)
    screen.blit(font_big.render("GAME OVER", True, RED), (220, 220))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (350, 310))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (270, 360))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def level_select_screen():
    screen.fill(GRAY)
    screen.blit(font_big.render("SNAKE", True, GREEN), (310, 160))
    for lv, info in LEVELS.items():
        screen.blit(
            font.render(f"{lv}: {info['label']}", True, WHITE), (340, 250 + lv * 40)
        )
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: return 1
                if e.key == pygame.K_2: return 2
                if e.key == pygame.K_3: return 3

def main():
    selected_level = level_select_screen()
    
    while True:
        snake = [(WIDTH // 2, HEIGHT // 2)]
        direction = (CELL, 0)
        food = new_food(snake)
        score = 0
        current_level = selected_level
        speed = LEVELS[current_level]["speed"]
        
        game_running = True
        while game_running:
            clock.tick(speed)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP and direction != (0, CELL):
                        direction = (0, -CELL)
                    elif e.key == pygame.K_DOWN and direction != (0, -CELL):
                        direction = (0, CELL)
                    elif e.key == pygame.K_LEFT and direction != (CELL, 0):
                        direction = (-CELL, 0)
                    elif e.key == pygame.K_RIGHT and direction != (-CELL, 0):
                        direction = (CELL, 0)

            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            if (head[0] < 0 or head[0] >= WIDTH or 
                head[1] < 0 or head[1] >= HEIGHT or 
                head in snake):
                if game_over_screen(score):
                    game_running = False
                    break
                else:
                    return

            snake.insert(0, head)
            if head == food:
                score += 10
                food = new_food(snake)
                if score % 50 == 0 and current_level < 3:
                    current_level = min(current_level + 1, 3)
                    speed = LEVELS[current_level]["speed"]
            else:
                snake.pop()

            screen.fill(GRAY)
            draw_grid()
            pygame.draw.rect(screen, RED, (*food, CELL, CELL))
            draw_snake(snake)
            draw_hud(score, LEVELS[current_level]["label"])
            pygame.display.flip()

if __name__ == "__main__":
    main()