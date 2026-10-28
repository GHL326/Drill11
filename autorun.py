from pico2d import get_canvas_width


class AutoRun:
    SCALE = 2

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        boy = self.boy
        boy.draw_size = 100 * self.SCALE
        half_width = boy.draw_size / 2
        width = get_canvas_width()
        boy.x = max(half_width, min(width - half_width, boy.x))
        boy.face_dir = -1 if boy.x <= width / 2 else 1

    def update(self):
        boy = self.boy
        half_width = boy.draw_size / 2
        right_wall = get_canvas_width() - half_width
        boy.x += boy.face_dir * boy.RUN_SPEED
        if boy.x <= half_width:
            boy.x = half_width
            boy.face_dir = 1
        elif boy.x >= right_wall:
            boy.x = right_wall
            boy.face_dir = -1
        boy.frame = (boy.frame + 1) % 8

    def exit(self):
        self.boy.draw_size = 100
