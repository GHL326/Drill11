from pico2d import load_image
from transitions import Machine


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(model=self, states=['IDLE'], initial='IDLE', auto_transitions=False)

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        row = 300 if self.face_dir == 1 else 200
        self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
