#!/usr/bin/env python
# -*- coding: utf-8 -*-

#各種モジュールのインポート
from psychopy import visual, core, event,gui,data,misc
import numpy, os , random,time,csv
import tkinter
from tkinter import *
import win32gui
import win32con
import winsound

import glob
import os.path as path

#参加者IDの入力を求め，それをファイル名に使う
try:
    expInfo = misc.fromFile('lastParams.pickle')
except:
    expInfo = {'Participant':'001'}

expInfo['dateStr']= data.getDateStr()

dlg = gui.DlgFromDict(expInfo, title='Experiment', fixed=['dateStr'])
if dlg.OK:
    misc.toFile('lastParams.pickle', expInfo)
else:
    core.quit()

#http://sapir.psych.wisc.edu/wiki/index.php/Psychopyのスクリプト
def getKeyboardResponse(validResponses,duration=0):
    event.clearEvents() #important - prevents buffer overruns
    responded = False
    timeElapsed = False
    rt = '*'
    responseTimer = core.Clock()
    if duration==0:
        responded = event.waitKeys(keyList=validResponses)
        rt = responseTimer.getTime()
        return [responded[0],rt] #only get the first response. no timer for waitKeys, so do it manually w/ a clock
    else:
        while responseTimer.getTime() < duration:
            if not responded:
                responded = event.getKeys(keyList=validResponses,timeStamped=responseTimer)
        if not responded:
            return ['*','*']
        else:
            return responded[0]  #only get the first response

#画面設定をして、それをmyWinに入れる(myWinと打つだけで設定もはいる）
myWin =visual.Window (fullscr=False, monitor= 'Default', units='norm', color= (0,0,0))
myWin.setMouseVisible(False)
w, h = myWin.size[0], myWin.size[1]      # Size of window

v_split = 0.7
uprof_pos = (0.0, (0.5 - (1 - v_split) / 2) * h)               # Center of user profile section
uprof_size = [w, (1 - v_split) * h]

act_pos =   (0.0, (v_split / 2 - 0.5) * h)              # Center of activity area
act_size = [w, v_split * h]

def make_actimagestim(path):
    return visual.ImageStim(myWin, image=path, units="pix", pos=act_pos, size=act_size) 

def make_faceimagestim(path, pos):
    return visual.ImageStim(myWin, image=path, units="pix", pos=pos, size=act_size) 

#提示刺激を準備
wait = make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/start.bmp')

LS1 = make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(1).bmp')
LS2 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(2).bmp')
LS3 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(3).bmp')
LS4 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(4).bmp')
LS5 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(5).bmp')
LS6 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(6).bmp')
LS7 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(7).bmp')
LS8 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1toY(8).bmp')

LR1 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(1).bmp')
LR2 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(2).bmp')
LR3 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(3).bmp')
LR4 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(4).bmp')
LR5 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(5).bmp')
LR6 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(6).bmp')
LR7 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(7).bmp')
LR8 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(8).bmp')
LR9 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/1to2(9).bmp')

RS1 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(1).bmp')
RS2 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(2).bmp')
RS3 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(3).bmp')
RS4 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(4).bmp')
RS5 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(5).bmp')
RS6 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(6).bmp')
RS7 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(7).bmp')
RS8 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2toY(8).bmp')

RL1 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(1).bmp')
RL2 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(2).bmp')
RL3 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(3).bmp')
RL4 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(4).bmp')
RL5 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(5).bmp')
RL6 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(6).bmp')
RL7 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(7).bmp')
RL8 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(8).bmp')
RL9 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/2to1(9).bmp')

SL1 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto1(1).bmp')
SL2 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto1(2).bmp')
SL3 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto1(3).bmp')
SL4 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto1(4).bmp')
SL5 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto1(5).bmp')
SL6 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto1(6).bmp')
SL7 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto1(7).bmp')

SR1 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto2(1).bmp')
SR2 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto2(2).bmp')
SR3 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto2(3).bmp')
SR4 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto2(4).bmp')
SR5 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto2(5).bmp')
SR6 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto2(6).bmp')
SR7 =  make_actimagestim('C:/Users/micha/Documents/cyberball/cyberball/stim/Yto2(7).bmp')

conw = visual.ImageStim(myWin, image=u'C:/Users/micha/Documents/cyberball/cyberball/stim/connectingwindow.bmp', mask = None, pos = (0,0), size = [0.4, 0.25])

face_dir_root = "./stim/face/"
neg_face = glob.glob(path.join(face_dir_root, "negafile", "*.jpg"))
neu_face = glob.glob(path.join(face_dir_root, "neufile", "*.jpg"))
pos_face = glob.glob(path.join(face_dir_root, "posifile", "*.jpg"))

#Lは参加者から見て左、Sは参加者、Rは参加者から見て右。LSは、左の人から参加者にボールが投げられるアクションを指す
def LS():
    r = random.uniform(0.5, 1.5)
    LS1.draw()
    myWin.flip()
    core.wait(r)
    LS2.draw()
    myWin.flip()
    core.wait(0.2)
    LS3.draw()
    myWin.flip()
    core.wait(0.2)
    LS4.draw()
    myWin.flip()
    core.wait(0.2)
    LS5.draw()
    myWin.flip()
    core.wait(0.2)
    LS6.draw()
    myWin.flip()
    core.wait(0.2)
    LS7.draw()
    myWin.flip()
    core.wait(0.2)
    LS8.draw()
    myWin.flip()
    core.wait(0.2)

def LR():
    r = random.uniform(0.5, 1.5)
    LR1.draw()
    myWin.flip()
    core.wait(r)
    LR2.draw()
    myWin.flip()
    core.wait(0.2)
    LR3.draw()
    myWin.flip()
    core.wait(0.2)
    LR4.draw()
    myWin.flip()
    core.wait(0.2)
    LR5.draw()
    myWin.flip()
    core.wait(0.2)
    LR6.draw()
    myWin.flip()
    core.wait(0.2)
    LR7.draw()
    myWin.flip()
    core.wait(0.2)
    LR8.draw()
    myWin.flip()
    core.wait(0.2)
    LR9.draw()
    myWin.flip()
    core.wait(0.2)

def RS():
    r = random.uniform(0.5, 1.5)
    RS1.draw()
    myWin.flip()
    core.wait(r)
    RS2.draw()
    myWin.flip()
    core.wait(0.2)
    RS3.draw()
    myWin.flip()
    core.wait(0.2)
    RS4.draw()
    myWin.flip()
    core.wait(0.2)
    RS5.draw()
    myWin.flip()
    core.wait(0.2)
    RS6.draw()
    myWin.flip()
    core.wait(0.2)
    RS7.draw()
    myWin.flip()
    core.wait(0.2)
    RS8.draw()
    myWin.flip()
    core.wait(0.2)

def RL():
    r = random.uniform(0.5, 1.5)
    RL1.draw()
    myWin.flip()
    core.wait(r)
    RL2.draw()
    myWin.flip()
    core.wait(0.2)
    RL3.draw()
    myWin.flip()
    core.wait(0.2)
    RL4.draw()
    myWin.flip()
    core.wait(0.2)
    RL5.draw()
    myWin.flip()
    core.wait(0.2)
    RL6.draw()
    myWin.flip()
    core.wait(0.2)
    RL7.draw()
    myWin.flip()
    core.wait(0.2)
    RL8.draw()
    myWin.flip()
    core.wait(0.2)
    RL9.draw()
    myWin.flip()
    core.wait(0.2)

def SL():
    SL1.draw()
    myWin.flip()
    core.wait(0.2)
    SL2.draw()
    myWin.flip()
    core.wait(0.2)
    SL3.draw()
    myWin.flip()
    core.wait(0.2)
    SL4.draw()
    myWin.flip()
    core.wait(0.2)
    SL5.draw()
    myWin.flip()
    core.wait(0.2)
    SL6.draw()
    myWin.flip()
    core.wait(0.2)
    SL7.draw()
    myWin.flip()
    core.wait(0.2)

def SR():
    SR1.draw()
    myWin.flip()
    core.wait(0.2)
    SR2.draw()
    myWin.flip()
    core.wait(0.2)
    SR3.draw()
    myWin.flip()
    core.wait(0.2)
    SR4.draw()
    myWin.flip()
    core.wait(0.2)
    SR5.draw()
    myWin.flip()
    core.wait(0.2)
    SR6.draw()
    myWin.flip()
    core.wait(0.2)
    SR7.draw()
    myWin.flip()
    core.wait(0.2)

def instruction1():
    myWin.setMouseVisible(True)
    inst1 = Tk()
    inst1.title('Catchball(3people) -Instruction 1/3')
    inst1.geometry('600x180+20+20') #幅×高さ＋x＋y
    Label(inst1, text = u'Catchballは、オンラインでキャッチボールを行うプログラムです。\n',font=('Meiryo UI', 12)).pack()
    Label(inst1, text = u'今回はあなたの他にあと　2　名の参加者の方がおり、　3　名でプレイしていただきます。',font=('Meiryo UI', 12)).pack()
    Label(inst1, text = u'ボールが回ってきたら、左上のプレイヤーに投げる時は左ボタンを、\n右上のプレイヤーに投げる時は右ボタンを押してください。',font=('Meiryo UI', 12)).pack()
    Label(inst1, text = u'1ブロックあたり30～60球で、全部で5ブロック行なっていただきます。',font=('Meiryo UI', 12)).pack()
    Button(inst1, text = 'Next', command = inst1.destroy).pack()
    def callback1():
        hwnd = int(inst1.wm_frame(),0)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    inst1.after(100, callback1) #デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    inst1.mainloop()

def instruction2():
    inst2 = Tk()
    inst2.title('Catchball(3people) -Instruction 2/3')
    inst2.geometry('600x180+20+20')
    Label(inst2, text = u'注意点があります。\n\n①ボールの動きが確実に止まってからボタンを押してください。\n②ボールを受け取ったらすぐに投げてください。\n\n',font=('Meiryo UI', 12)).pack()
    Button(inst2, text = 'Next', command = inst2.destroy).pack()
    def callback1():
        hwnd = int(inst2.wm_frame(),0)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    inst2.after(100, callback1) #デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    inst2.mainloop()

def instruction3():
    inst3 = Tk()
    inst3.title('Catchball(3people) -Instruction 3/3')
    inst3.geometry('600x180+20+20')
    Label(inst3, text = u'準備ができたらStartボタンを押してください。他プレイヤーとの接続を開始します。\n全プレイヤーの準備ができたらブロックを開始しますので、キーボードに指を置いてお待ちください。\n電極を装着した箇所は動かさないようにしてください。',font=('Meiryo UI', 12)).pack()
    Button(inst3, text = 'Start', command = inst3.destroy).pack()
    def callback1():
        hwnd = int(inst3.wm_frame(),0)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    inst3.after(100, callback1) #デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    inst3.mainloop()

def connecting():
    conw.draw()
    myWin.flip()
    core.wait(8)
    myWin.setMouseVisible(True)
    connecting = Tk()
    connecting.title('Catchball - 3people')
    connecting.geometry('600x180+20+20')
    Label(connecting, text = u'他のプレイヤーが練習モードでプレイしています。\nブロック終了までしばらくお待ちください。\n\n電極を装着した箇所は動かさないようにしてください。',font=('Meiryo UI', 12)).pack()
    Button(connecting, text = ' OK ', command = connecting.destroy, anchor = 'w').pack()
    def callback1():
        hwnd = int(connecting.wm_frame(),0)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    connecting.after(100, callback1) #デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    connecting.mainloop()
    myWin.setMouseVisible(False)

def between():
    myWin.setMouseVisible(True)
    myWin.flip()
    between = Tk()
    between.title('Catchball - 3people')
    between.geometry('600x220+20+20')
    Label(between, text = u'\nブロックが終了しました。\nアンケートへの記入をお願いします。\n',font=('Meiryo UI', 12)).pack()
    Label(between, text = u'回答が済んだらStartボタンを押してください。他プレイヤーとの接続を開始します。\n全プレイヤーの準備ができたら次ブロックを開始しますので、キーボードに指を置いてお待ちください。\n電極を装着した箇所は動かさないようにしてください。\nお互いに、他の2人がどんな人か想像しながら取り組んでください。',font=('Meiryo UI', 12)).pack()
    Button(between, text = 'Start', command = between.destroy, anchor = 'w').pack()
    Button(between, text = ' Exit ', anchor = 'w').pack()
    def callback1():
        hwnd = int(between.wm_frame(),0)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    between.after(100, callback1) #デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
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
    exit.title('Catchball - 3people')
    exit.geometry('600x170+20+20')
    Label(exit, text = u'\n5ブロックが終了しました。\n',font=('Meiryo UI', 12)).pack()
    Label(exit, text = u'アンケートへの記入をお願いします。\n',font=('Meiryo UI', 12)).pack()
    Button(exit, text = 'Start', anchor = 'w').pack()
    Button(exit, text = ' Exit ', command = exit.destroy, anchor = 'w').pack()
    def callback1():
        hwnd = int(exit.wm_frame(),0)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    exit.after(100, callback1) #デフォルトでは背面にウインドウが出てしまう。前面のコマンドはmainloopの後に呼び出さないと動作しないためタイマーで0.1sec後に前面固定
    exit.mainloop()
    myWin.setMouseVisible(False)

#lists
numlist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
Rlist = [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3]
Llist = [1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3]
exnumlist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
exRlist = [2,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1]
exLlist = [1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
deinnumlist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
deinRlist = [2,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1]
deinLlist = [1,2,1,2,1,1,1,2,1,1,1,2,1,1,1,1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1]

#clock
trialClock = core.Clock()
trialClock.reset()
t = 0

#結果をいれる場所を準備
results=[]

# Escで終了
if event.getKeys(keyList=["escape"]):
    sys.exit()

#Count
numtotal = 0
numsub = 0
numcom = 0
numR = 0
numL = 0
numexR = 0
numexL = 0
numdeinR = 0
numdeinL = 0
direction = 0
i = 0

#####################################################################################
# Practice session

#watch
# instruction1()
# instruction2()
# instruction3()
# connecting()

# winsound.Beep(523, 5000)
for h in range(22):
    LR()
    RL()
winsound.Beep(523, 500)
between()

if False:

    #####################################################################################
    # Inclusion session

    #inclusion
    winsound.Beep(523, 5000)
    numtotal = 0
    numsub = 0
    numcom = 0
    for h in numlist:
        numpy.random.shuffle(Rlist)
        numpy.random.shuffle(Llist)
        if h == 1:
            RS()
            numtotal = numtotal + 1
            numcom = numcom + 1
            i = 0
            direction = 'RS'
            Rtime = 0
            selectKey = 0
            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
        else:
            if numtotal < 45:
                trialClock.reset()
                t = trialClock.getTime()
                (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
                numtotal = numtotal + 1
                numsub = numsub + 1
                if 'right' in selectKey:
                    SR()
                    direction = 'SR'
                    results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    i = Rlist[numR]
                    if i == 1:
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 2:
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 3:
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numR = numR + 1
                elif 'left' in selectKey:
                    SL()
                    direction = 'SL'
                    results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    i = Llist[numL]
                    if i == 1:
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 2:
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 3:
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numL = numL + 1
            elif numtotal >= 45:
                break
    winsound.Beep(523, 500)
    between()

    #####################################################################################
    # Decrease session

    #decrease (R基準)
    winsound.Beep(523, 5000)
    numtotal = 0
    numsub = 0
    numcom = 0
    numR = 0
    numL = 0
    numdeinR = 0
    numdeinL = 0
    for h in deinnumlist:
        if h ==1:
            RS() #1球目
            numtotal = numtotal + 1
            numcom = numcom + 1
            i = 0
            direction = 'RS'
            Rtime = 0
            selectKey = 0
            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
            trialClock.reset() #ここから2球目
            t = trialClock.getTime()
            (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
            numtotal = numtotal + 1
            numsub = numsub + 1
            if 'right' in selectKey:
                SR() #2球目
                direction = 'SR'
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
            elif 'left' in selectKey:
                SL() #2球目
                direction = 'SL'
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                LR() #3球目
                numtotal = numtotal + 1
                numcom = numcom + 1
                i = 0
                direction = 'LR'
                Rtime = 0
                selectKey = 0
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
        else:
            if numtotal < 45:
                if h % 2 == 0: #偶数
                    i = deinRlist[numdeinR]
                    if i == 1:
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    else: #i==2
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        trialClock.reset() #ここからS試行
                        t = trialClock.getTime()
                        (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
                        numtotal = numtotal + 1
                        numsub = numsub + 1
                        if 'right' in selectKey:
                            SR()
                            direction = 'SR'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                            RL()
                            numtotal = numtotal + 1
                            numcom = numcom + 1
                            direction = 'RL'
                            Rtime = 0
                            selectKey = 'none'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        elif 'left' in selectKey:
                            SL()
                            direction = 'SL'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numdeinR = numdeinR + 1
                elif h % 2 == 1: #奇数
                    i == deinLlist[numdeinL]
                    if i == 1:
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    else: #i==2
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        trialClock.reset() #ここからS試行
                        t = trialClock.getTime()
                        (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
                        numtotal = numtotal + 1
                        numsub = numsub + 1
                        if 'right' in selectKey:
                            SR()
                            direction = 'SR'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        elif 'left' in selectKey:
                            SL()
                            direction = 'SL'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                            LR()
                            numtotal = numtotal + 1
                            numcom = numcom + 1
                            direction = 'LR'
                            Rtime = 0
                            selectKey = 'none'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numdeinL = numdeinL + 1
            elif numtotal >= 45:
                break
    winsound.Beep(523, 500)
    between()

    #####################################################################################
    # Exclusion session

    #exclusion (R基準)
    winsound.Beep(523, 5000)
    numtotal = 0
    numsub = 0
    numcom = 0
    numR = 0
    numL = 0
    for h in exnumlist:
        if h ==1:
            RS() #1球目
            numtotal = numtotal + 1
            numcom = numcom + 1
            i = 0
            direction = 'RS'
            Rtime = 0
            selectKey = 0
            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
            trialClock.reset() #ここから2球目
            t = trialClock.getTime()
            (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
            numtotal = numtotal + 1
            numsub = numsub + 1
            if 'right' in selectKey:
                SR() #2球目
                direction = 'SR'
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
            elif 'left' in selectKey:
                SL() #2球目
                direction = 'SL'
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                LR() #3球目
                numtotal = numtotal + 1
                numcom = numcom + 1
                i = 0
                direction = 'LR'
                Rtime = 0
                selectKey = 0
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
        else:
            if numtotal < 45:
                if h % 2 == 0: #偶数
                    i = exRlist[numexR]
                    if i == 1:
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    else: #i==2
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        trialClock.reset() #ここからS試行
                        t = trialClock.getTime()
                        (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
                        numtotal = numtotal + 1
                        numsub = numsub + 1
                        if 'right' in selectKey:
                            SR()
                            direction = 'SR'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                            RL()
                            numtotal = numtotal + 1
                            numcom = numcom + 1
                            direction = 'RL'
                            Rtime = 0
                            selectKey = 'none'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        elif 'left' in selectKey:
                            SL()
                            direction = 'SL'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numexR = numexR + 1
                elif h % 2 == 1: #奇数
                    i == exLlist[numexL]
                    if i == 1:
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    else: #i==2
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        trialClock.reset() #ここからS試行
                        t = trialClock.getTime()
                        (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
                        numtotal = numtotal + 1
                        numsub = numsub + 1
                        if 'right' in selectKey:
                            SR()
                            direction = 'SR'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        elif 'left' in selectKey:
                            SL()
                            direction = 'SL'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                            LR()
                            numtotal = numtotal + 1
                            numcom = numcom + 1
                            direction = 'LR'
                            Rtime = 0
                            selectKey = 'none'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numexL = numexL + 1
            elif numtotal >= 45:
                break
    winsound.Beep(523, 500)
    between()

    #####################################################################################
    # Increase session

    #increase (R基準)
    winsound.Beep(523, 5000)
    numtotal = 0
    numsub = 0
    numcom = 0
    numR = 0
    numL = 0
    numdeinR = 0
    numdeinL = 0
    for h in deinnumlist:
        if h ==1:
            RS() #1球目
            numtotal = numtotal + 1
            numcom = numcom + 1
            i = 0
            direction = 'RS'
            Rtime = 0
            selectKey = 0
            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
            trialClock.reset() #ここから2球目
            t = trialClock.getTime()
            (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
            numtotal = numtotal + 1
            numsub = numsub + 1
            if 'right' in selectKey:
                SR() #2球目
                direction = 'SR'
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
            elif 'left' in selectKey:
                SL() #2球目
                direction = 'SL'
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                LR() #3球目
                numtotal = numtotal + 1
                numcom = numcom + 1
                i = 0
                direction = 'LR'
                Rtime = 0
                selectKey = 0
                results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
        else:
            if numtotal < 45:
                if h % 2 == 0: #偶数
                    i = deinRlist[numdeinR]
                    if i == 1:
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    else: #i==2
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        trialClock.reset() #ここからS試行
                        t = trialClock.getTime()
                        (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
                        numtotal = numtotal + 1
                        numsub = numsub + 1
                        if 'right' in selectKey:
                            SR()
                            direction = 'SR'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                            RL()
                            numtotal = numtotal + 1
                            numcom = numcom + 1
                            direction = 'RL'
                            Rtime = 0
                            selectKey = 'none'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        elif 'left' in selectKey:
                            SL()
                            direction = 'SL'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numdeinR = numdeinR + 1
                elif h % 2 == 1: #奇数
                    i == deinLlist[numdeinL]
                    if i == 1:
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    else: #i==2
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        trialClock.reset() #ここからS試行
                        t = trialClock.getTime()
                        (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectg is written in capital letter
                        numtotal = numtotal + 1
                        numsub = numsub + 1
                        if 'right' in selectKey:
                            SR()
                            direction = 'SR'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        elif 'left' in selectKey:
                            SL()
                            direction = 'SL'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                            LR()
                            numtotal = numtotal + 1
                            numcom = numcom + 1
                            direction = 'LR'
                            Rtime = 0
                            selectKey = 'none'
                            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numdeinL = numdeinL + 1
            elif numtotal >= 45:
                break
    winsound.Beep(523, 500)
    between()

    #####################################################################################
    # Re-inclusion session

    #Re-inclusion
    winsound.Beep(523, 5000)
    numtotal = 0
    numsub = 0
    numcom = 0
    numR = 0
    numL = 0
    for h in numlist:
        numpy.random.shuffle(Rlist)
        numpy.random.shuffle(Llist)
        if h ==1:
            RS()
            numtotal = numtotal + 1
            numcom = numcom + 1
            i = 0
            direction = 'RS'
            Rtime = 0
            selectKey = 0
            results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
        else:
            if numtotal < 45:
                trialClock.reset()
                t = trialClock.getTime()
                (selectKey, Rtime) = getKeyboardResponse(['right', 'left'], duration = 0) #'K' in selectKey is written in capital letter
                numtotal = numtotal + 1
                numsub = numsub + 1
                if 'right' in selectKey:
                    SR()
                    direction = 'SR'
                    results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    i = Rlist[numR]
                    if i == 1:
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 2:
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 3:
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numR = numR + 1
                elif 'left' in selectKey:
                    SL()
                    direction = 'SL'
                    results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    i = Llist[numL]
                    if i == 1:
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 2:
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        RS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    elif i == 3:
                        LR()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LR'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        RL()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'RL'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                        LS()
                        numtotal = numtotal + 1
                        numcom = numcom + 1
                        direction = 'LS'
                        Rtime = 0
                        selectKey = 'none'
                        results.append([numtotal]+[numsub]+[numcom]+[h]+[i]+[direction]+[Rtime]+[selectKey])
                    numL = numL + 1
            elif numtotal >= 45:
                break
    winsound.Beep(523, 500)

curD = os.getcwd()
datafile = open(os.path.join(curD,'log/Sub'+expInfo['Participant']+'_'+expInfo['dateStr']+'.csv'),'wb')  #save log as csvfile
datafile.write('numtotal,numsub,numcom,h,6ways,direction,responseTime,key\n')
for j in results:
    datafile.write('%d,%d,%d,%d,%d,%s,%f,%s\n' % tuple(j))
datafile.close()

#ウインドウ前面 http://blogs.yahoo.co.jp/topitopi38/1291282.html
#ウインドウ破棄 http://effbot.org/tkinterbook/toplevel.htm
#ウインドウ位置 http://www.shido.info/py/tkinter8.html
#beep音 http://blanktar.jp/blog/2013/08/python-beep.html
