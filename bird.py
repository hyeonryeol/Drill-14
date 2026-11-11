# 새의 비행 애니메이션
#
# 1. 시트 격자: bird_animation.png(918x506)는 5열 x 3행에 14프레임이 있다.
#    눈 위치를 재 보면 열 간격은 182픽셀(918/5 = 183.6이 아님), 행 높이는 506/3이다.
# 2. 프레임 잘라내기: 격자는 정수로 나누어떨어지지 않고 2행 날개 끝이 경계를 넘으므로,
#    프레임마다 투명하지 않은 픽셀 범위만 잘라낸다.
# 3. 정렬: 칸 기준점(가로 몸 중심 107 + 182 x 열, 세로 506/3 x 행 + 90)에서
#    잘라낸 영역 중심까지의 거리 dx, dy만큼 옮겨 그린다. 좌우 떨림이 없고,
#    원본에 그려진 날갯짓에 따른 몸의 오르내림(약 12픽셀)은 그대로 살린다.
# 4. 크기와 속력: 10픽셀 = 30cm. 몸길이 1.5m, 비행 속력 시속 16~24km를 픽셀/초로 바꾼다.
# 5. 날갯짓: 날갯짓 한 번 = 14프레임. 날갯짓 한 번에 나아가는 거리를 정해 두고
#    1초당 프레임 수 = 속력 / 날갯짓 거리 x 14 로 구한다. 빨리 나는 새가 날갯짓도 빠르다.
# 6. 모든 움직임은 속력 x frame_time 이라 FPS와 상관없이 같은 빠르기로 날고 날갯짓한다.
# 7. 좌우 반복: 화면 끝에서 방향을 바꾸고, 왼쪽으로 날 때는 몸 중심을 축으로 좌우 반전한다.

import random

from pico2d import get_canvas_width, load_image

import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

# 원본 몸길이(부리 끝 ~ 꼬리 끝) 146픽셀을 1.5m로 그린다
BIRD_LENGTH_M = 1.5
BIRD_SCALE = BIRD_LENGTH_M * PIXEL_PER_METER / 146

# Bird Fly Speed
FLY_SPEED_KMPH = 20.0  # Km / Hour
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)
MIN_FLY_SPEED_KMPH, MAX_FLY_SPEED_KMPH = 16.0, 24.0  # 새마다 속력이 다르다

# bird_animation.png 프레임 데이터 (left, bottom, width, height, dx, dy)
# 5열 x 3행에 14프레임. 프레임마다 투명하지 않은 픽셀 범위만 잘라낸다.
# 칸의 기준점(가로 182픽셀 격자, 세로 506/3 격자)을 몸 중심으로 삼고,
# 잘라낸 영역의 중심이 기준점에서 떨어진 거리를 dx, dy로 둔다.
FRAMES = (
    (34, 362, 146, 143, 0, 17.5),
    (216, 363, 146, 141, 0, 17.5),
    (398, 364, 146, 130, 0, 13),
    (555, 367, 171, 122, -12.5, 12),
    (728, 370, 182, 88, -16, -2),
    (34, 171, 146, 118, 0, -17.3),
    (216, 166, 146, 124, 0, -19.3),
    (398, 170, 146, 120, 0, -17.3),
    (580, 180, 146, 109, 0, -12.8),
    (762, 177, 146, 110, 0, -15.3),
    (34, 6, 146, 108, 0, -18.7),
    (216, 6, 146, 106, 0, -19.7),
    (376, 23, 168, 88, -11, -11.7),
    (546, 22, 180, 114, -17, 0.3),
)
FRAMES_PER_FLAP = len(FRAMES)

# 날갯짓: 기본 속력에서 1초에 3번
FLAPS_PER_SECOND = 3.0

# 날갯짓 한 번에 나아가는 거리 (소년의 보폭과 같은 개념)
FLAP_DISTANCE_M = FLY_SPEED_MPS / FLAPS_PER_SECOND


class Bird:
    image = None

    def __init__(self, x, y, direction):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = random.uniform(0, FRAMES_PER_FLAP)  # 날갯짓 시작 위상
        self.dir = direction
        speed_mps = random.uniform(MIN_FLY_SPEED_KMPH, MAX_FLY_SPEED_KMPH) * 1000.0 / 60.0 / 60.0
        self.speed_pps = speed_mps * PIXEL_PER_METER
        # 1초당 프레임 수 = 1초당 날갯짓 수 x 14
        self.frames_per_second = speed_mps / FLAP_DISTANCE_M * FRAMES_PER_FLAP

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + self.frames_per_second * dt) % FRAMES_PER_FLAP
        self.x += self.dir * self.speed_pps * dt

        # 몸 중심이 화면 끝에서 몸길이 절반만큼 안쪽에 닿으면 방향 전환
        half = BIRD_LENGTH_M * PIXEL_PER_METER / 2
        if self.x > get_canvas_width() - half:
            self.x, self.dir = get_canvas_width() - half, -1
        elif self.x < half:
            self.x, self.dir = half, 1

    def draw(self):
        left, bottom, width, height, dx, dy = FRAMES[int(self.frame)]
        if self.dir == 1:
            self.image.clip_draw(left, bottom, width, height,
                                 self.x + dx * BIRD_SCALE, self.y + dy * BIRD_SCALE,
                                 width * BIRD_SCALE, height * BIRD_SCALE)
        else:
            # 원본은 오른쪽을 보므로 좌우 반전하고 dx 부호도 바꾼다 (몸 중심 기준 반전)
            self.image.clip_composite_draw(left, bottom, width, height, 0, 'h',
                                           self.x - dx * BIRD_SCALE, self.y + dy * BIRD_SCALE,
                                           width * BIRD_SCALE, height * BIRD_SCALE)
