import pygame
import math

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Collision Triple Check: Circle, AABB, OBB")

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("arial", 24, bold=True)

def get_rotated_vertices(center, size, angle):
    rad = math.radians(-angle)
    hw, hh = size / 2, size / 2
    points = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    rotated = []
    for x, y in points:
        rx = center[0] + x * math.cos(rad) - y * math.sin(rad)
        ry = center[1] + x * math.sin(rad) + y * math.cos(rad)
        rotated.append(pygame.Vector2(rx, ry))
    return rotated

def get_axes(vertices):
    axes = []
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        edge = p2 - p1
        normal = pygame.Vector2(-edge.y, edge.x).normalize()
        axes.append(normal)
    return axes

def project(vertices, axis):
    dots = [vertex.dot(axis) for vertex in vertices]
    return min(dots), max(dots)

def check_obb_collision(v1, v2):
    axes = get_axes(v1) + get_axes(v2)
    for axis in axes:
        min1, max1 = project(v1, axis)
        min2, max2 = project(v2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True

moving_size = 60
moving_rect_x = 100
moving_rect_y = 100
velocity = 5

static_size = 150
static_center = pygame.Vector2(screen_width // 2, screen_height // 2)

angle = 0
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: moving_rect_x -= velocity
    if keys[pygame.K_RIGHT]: moving_rect_x += velocity
    if keys[pygame.K_UP]: moving_rect_y -= velocity
    if keys[pygame.K_DOWN]: moving_rect_y += velocity

    angle += 5 if keys[pygame.K_z] else 1
    moving_center = pygame.Vector2(moving_rect_x + moving_size // 2, moving_rect_y + moving_size // 2)

    v1_obb = get_rotated_vertices(static_center, static_size, angle)
    v2_obb = get_rotated_vertices(moving_center, moving_size, 0)
    
    static_aabb = pygame.Rect(0, 0, 0, 0)
    static_aabb.left = min(v.x for v in v1_obb)
    static_aabb.top = min(v.y for v in v1_obb)
    static_aabb.width = max(v.x for v in v1_obb) - static_aabb.left
    static_aabb.height = max(v.y for v in v1_obb) - static_aabb.top
    
    moving_aabb = pygame.Rect(moving_rect_x, moving_rect_y, moving_size, moving_size)

    dist = moving_center.distance_to(static_center)
    circle_hit = dist < (moving_size // 2 + static_size // 2)
    aabb_hit = static_aabb.colliderect(moving_aabb)
    obb_hit = check_obb_collision(v1_obb, v2_obb)

    screen.fill(RED if obb_hit else WHITE)

    pygame.draw.polygon(screen, GRAY, v1_obb)
    pygame.draw.polygon(screen, GRAY, v2_obb)

    pygame.draw.rect(screen, YELLOW, static_aabb, 1)
    pygame.draw.rect(screen, YELLOW, moving_aabb, 1)

    pygame.draw.polygon(screen, GREEN, v1_obb, 2)
    pygame.draw.polygon(screen, GREEN, v2_obb, 2)

    pygame.draw.circle(screen, BLUE, (int(static_center.x), int(static_center.y)), static_size // 2, 1)
    pygame.draw.circle(screen, BLUE, (int(moving_center.x), int(moving_center.y)), moving_size // 2, 1)

    status_labels = [
        (f"Circle: {'HIT' if circle_hit else 'SAFE'}", BLUE),
        (f"AABB: {'HIT' if aabb_hit else 'SAFE'}", YELLOW),
        (f"OBB: {'HIT' if obb_hit else 'SAFE'}", GREEN)
    ]

    for i, (msg, color) in enumerate(status_labels):
        text_surface = font.render(msg, True, color if color != YELLOW else (200, 200, 0))
        screen.blit(text_surface, (20, 20 + (i * 35)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()