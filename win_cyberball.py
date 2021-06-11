#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel

from psychopy import visual, core, event, gui, data, misc
import numpy
import pandas as pd
import tkinter
from tkinter import *
import win32gui
import win32api
import win32con
import winsound

import glob, os, random, time, csv, functools, logging, math
import os.path as path

import texts

LGFMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename="cyberball.log", level=logging.DEBUG, format=LGFMT)

# http://sapir.psych.wisc.edu/wiki/index.php/Psychopyのスクリプト
def getKeyboardResponse(validResponses):
    event.clearEvents()  # important - prevents buffer overruns
    responseTimer = core.Clock()
    responded = event.waitKeys(keyList=validResponses)
    rt = responseTimer.getTime()
    return [
        responded[0],
        rt,
    ]  # only get the first response. no timer for waitKeys, so do it manually w/ a clock


def request_experiment_session_info():
    expInfo = {"Participant": "001"}
    expInfo["date"] = data.getDateStr()

    dlg = gui.DlgFromDict(expInfo, title="Experiment", fixed=["date"])
    if dlg.OK:
        return expInfo
    else:
        core.quit()


expInfo = request_experiment_session_info()

# 画面設定をして、それをmyWinに入れる(myWinと打つだけで設定もはいる）
screen_width, screen_height = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
myWin = visual.Window(
    fullscr=False,
    units="norm",
    size=(screen_width, screen_height),
    name="experiment",
    color=(0.5, 0.5, 0.5),
)
myWin.setMouseVisible(False)
w, h = myWin.size[0], myWin.size[1]  # Size of window

v_split = 0.7
act_pos = (0.0, v_split - 1)  # Center of activity area
act_size = [2.0, 1.4]

uprof_pos_y = 1 - 0.43 * v_split  # Center of user profile section
face_img_size_px = (154, 219)
img_aspect_ratio = face_img_size_px[0] / face_img_size_px[1]
window_aspect_ratio = w / h
face_img_size_norm = numpy.array([0.6 * img_aspect_ratio / window_aspect_ratio, 0.6])

anim_frame_duration = 0.2  # Frame duration of animation


def set_min_style():
    """
    Use win32gui to set PsychoPy window as borderless, and maximized.
    https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowlongptra
    https://docs.microsoft.com/en-us/windows/win32/winmsg/window-styles
    """
    windowHandle = win32gui.FindWindowEx(None, None, None, "PsychoPy")
    GWL_STYLE = -16
    SW_SHOWMAXIMIZED = 3
    style = 0x0
    win32gui.SetWindowLong(windowHandle, GWL_STYLE, style)
    win32gui.ShowWindow(windowHandle, SW_SHOWMAXIMIZED)


set_min_style()
myWin.flip(False)


def make_actimagestim(path):
    return visual.ImageStim(myWin, image=path, pos=act_pos, size=act_size)


def make_faceimagestim(path):
    return visual.ImageStim(myWin, image=path, units="norm")


def set_face_pair(imstim1, imstim2):
    imstim1.pos, imstim2.pos = (-0.5, uprof_pos_y), (0.5, uprof_pos_y)
    imstim1.size, imstim2.size = face_img_size_norm, face_img_size_norm


# 提示刺激を準備
wait = make_actimagestim("./stim/start.bmp")
LS_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/1toY*"))]
LR_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/1to2*"))]
RS_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/2toY*"))]
RL_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/2to1*"))]
SL_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/Yto1*"))]
SR_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/Yto2*"))]
conw = visual.ImageStim(
    myWin, image="./stim/connectingwindow.bmp", mask=None, pos=(0, 0), size=[0.4, 0.25]
)

# Face images paths
face_dir_root = "./stim/face/"
face_p = {
    "neg": sorted(glob.glob(path.join(face_dir_root, "negafile", "*.jpg"))),
    "neu": sorted(glob.glob(path.join(face_dir_root, "neufile", "*.jpg"))),
    "pos": sorted(glob.glob(path.join(face_dir_root, "posifile", "*.jpg"))),
}
num_faces = len(face_p["neg"])
# Load face images
face = {x: [make_faceimagestim(y_p) for y_p in y] for x, y in face_p.items()}

logging.debug(face_p)


def draw(*imgstims):
    for imgstim in imgstims:
        imgstim.draw()


def frame(imgstims, duration=0.2):
    draw(*imgstims)
    myWin.flip()
    core.wait(duration)


def animation(img_stims, l_face, r_face, frame_duration, randomize_first_frame=True):
    start = 0
    if randomize_first_frame:
        frame([l_face, r_face, img_stims[0]], duration=random.uniform(0.5, 1.5))
        start = 1
    for img in img_stims[start:]:
        frame([l_face, r_face, img], duration=frame_duration)


# Lは参加者から見て左、Sは参加者、Rは参加者から見て右。LSは、左の人から参加者にボールが投げられるアクションを指す
def LS(l_face, r_face):
    animation(
        LS_image_stim, l_face, r_face, anim_frame_duration, randomize_first_frame=True
    )


def LR(l_face, r_face):
    animation(
        LR_image_stim, l_face, r_face, anim_frame_duration, randomize_first_frame=True
    )


def RS(l_face, r_face):
    animation(
        RS_image_stim, l_face, r_face, anim_frame_duration, randomize_first_frame=True
    )


def RL(l_face, r_face):
    animation(
        RL_image_stim, l_face, r_face, anim_frame_duration, randomize_first_frame=True
    )


def SL(l_face, r_face):
    animation(
        SL_image_stim, l_face, r_face, anim_frame_duration, randomize_first_frame=False
    )


def SR(l_face, r_face):
    animation(
        SR_image_stim, l_face, r_face, anim_frame_duration, randomize_first_frame=False
    )


def show_connection(time):
    per_frame_time = 1  # s
    time = math.ceil(time)
    conw_frames = [conw for _ in range(time)]
    for c in conw_frames:
        frame([c], per_frame_time)


def make_qlabel(dlg, txt, font):
    qlabel = QLabel(dlg)
    qlabel.setText(txt)
    qlabel.setFont(font)
    return qlabel


def message(title, labels, geometry, main_window, button_name="Next"):
    main_window.setMouseVisible(True)

    dlg = QDialog()
    dlg.setWindowTitle(title)
    button = QPushButton(button_name, dlg)
    font = QFont("Meiryo UI", 20)
    qlabel = make_qlabel(dlg, labels, font)
    layout = QVBoxLayout()
    layout.addWidget(qlabel)
    layout.addWidget(button)
    dlg.setLayout(layout)
    button.clicked.connect(lambda: dlg.accept())

    dlg.raise_()
    dlg.exec()
    main_window.setMouseVisible(False)


def instruction1(mywin):
    title = "Catchball(3people) -Instruction 1/3"
    geometry = "600x180+20+20"  # 幅×高さ＋x＋y
    labels = texts.inst1_txt
    message(title, labels, geometry, mywin)


def instruction2(mywin):
    title = "Catchball(3people) -Instruction 2/3"
    geometry = "600x180+20+20"
    labels = texts.inst2_txt
    message(title, labels, geometry, mywin)


def instruction3(mywin):
    title = "Catchball(3people) -Instruction 3/3"
    geometry = "600x180+20+20"
    labels = texts.inst3_txt
    message(title, labels, geometry, mywin, button_name="Start")


def connecting(mywin):
    show_connection(time=8)
    mywin.setMouseVisible(True)
    title = "Catchball - 3people"
    geometry = "600x180+20+20"
    labels = texts.conn_txt

    message(title, labels, geometry, mywin)


def ready_for_test(mywin):
    mywin.setMouseVisible(True)
    mywin.flip()
    title = "Catchball - 3people"
    geometry = "600x180+20+20"
    labels = texts.start_txt

    message(title, labels, geometry, mywin, button_name="Ok")


def between(mywin):
    mywin.setMouseVisible(True)
    mywin.flip()
    title = "Catchball - 3people"
    geometry = "600x220+20+20"
    labels = texts.between_txt

    message(title, labels, geometry, mywin, button_name="Start")

    q = random.uniform(4.5, 60)
    show_connection(time=q)
    mywin.setMouseVisible(False)


def end(mywin):
    mywin.setMouseVisible(True)
    mywin.flip()
    title = "Catchball - 3people"
    geometry = "600x170+20+20"
    labels = texts.end_txt

    message(title, labels, geometry, mywin, button_name="Ok")


def prob_model(rnd_left, Spass_left, a):
    """
    Probablistic model for passing to user
    Controled by parameter a, in range (0, 1.0)
    - a = 0.5, same probability passing to user across the session
    - a < 0.5, higher probability passing to user towards the end of the session
    - a > 0.5, higher probability passing to user towards the start of the session.
    """
    logging.debug([rnd_left, Spass_left])
    not_Spass_left = rnd_left - Spass_left
    if Spass_left * 2 >= rnd_left:
        return True
    else:
        x = Spass_left * a
        y = not_Spass_left / 2 * (1 - a)
        x, y = x / (x + y), y / (x + y)
        r = random.uniform(0, 1.0)
        return r < x


def generate_user_profile_pictures(playerids, emotions):
    logging.debug(f"Loading players {playerids}, emotions {emotions}")
    l_emo, r_emo = emotions
    lid, rid = playerids
    l_face, r_face = face[l_emo][lid], face[r_emo][rid]
    return l_face, r_face


#####################################################################################
# Session template


def session(
    total_passes,
    num_Spass_totl,
    players,
    a=0.5,
    session_label=None,
    expInfo={"sessions": {}},
):
    """
    Main loop for a session

    Parameter
    ---------
    total_passes: int
    Controls the total number of passes in this session

    num_Spass_totl: int
    Number to pass to user. Must be less than half of `total_passes`.

    players: 2-tuple object
    A tuple of images for left and right user profile picture.

    a: float [0, 1.0]
    Controls the distribution of probability passing to user, see
    `prob_model` for usage

    Return
    ------
    None
    """
    if not 0 <= a and a <= 1.0:
        raise ValueError("Invalid x`value a.")

    if num_Spass_totl * 2 > total_passes:
        raise ValueError(
            "Cannot pass to user more than half of total number of passes."
        )

    logging.debug(f"Current session: {session_label}")
    expInfo["sessions"][session_label] = {"positions": [], "reaction_times": []}

    winsound.Beep(523, 5000)

    l_face, r_face = players
    set_face_pair(l_face, r_face)

    cur_pos = random.randint(0, 2)
    num_Spass = 0

    if cur_pos == 0:
        frame([l_face, r_face, SL_image_stim[0]])
    for rnd in range(total_passes):
        expInfo["sessions"][session_label]["positions"].append(cur_pos)
        if cur_pos == 0:
            selectKey, reaction_time = getKeyboardResponse(["left", "right", "q"])
            expInfo["sessions"][session_label]["reaction_times"].append(reaction_time)
            if "left" in selectKey:
                SL(l_face, r_face)
                cur_pos = 1
            elif "right" in selectKey:
                SR(l_face, r_face)
                cur_pos = 2
            elif "q" in selectKey:
                core.quit()
        else:
            rnd_left = total_passes - rnd
            Spass_left = num_Spass_totl - num_Spass
            Spass = prob_model(rnd_left, Spass_left, a)

            if Spass:
                if cur_pos == 1:
                    LS(l_face, r_face)
                else:
                    RS(l_face, r_face)
                cur_pos = 0
                num_Spass += 1
            else:
                if cur_pos == 1:
                    LR(l_face, r_face)
                    cur_pos = 2
                else:
                    RL(l_face, r_face)
                    cur_pos = 1
    m = int(total_passes / 3)
    winsound.Beep(523, 500)


#####################################################################################
# Practice session


def practice(playerids):
    instruction1(myWin)
    instruction2(myWin)
    instruction3(myWin)
    connecting(myWin)

    player_profiles = generate_user_profile_pictures(playerids, ("neu", "neu"))
    session(20, 5, player_profiles, 0.5, "Practice")


#####################################################################################
# 6 sessions


def make_sessions(playerids, expInfo):
    """
    Session factory

    Creates 6 sessions according to presets. expInfo is a dict
    that holds the logs of the experiment.

    Returns a list of session lambdas, len=6
    """
    user_profiles = [
        generate_user_profile_pictures(playerids, x)
        for x in [
            ("pos", "neg"),
            ("pos", "pos"),
            ("neg", "neg"),
            ("pos", "pos"),
            ("neg", "neg"),
            ("pos", "neg"),
        ]
    ]

    total_passes = 30

    # Acceptance: on the higher end of the upper half
    # 0 |-----------|----{-------}| 15 (max possible Spasses)
    # acceptance_Spass_func = lambda: random.randint(11, 15)
    acceptance_Spass_func = lambda: 10
    # Rejection: on the lower end of the lower half
    # 0 |--{----}-----|-----------| 15 (max possible Spasses)
    # rejection_Spass_func = lambda: random.randint(2, 6)
    rejection_Spass_func = lambda: 5

    acceptance_param_a = 0.5
    rejection_param_a = 0.92

    session_args = [
        [
            total_passes,
            acceptance_Spass_func(),
            user_profiles[0],
            acceptance_param_a,
            "PNacc",
        ],
        [
            total_passes,
            rejection_Spass_func(),
            user_profiles[1],
            rejection_param_a,
            "PPrej",
        ],
        [
            total_passes,
            acceptance_Spass_func(),
            user_profiles[2],
            acceptance_param_a,
            "NNacc",
        ],
        [
            total_passes,
            acceptance_Spass_func(),
            user_profiles[3],
            acceptance_param_a,
            "PPacc",
        ],
        [
            total_passes,
            rejection_Spass_func(),
            user_profiles[4],
            rejection_param_a,
            "NNrej",
        ],
        [
            total_passes,
            rejection_Spass_func(),
            user_profiles[5],
            rejection_param_a,
            "PNrej",
        ],
    ]

    expInfo["sessions"] = {}
    sessions = [
        functools.partial(session, *(args + [expInfo])) for args in session_args
    ]

    # Fix front and back. Shuffle middle ones
    mid_sessions = sessions[1:-1]
    random.shuffle(mid_sessions)
    sessions_reordered = [sessions[0]] + mid_sessions + [sessions[-1]]

    return sessions_reordered


def get_player_id():
    all_players = [x for x in range(0, 5)]
    random.shuffle(all_players)
    playerids = all_players[0:2]
    logging.debug(f"Selected user ids: {playerids}")
    return playerids


def dump_exp_info(expInfo):
    positions = {s: expInfo["sessions"][s]["positions"] for s in expInfo["sessions"]}
    reaction_times = {
        s: expInfo["sessions"][s]["reaction_times"] for s in expInfo["sessions"]
    }

    # Align column lengths
    max_pos_len = max([len(positions[s]) for s in positions])
    max_rt_len = max([len(reaction_times[s]) for s in reaction_times])
    positions = {
        s: pos + [None] * (max_pos_len - len(pos)) for s, pos in positions.items()
    }
    reaction_times = {
        s: rt + [None] * (max_rt_len - len(rt)) for s, rt in reaction_times.items()
    }

    pos_df = pd.DataFrame(positions)
    rt_df = pd.DataFrame(reaction_times)

    filename = expInfo["Participant"] + "_" + expInfo["date"] + ".xlsx"
    with pd.ExcelWriter(filename) as writer:
        pos_df.to_excel(writer, sheet_name="positions")
        rt_df.to_excel(writer, sheet_name="reaction_times")


if __name__ == "__main__":
    playerids = get_player_id()
    practice(playerids)
    ready_for_test(myWin)

    sessions = make_sessions(playerids, expInfo)
    for i, session in enumerate(sessions):
        if i < 5:
            session()
            between(myWin)
        else:
            session()
            end(myWin)

    dump_exp_info(expInfo)
