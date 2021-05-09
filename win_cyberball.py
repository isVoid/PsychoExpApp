#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import visual, core, event, gui, data, misc
import numpy
import tkinter
from tkinter import *
import win32gui
import win32con
import winsound

import glob, os, random, time, csv
import os.path as path

# 参加者IDの入力を求め，それをファイル名に使う
def user_id_input():
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


# 画面設定をして、それをmyWinに入れる(myWinと打つだけで設定もはいる）
myWin = visual.Window(fullscr=False, monitor="Default", units="norm", color=(0, 0, 0))
myWin.setMouseVisible(False)
w, h = myWin.size[0], myWin.size[1]  # Size of window

v_split = 0.7
act_pos = (0.0, v_split - 1)  # Center of activity area
act_size = [2.0, 1.4]

uprof_pos_y = 1 - 0.43 * v_split  # Center of user profile section
original_size = None
uprof_size_f = numpy.array([0.8, 0.8])

anim_frame_duration = 0.2  # Frame duration of animation


def make_actimagestim(path):
    return visual.ImageStim(myWin, image=path, pos=act_pos, size=act_size)


def make_faceimagestim(path):
    return visual.ImageStim(myWin, image=path)


def set_face_pair(imstim1, imstim2):
    global original_size
    imstim1.pos, imstim2.pos = (-0.5, uprof_pos_y), (0.5, uprof_pos_y)
    if original_size is None:
        original_size = imstim1.size
    imstim1.size, imstim2.size = (
        original_size * uprof_size_f,
        original_size * uprof_size_f,
    )


# 提示刺激を準備
wait = make_actimagestim("./stim/start.bmp")
LS_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/1toY*"))]
LR_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/1to2*"))]
RS_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/2toY*"))]
RL_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/2to1*"))]
SL_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/Yto1*"))]
SR_image_stim = [make_actimagestim(x) for x in sorted(glob.glob("./stim/Yto2*"))]
conw = visual.ImageStim(
    myWin, image=u"./stim/connectingwindow.bmp", mask=None, pos=(0, 0), size=[0.4, 0.25]
)

# Face images paths
face_dir_root = "./stim/face/"
face_p = {
    "neg": sorted(glob.glob(path.join(face_dir_root, "negafile", "*.jpg"))),
    "neu": sorted(glob.glob(path.join(face_dir_root, "neufile", "*.jpg"))),
    "pos": sorted(glob.glob(path.join(face_dir_root, "posifile", "*.jpg"))),
}

# Load face images
face = {x: [make_faceimagestim(y_p) for y_p in y] for x, y in face_p.items()}


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
        inst1, text=u"Catchballは、オンラインでキャッチボールを行うプログラムです。\n", font=("Meiryo UI", 12)
    ).pack()
    Label(
        inst1,
        text=u"今回はあなたの他にあと　2　名の参加者の方がおり、　3　名でプレイしていただきます。",
        font=("Meiryo UI", 12),
    ).pack()
    Label(
        inst1,
        text=u"ボールが回ってきたら、左上のプレイヤーに投げる時は左ボタンを、\n右上のプレイヤーに投げる時は右ボタンを押してください。",
        font=("Meiryo UI", 12),
    ).pack()
    Label(
        inst1, text=u"1ブロックあたり30～60球で、全部で5ブロック行なっていただきます。", font=("Meiryo UI", 12)
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
        text=u"注意点があります。\n\n①ボールの動きが確実に止まってからボタンを押してください。\n②ボールを受け取ったらすぐに投げてください。\n\n",
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
        text=u"準備ができたらStartボタンを押してください。他プレイヤーとの接続を開始します。\n全プレイヤーの準備ができたらブロックを開始しますので、キーボードに指を置いてお待ちください。\n電極を装着した箇所は動かさないようにしてください。",
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
        text=u"他のプレイヤーが練習モードでプレイしています。\nブロック終了までしばらくお待ちください。\n\n電極を装着した箇所は動かさないようにしてください。",
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
        between, text=u"\nブロックが終了しました。\nアンケートへの記入をお願いします。\n", font=("Meiryo UI", 12)
    ).pack()
    Label(
        between,
        text=u"回答が済んだらStartボタンを押してください。他プレイヤーとの接続を開始します。\n全プレイヤーの準備ができたら次ブロックを開始しますので、キーボードに指を置いてお待ちください。\n電極を装着した箇所は動かさないようにしてください。\nお互いに、他の2人がどんな人か想像しながら取り組んでください。",
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

    q = random.uniform(4.5, 100)
    conw.draw()
    myWin.flip()
    core.wait(q)
    myWin.setMouseVisible(False)


def exit():
    myWin.setMouseVisible(True)
    myWin.flip()
    exit = Tk()
    exit.title("Catchball - 3people")
    exit.geometry("600x170+20+20")
    Label(exit, text=u"\n5ブロックが終了しました。\n", font=("Meiryo UI", 12)).pack()
    Label(exit, text=u"アンケートへの記入をお願いします。\n", font=("Meiryo UI", 12)).pack()
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


# The id corresponding to the left and right user profile, cannot be the same
left_person_id = random.randint(0, len(face["pos"]) - 1)
right_person_id = random.choice(
    [x for x in range(len(face["pos"])) if x != left_person_id]
)


def prob_model(rnd_left, Spass_left, a):
    """
    Probablistic model for passing to user
    Controled by parameter a, in range (0, 1.0)
    a = 0.5, same probability passing to user across
    the session; a < 0.5, higher probability passing to user
    towards the end of the session; a > 0.5, higher probability
    passing to user towards the start of the session.
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


#####################################################################################
# Practice session


def practice():
    instruction1()
    instruction2()
    instruction3()
    connecting()

    winsound.Beep(523, 5000)
    l_face, r_face = face["neu"][left_person_id], face["neu"][right_person_id]
    set_face_pair(l_face, r_face)
    for h in range(22):
        LR(l_face, r_face)
        RL(l_face, r_face)
    winsound.Beep(523, 500)
    between()


#####################################################################################
# Session template


def session(total_passes, a=0.5):
    """
    Main loop for a session

    Parameter
    ---------
    total_passes: int
    Controls the total number of passes in this session

    a: float [0, 1.0]
    Controls the distribution of probability passing to user, see
    `prob_model` for usage

    Return
    ------
    None
    """
    if not 0 <= a and a <= 1.0:
        raise ValueError("Invalid value a.")

    winsound.Beep(523, 5000)

    emotions = list(face.keys())
    l_emo, r_emo = random.choice(emotions), random.choice(emotions)
    l_face, r_face = face[l_emo][left_person_id], face[r_emo][right_person_id]
    set_face_pair(l_face, r_face)

    cur_pos = random.randint(0, 2)
    num_Spass = 0
    num_Spass_totl = round(total_passes / 3)
    if cur_pos == 0:
        frame([l_face, r_face, LS_image_stim[0]])
    for rnd in range(total_passes):
        if cur_pos == 0:
            (selectKey, react_time) = getKeyboardResponse(["left", "right"])
            if "left" in selectKey:
                SL(l_face, r_face)
                cur_pos = 1
            elif "right" in selectKey:
                SR(l_face, r_face)
                cur_pos = 2
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


if __name__ == "__main__":
    user_id_input()
    practice()
    session(60, 0.5)
    between()
    session(60, 0.3)
    between()
    session(60, 0.7)
