# from psychopy import visual

from movie4 import MovieStim4


def makeVideo(path, win, pos, size):
    return MovieStim4(
        win,
        path,
        size=size,
        pos=pos,
        units="norm",
        flipVert=False,
        flipHoriz=False,
        loop=False,
        noAudio=True,
    )
