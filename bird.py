from pico2d import load_image

# bird_animation.png 프레임 데이터 (left, bottom, width, height)
# 5열 x 3행에 14프레임. 프레임마다 투명하지 않은 픽셀 범위만 잘라낸다.
FRAMES = (
    (34, 362, 146, 143),
    (216, 363, 146, 141),
    (398, 364, 146, 130),
    (555, 367, 171, 122),
    (728, 370, 182, 88),
    (34, 171, 146, 118),
    (216, 166, 146, 124),
    (398, 170, 146, 120),
    (580, 180, 146, 109),
    (762, 177, 146, 110),
    (34, 6, 146, 108),
    (216, 6, 146, 106),
    (376, 23, 168, 88),
    (546, 22, 180, 114),
)
FRAMES_PER_FLAP = len(FRAMES)


class Bird:
    image = None

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.frame = 0

    def update(self):
        self.frame = (self.frame + 1) % FRAMES_PER_FLAP

    def draw(self):
        left, bottom, width, height = FRAMES[self.frame]
        self.image.clip_draw(left, bottom, width, height, self.x, self.y)
