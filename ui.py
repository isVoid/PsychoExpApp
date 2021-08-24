import PyQt5
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar, QPushButton, QVBoxLayout

from psychopy import gui, core, data, visual

import time, random, threading
import win32api, win32gui

from constants import __DEBUG__
import texts


class NoKeyboardReturnQDialog(QDialog):
    def keyPressEvent(self, e):
        if (
            e.key() == PyQt5.QtCore.Qt.Key_Enter
            or e.key() == PyQt5.QtCore.Qt.Key_Escape
        ):
            return
        super().keyPressEvent(e)


class QuitOnEscReturnQDialog(QDialog):
    def keyPressEvent(self, e):
        if e.key() == PyQt5.QtCore.Qt.Key_Escape:
            self.done(0)
        super().keyPressEvent(e)


def request_experiment_session_info():
    expInfo = {"Participant": "001"}
    expInfo["date"] = data.getDateStr()

    dlg = gui.DlgFromDict(expInfo, title="Experiment", fixed=["date"])
    if dlg.OK:
        return expInfo
    else:
        core.quit()


def make_qlabel(dlg, txt, font):
    qlabel = QLabel(dlg)
    qlabel.setText(txt)
    qlabel.setFont(font)
    return qlabel


def message(title, labels, main_window, button_name="Next"):
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


def delay_close_qdialog(dlg, t):
    time.sleep(t)
    dlg.close()


def make_connecting_window(main_window, time):
    main_window.setMouseVisible(False)

    dlg = NoKeyboardReturnQDialog()
    dlg.setWindowTitle("Catchball - 3people")

    # Setup layout
    layout = QVBoxLayout()
    font = QFont("Meiryo UI", 20)
    qlabel = make_qlabel(dlg, texts.connecting_txt, font)
    layout.addWidget(qlabel)
    progressbar = QProgressBar()
    progressbar.setRange(0, 0)
    layout.addWidget(progressbar)

    dlg.setLayout(layout)
    dlg.setWindowFlags(dlg.windowFlags() & ~PyQt5.QtCore.Qt.WindowCloseButtonHint)
    dlg.raise_()
    x = threading.Thread(target=delay_close_qdialog, args=(dlg, time))
    x.start()
    dlg.exec()
    x.join()


def make_end_window(main_window):
    main_window.setMouseVisible(False)

    dlg = QuitOnEscReturnQDialog()
    dlg.setWindowTitle("Catchball - 3people")

    # Setup layout
    layout = QVBoxLayout()
    font = QFont("Meiryo UI", 20)
    qlabel = make_qlabel(dlg, texts.end_txt, font)
    layout.addWidget(qlabel)

    dlg.setLayout(layout)
    dlg.setWindowFlags(dlg.windowFlags() & ~PyQt5.QtCore.Qt.WindowCloseButtonHint)
    dlg.raise_()
    dlg.exec()


def instruction1(mywin):
    mywin.flip()
    title = "Catchball(3people) -Instruction 1/3"
    labels = texts.inst1_txt
    message(title, labels, mywin)


def instruction2(mywin):
    title = "Catchball(3people) -Instruction 2/3"
    labels = texts.inst2_txt
    message(title, labels, mywin)


def instruction3(mywin):
    title = "Catchball(3people) -Instruction 3/3"
    labels = texts.inst3_txt
    message(title, labels, mywin, button_name="START")


def connecting(mywin):
    mywin.flip()
    title = "Catchball - 3people"
    labels = texts.conn_txt
    message(title, labels, mywin)

    if __DEBUG__:
        q = 1
    else:
        q = 8

    make_connecting_window(mywin, time=q)


def ready_for_test(mywin):
    mywin.flip()
    title = "Catchball - 3people"
    labels = texts.start_txt

    message(title, labels, mywin, button_name="OK")


def between(mywin):
    mywin.flip()
    title = "Catchball - 3people"
    labels = texts.between_txt

    message(title, labels, mywin, button_name="START")

    if __DEBUG__:
        q = 1
    else:
        q = random.uniform(4.5, 60)

    make_connecting_window(mywin, time=q)


def end(mywin):
    mywin.flip()
    make_end_window(mywin)


def make_window():
    screen_width, screen_height = win32api.GetSystemMetrics(
        0
    ), win32api.GetSystemMetrics(1)
    myWin = visual.Window(
        fullscr=False,
        units="norm",
        size=(screen_width, screen_height),
        name="experiment",
        color=(0.5, 0.5, 0.5),
    )
    myWin.setMouseVisible(False)
    return myWin


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
