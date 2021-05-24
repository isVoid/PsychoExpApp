#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui, data, misc
import numpy
import tkinter
from tkinter import *
import win32gui
import win32con
import winsound

import glob, os, random, time, csv, functools, logging
import os.path as path

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


# 参加者IDの入力を求め，それをファイル名に使う
try:
    expInfo = misc.fromFile("lastParams.pickle")
except:
    expInfo = {"Participant": "001"}

expInfo["dateStr"] = data.getDateStr()

dlg = gui.DlgFromDict(expInfo, title="Experiment", fixed=["dateStr"])
if dlg.OK:
    misc.toFile("lastParams.pickle", expInfo)
else:
    core.quit()

# 画面設定をして、それをmyWinに入れる(myWinと打つだけで設定もはいる）
myWin = visual.Window(fullscr=True, monitor="Default", units="norm")
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


def instruction1():
    myWin.setMouseVisible(True)
    inst1 = Tk()
    inst1.title("Catchball(3people) -Instruction 1/3")
    inst1.geometry("600x180+20+20")  # 幅×高さ＋x＋y
    Label(
        inst1, text="Catchballは、オンラインでキャッチボールを行うプログラムです。\n", font=("Meiryo UI", 12)
    ).pack()
    Label(
        inst1,
        text="今回はあなたの他にあと　2　名の参加者の方がおり、　3　名でプレイしていただきます。",
        font=("Meiryo UI", 12),
    ).pack()
    Label(
        inst1,
        text="ボールが回ってきたら、左上のプレイヤーに投げる時は左ボタンを、\n右上のプレイヤーに投げる時は右ボタンを押してください。",
        font=("Meiryo UI", 12),
    ).pack()
    Label(
        inst1, text="1ブロックあたり30～60球で、全部で5ブロック行なっていただきます。", font=("Meiryo UI", 12)
    ).pack()
    Button(inst1, text="Next", command=inst1.destroy).pack()

    def callback1():
        hwnd = int(inst1.wm_frame(), 0)
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    inst1.after(
        100, callback1
    )  # デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    inst1.mainloop()


def instruction2():
    inst2 = Tk()
    inst2.title("Catchball(3people) -Instruction 2/3")
    inst2.geometry("600x180+20+20")
    Label(
        inst2,
        text="注意点があります。\n\n①ボールの動きが確実に止まってからボタンを押してください。\n②ボールを受け取ったらすぐに投げてください。\n\n",
        font=("Meiryo UI", 12),
    ).pack()
    Button(inst2, text="Next", command=inst2.destroy).pack()

    def callback1():
        hwnd = int(inst2.wm_frame(), 0)
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    inst2.after(
        100, callback1
    )  # デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    inst2.mainloop()


def instruction3():
    inst3 = Tk()
    inst3.title("Catchball(3people) -Instruction 3/3")
    inst3.geometry("600x180+20+20")
    Label(
        inst3,
        text="準備ができたらStartボタンを押してください。他プレイヤーとの接続を開始します。\n全プレイヤーの準備ができたらブロックを開始しますので、キーボードに指を置いてお待ちください。\n電極を装着した箇所は動かさないようにしてください。",
        font=("Meiryo UI", 12),
    ).pack()
    Button(inst3, text="Start", command=inst3.destroy).pack()

    def callback1():
        hwnd = int(inst3.wm_frame(), 0)
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    inst3.after(
        100, callback1
    )  # デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    inst3.mainloop()


def connecting():
    conw.draw()
    myWin.flip()
    core.wait(8)
    myWin.setMouseVisible(True)
    connecting = Tk()
    connecting.title("Catchball - 3people")
    connecting.geometry("600x180+20+20")
    Label(
        connecting,
        text="他のプレイヤーが練習モードでプレイしています。\nブロック終了までしばらくお待ちください。\n\n電極を装着した箇所は動かさないようにしてください。",
        font=("Meiryo UI", 12),
    ).pack()
    Button(connecting, text=" OK ", command=connecting.destroy, anchor="w").pack()

    def callback1():
        hwnd = int(connecting.wm_frame(), 0)
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    connecting.after(
        100, callback1
    )  # デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    connecting.mainloop()
    myWin.setMouseVisible(False)


def between():
    myWin.setMouseVisible(True)
    myWin.flip()
    between = Tk()
    between.title("Catchball - 3people")
    between.geometry("600x220+20+20")
    Label(
        between, text="\nブロックが終了しました。\nアンケートへの記入をお願いします。\n", font=("Meiryo UI", 12)
    ).pack()
    Label(
        between,
        text="回答が済んだらStartボタンを押してください。他プレイヤーとの接続を開始します。\n全プレイヤーの準備ができたら次ブロックを開始しますので、キーボードに指を置いてお待ちください。\n電極を装着した箇所は動かさないようにしてください。\nお互いに、他の2人がどんな人か想像しながら取り組んでください。",
        font=("Meiryo UI", 12),
    ).pack()
    Button(between, text="Start", command=between.destroy, anchor="w").pack()
    Button(between, text=" Exit ", anchor="w").pack()

    def callback1():
        hwnd = int(between.wm_frame(), 0)
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    between.after(
        100, callback1
    )  # デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    between.mainloop()
    myWin.setMouseVisible(False)

    q = random.uniform(4.5, 60)
    conw.draw()
    myWin.flip()
    core.wait(q)
    myWin.setMouseVisible(False)


def end():
    myWin.setMouseVisible(True)
    myWin.flip()
    exit = Tk()
    exit.title("Catchball - 3people")
    exit.geometry("600x170+20+20")
    Label(exit, text="\n5ブロックが終了しました。\n", font=("Meiryo UI", 12)).pack()
    Label(exit, text="アンケートへの記入をお願いします。\n", font=("Meiryo UI", 12)).pack()
    Button(exit, text="Start", anchor="w").pack()
    Button(exit, text=" Exit ", command=exit.destroy, anchor="w").pack()

    def callback1():
        hwnd = int(exit.wm_frame(), 0)
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
        )

    exit.after(
        100, callback1
    )  # デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    exit.mainloop()
    myWin.setMouseVisible(False)


def prob_model(rnd_left, Spass_left, a):
    """
    Probablistic model for passing to user
    Controled by parameter a, in range (0, 1.0)
    - a = 0.5, same probability passing to user across the session
    - a < 0.5, higher probability passing to user towards the end of the session
    - a > 0.5, higher probability passing to user towards the start of the session.
    """
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


def session(total_passes, num_Spass_totl, players, a=0.5, session_label=None):
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

    winsound.Beep(523, 5000)

    l_face, r_face = players
    set_face_pair(l_face, r_face)

    cur_pos = random.randint(0, 2)
    num_Spass = 0
    num_Spass_totl = round(total_passes / 3)

    if cur_pos == 0:
        frame([l_face, r_face, SL_image_stim[0]])
    for rnd in range(total_passes):
        if cur_pos == 0:
            (selectKey, _) = getKeyboardResponse(["left", "right", "q"])
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
    instruction1()
    instruction2()
    instruction3()
    connecting()

    player_profiles = generate_user_profile_pictures(playerids, ("pos", "pos"))
    session(20, 5, player_profiles, 0.5, "Practice")


#####################################################################################
# 6 sessions


def make_sessions(playerids):
    """
    Session factory

    Creates 6 sessions according to presets.

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
    acceptance_Spass_func = lambda: random.randint(11, 15)
    # Rejection: on the lower end of the lower half
    # 0 |--{----}-----|-----------| 15 (max possible Spasses)
    rejection_Spass_func = lambda: random.randint(2, 6)

    acceptance_param_a = 0.5
    rejection_param_a = 0.8

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

    sessions = [functools.partial(session, *args) for args in session_args]

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


if __name__ == "__main__":
    playerids = get_player_id()
    practice(playerids)
    between()
    sessions = make_sessions(playerids)
    for session in sessions:
        session()
        between()
    end()
