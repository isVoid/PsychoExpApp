import glob
from typing import List
from psychopy import visual

from constants import FPS


def make_actimagestim(path, myWin, pos, size):
    return visual.ImageStim(myWin, image=path, pos=pos, size=size)


class Animation:
    frames: List[object]
    frame_duration: float

    indices_per_frame: int
    cur_idx: int

    def __init__(self, frames, duration):
        """Each animation is specified with a frame list
        and frame duration.
        """
        if len(frames) == 0:
            raise ValueError("Cannot have 0-length frames.")

        self.frames = frames
        self.frame_duration = duration
        self.indices_per_frame = self.frame_duration * FPS
        self.cur_idx = 0

    def draw_first_frame(self):
        self.frames[0].draw()

    def draw(self):
        play_idx = int(self.cur_idx // self.indices_per_frame)
        if play_idx >= len(self.frames):
            play_idx = -1
        self.frames[play_idx].draw()
        self.cur_idx += 1

    def finished(self) -> bool:
        return self.cur_idx >= self.indices_per_frame * len(self.frames)

    def reset(self):
        self.cur_idx = 0
