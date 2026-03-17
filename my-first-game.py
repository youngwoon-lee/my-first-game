import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Particle World")

clock = pygame.time.Clock()

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.max_life = random.randint(40, 70)
        self.life = self.max_life
        self.initial_size = random.randint(5, 10)
        
        colors = [
            (255, 20, 147), (0, 255, 255), (148, 0, 211), 
            (255, 255, 0), (50, 255, 50)
        ]
        self.base_color = random.choice(colors)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.12
        self.vx *= 0.97
        self.vy *= 0.97
        self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            ratio = self.life / self.max_life
            size = max(1, int(self.initial_size * ratio))
            alpha = int(ratio * 255)
            
            p_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.base_color, alpha), (size, size), size)
            surf.blit(p_surf, (int(self.x - size), int(self.y - size)), special_flags=pygame.BLEND_RGBA_ADD)

def draw_background(surface, t):
    for y in range(0, HEIGHT, 4):
        c = int(20 + 15 * math.sin(y * 0.008 + t))
        pygame.draw.rect(surface, (10, c // 2, c), (0, y, WIDTH, 4))

particles = []
running = True
time_val = 0

while running:
    screen.fill((5, 5, 15))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        for _ in range(6):
            particles.append(Particle(*mouse_pos))

    time_val += 0.04
    draw_background(screen, time_val)

    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)
        else:
            p.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()