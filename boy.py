from math import pi
from time import monotonic

from pico2d import (
    SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_SPACE, SDLK_a,
    get_canvas_width, load_image,
)
from transitions import Machine

from autorun import AutoRun

class Boy:
    IDLE_TIMEOUT = 5.0
    RUN_SPEED = 5
    HALF_WIDTH = 50

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.pressed_directions = []
        self.draw_size = 100
        self.autorun = AutoRun(self)
        self.image = load_image('animation_sheet.png')

        self.machine = Machine(
            model=self,
            states=[
                {'name': 'IDLE', 'on_enter': 'enter_idle'},
                {'name': 'SLEEP', 'on_enter': 'enter_sleep'},
                {'name': 'RUN', 'on_enter': 'enter_run'},
                {'name': 'AUTORUN', 'on_enter': 'enter_autorun', 'on_exit': 'exit_autorun'},
            ],
            transitions=[
                {'trigger': 'fall_asleep', 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake_up', 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'start_running', 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
                {'trigger': 'stop_running', 'source': 'RUN', 'dest': 'IDLE'},
                {'trigger': 'start_autorun', 'source': ['IDLE', 'SLEEP', 'RUN'], 'dest': 'AUTORUN'},
                {'trigger': 'finish_autorun', 'source': 'AUTORUN', 'dest': 'IDLE'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )
        # Machine does not call on_enter for its initial state.
        self.enter_idle()

    def enter_idle(self):
        self.idle_started_at = monotonic()
        self.frame = 0
        self.pressed_directions.clear()

    def enter_sleep(self):
        self.frame = 0

    def enter_run(self):
        self.frame = 0

    def enter_autorun(self):
        self.frame = 0
        self.pressed_directions.clear()
        self.autorun.enter()

    def exit_autorun(self):
        self.autorun.exit()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            if self.state in ('IDLE', 'SLEEP', 'RUN'):
                self.start_autorun()
            return
        if self.state == 'AUTORUN':
            return

        if self.state == 'SLEEP' and event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            self.wake_up()
            return

        if event.type not in (SDL_KEYDOWN, SDL_KEYUP):
            return
        if event.key not in (SDLK_LEFT, SDLK_RIGHT):
            return

        if event.type == SDL_KEYDOWN:
            # Ignore key repeat; the most recently pressed direction takes priority.
            if event.key not in self.pressed_directions:
                self.pressed_directions.append(event.key)
            if self.state in ('IDLE', 'SLEEP'):
                self.start_running()
        elif event.key in self.pressed_directions:
            self.pressed_directions.remove(event.key)

        if self.pressed_directions:
            self.face_dir = 1 if self.pressed_directions[-1] == SDLK_RIGHT else -1
        elif self.state == 'RUN':
            self.stop_running()

    def update(self):
        if self.state == 'IDLE':
            if monotonic() - self.idle_started_at >= self.IDLE_TIMEOUT:
                self.fall_asleep()
            else:
                self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.x += self.face_dir * self.RUN_SPEED
            self.x = max(self.HALF_WIDTH, min(get_canvas_width() - self.HALF_WIDTH, self.x))
            self.frame = (self.frame + 1) % 8
        elif self.state == 'AUTORUN':
            if self.autorun.update():
                self.finish_autorun()

    def draw(self):
        if self.state == 'SLEEP':
            row = 300 if self.face_dir == 1 else 200
            self.image.clip_composite_draw(
                0, row, 100, 100, -pi / 2, '', self.x, self.y - 25, 100, 100
            )
            return
        if self.state in ('RUN', 'AUTORUN'):
            row = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(
                self.frame * 100, row, 100, 100,
                self.x, self.y + (self.draw_size - 100) / 2,
                self.draw_size, self.draw_size,
            )
            return
        if self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
