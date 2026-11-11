from pico2d import load_image


class Bird:
    image = None

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(34, 362, 146, 143, self.x, self.y)
