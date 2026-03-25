import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

circle_x = 400
circle_y = 300
speed = 5

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        circle_y -= speed
    if keys[pygame.K_s]:
        circle_y += speed
    if keys[pygame.K_a]:
        circle_x -= speed
    if keys[pygame.K_d]:
        circle_x += speed

    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (circle_x, circle_y), 50)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()