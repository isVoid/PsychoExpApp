from psychopy import visual


def makeVideo(path, win, pos, size):
    return visual.MovieStim3(
        win,
        path,
        size=size,
        pos=pos,
        units="norm",
        flipVert=False,
        flipHoriz=False,
        loop=True,
        noAudio=True,
    )
