import pygame
import math
import base64
import io

# 1. 이미지 데이터 (이 변수 이름이 _ROCKET 인지 꼭 확인하세요)
_ROCKET = (
    "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"
    "7gAAAABJRU5ErkJggg=="
)

# 2. 이미지 로드 함수 (이 함수가 _ROCKET 을 사용합니다)
def load_sprite(name, size=None):
    if name == "rocket":
        raw = base64.b64decode(_ROCKET)
        surface = pygame.image.load(io.BytesIO(raw)).convert_alpha()
        if size:
            surface = pygame.transform.scale(surface, size)
        return surface
    return None

# --- 3. 게임 엔진 메인 설정 ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rocket OBB Visualization")

# 색상 및 크기 설정
BLACK, RED, BLUE, YELLOW, GREEN = (0, 0, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0)
static_size, moving_size = (60, 160), (40, 100)

# 고정 오브젝트 원본 및 이동 오브젝트 로드
static_img_orig = load_sprite("rocket", static_size)
moving_img = load_sprite("rocket", moving_size)

static_radius, moving_radius = static_size[1] / 2, moving_size[1] / 2
static_pos = (400, 300)
moving_rect = moving_img.get_rect(topleft=(100, 100))

angle, clock = 0, pygame.time.Clock()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # 키 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: moving_rect.x -= 5
    if keys[pygame.K_RIGHT]: moving_rect.x += 5
    if keys[pygame.K_UP]: moving_rect.y -= 5
    if keys[pygame.K_DOWN]: moving_rect.y -= 5

    # Z키 회전 부스트
    angle += 10 if keys[pygame.K_z] else 1

    # 회전 이미지 생성
    rotated_static = pygame.transform.rotate(static_img_orig, angle)
    static_rect = rotated_static.get_rect(center=static_pos)

    # 충돌 체크
    dist = math.sqrt((static_rect.centerx - moving_rect.centerx)**2 + 
                     (static_rect.centery - moving_rect.centery)**2)
    screen.fill(YELLOW if dist < (static_radius + moving_radius) else BLACK)

    # 그리기
    screen.blit(rotated_static, static_rect.topleft)
    screen.blit(moving_img, moving_rect.topleft)
    pygame.draw.rect(screen, RED, static_rect, 2)
    pygame.draw.rect(screen, RED, moving_rect, 2)
    pygame.draw.circle(screen, BLUE, static_rect.center, int(static_radius), 2)
    pygame.draw.circle(screen, BLUE, moving_rect.center, int(moving_radius), 2)

    # OBB (초록) 계산
    rad = math.radians(-angle)
    hw, hh = static_size[0]/2, static_size[1]/2
    obb_pts = []
    for cx, cy in [(-hw,-hh), (hw,-hh), (hw,hh), (-hw,hh)]:
        rx = cx * math.cos(rad) - cy * math.sin(rad)
        ry = cx * math.sin(rad) + cy * math.cos(rad)
        obb_pts.append((static_pos[0] + rx, static_pos[1] + ry))
    pygame.draw.polygon(screen, GREEN, obb_pts, 2)

    pygame.display.flip()

pygame.quit()