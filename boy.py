from math import pi
from time import monotonic

from pico2d import load_image
from transitions import Machine


class Boy:
    IDLE_TIMEOUT = 5.0

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(model=self, states=[{'name': 'IDLE', 'on_enter': 'enter_idle'}, {'name': 'SLEEP', 'on_enter': 'enter_sleep'}], transitions=[{'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP'}], initial='IDLE', auto_transitions=False)

        # The initial state does not invoke on_enter automatically.
        self.enter_idle()

    def enter_idle(self):
        self.idle_started_at = monotonic()
        self.frame = 0

    def enter_sleep(self):
        self.frame = 0

    def update(self):
        if self.state == 'IDLE':
            if monotonic() - self.idle_started_at >= self.IDLE_TIMEOUT:
                self.fall_asleep()
            else:
                self.frame = (self.frame + 1) % 8

    def draw(self):
        row = 300 if self.face_dir == 1 else 200
        if self.state == 'SLEEP':
            self.image.clip_composite_draw(0, row, 100, 100, -pi / 2, '', self.x, self.y - 25, 100, 100)
        else:
            self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
