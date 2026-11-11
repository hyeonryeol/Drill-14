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

# 날갯짓: 1초에 3번, 즉 1초에 14 x 3 = 42프레임
FLAPS_PER_SECOND = 3.0
FLAP_FRAMES_PER_SECOND = FRAMES_PER_FLAP * FLAPS_PER_SECOND


class Bird:
    image = None

    def __init__(self, x, y, direction):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = random.uniform(0, FRAMES_PER_FLAP)  # 날갯짓 시작 위상
        self.dir = direction

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FLAP_FRAMES_PER_SECOND * dt) % FRAMES_PER_FLAP
        self.x += self.dir * FLY_SPEED_PPS * dt

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
