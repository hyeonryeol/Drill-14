from pico2d import load_image

import game_framework

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

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0.0

    def update(self):
        dt = game_framework.frame_time
        self.frame = (self.frame + FLAP_FRAMES_PER_SECOND * dt) % FRAMES_PER_FLAP

    def draw(self):
        left, bottom, width, height, dx, dy = FRAMES[int(self.frame)]
        self.image.clip_draw(left, bottom, width, height, self.x + dx, self.y + dy)
