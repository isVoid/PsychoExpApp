from typing import Dict

from ui import (
    instruction2,
    make_window,
    set_min_style,
    between,
    end,
    instruction1,
    instruction2,
    instruction3,
    connecting,
    ready_for_test,
)
from videos import makeVideo
from animation import make_actimagestim, Animation
from utils import get_player_id, request_experiment_session_info, dump_exp_info
from session import Session
from psychopy import core

from constants import (
    act_pos,
    act_size,
    playball_frame_duration,
    face_vid_aspect_ratio,
    lface_pos,
    rface_pos,
    FPS,
)

import glob, logging, random, threading, itertools, multiprocessing
from enum import Enum

import numpy as np


class VideoDirection(Enum):
    FORWARD = 0
    REVERSE = 1


class Main:

    action_animations: Dict[str, Animation]

    def setup(self):
        self.myWin = make_window()
        self.myWin.flip(False)
        self.load_actionframes()

        self.expInfo = request_experiment_session_info()
        self.expInfo["sessions"] = {}

        nids = get_player_id()
        self.all_persons = ["f1", "f2", "f3", "m1", "m2", "m3"]
        self.all_emotions = ["pos", "neu", "neg"]

        self.player_ids = (self.all_persons[nids[0]], self.all_persons[nids[1]])

    def load_actionframes(self):
        LS_image_stim = [
            make_actimagestim(x, self.myWin, act_pos, act_size)
            for x in sorted(glob.glob("./stim/1toY*"))
        ]
        LR_image_stim = [
            make_actimagestim(x, self.myWin, act_pos, act_size)
            for x in sorted(glob.glob("./stim/1to2*"))
        ]
        RS_image_stim = [
            make_actimagestim(x, self.myWin, act_pos, act_size)
            for x in sorted(glob.glob("./stim/2toY*"))
        ]
        RL_image_stim = [
            make_actimagestim(x, self.myWin, act_pos, act_size)
            for x in sorted(glob.glob("./stim/2to1*"))
        ]
        SL_image_stim = [
            make_actimagestim(x, self.myWin, act_pos, act_size)
            for x in sorted(glob.glob("./stim/Yto1*"))
        ]
        SR_image_stim = [
            make_actimagestim(x, self.myWin, act_pos, act_size)
            for x in sorted(glob.glob("./stim/Yto2*"))
        ]

        LSAnimation = Animation(LS_image_stim, playball_frame_duration)
        LRAnimation = Animation(LR_image_stim, playball_frame_duration)
        RSAnimation = Animation(RS_image_stim, playball_frame_duration)
        RLAnimation = Animation(RL_image_stim, playball_frame_duration)
        SLAnimation = Animation(SL_image_stim, playball_frame_duration)
        SRAnimation = Animation(SR_image_stim, playball_frame_duration)

        self.action_animations = {
            "LS": LSAnimation,
            "LR": LRAnimation,
            "RS": RSAnimation,
            "RL": RLAnimation,
            "SL": SLAnimation,
            "SR": SRAnimation,
        }

    def prepare_video(self, pid0, emotion0, pid1, emotion1):
        """Should be called in separate thread to avoid high block."""
        window_aspect_ratio = self.myWin.size[0] / self.myWin.size[1]
        face_vid_size_norm = (
            np.array([face_vid_aspect_ratio / window_aspect_ratio, 1.0]) * 0.6
        )
        video0_forward = makeVideo(
            f"./stim/video/{pid0}{emotion0}.mp4",
            self.myWin,
            pos=lface_pos,
            size=face_vid_size_norm,
        )
        video0_reverse = makeVideo(
            f"./stim/video/reversed_{pid0}{emotion0}.mp4",
            self.myWin,
            pos=lface_pos,
            size=face_vid_size_norm,
        )
        video1_forward = makeVideo(
            f"./stim/video/{pid1}{emotion1}.mp4",
            self.myWin,
            pos=rface_pos,
            size=face_vid_size_norm,
        )
        video1_reverse = makeVideo(
            f"./stim/video/reversed_{pid1}{emotion1}.mp4",
            self.myWin,
            pos=rface_pos,
            size=face_vid_size_norm,
        )

        self.current_video_forward = (video0_forward, video1_forward)
        self.current_video_reverse = (video0_reverse, video1_reverse)

    def launch_prepare_video_asnyc(self, user_profiles):
        p1, p2 = user_profiles
        self.videoLoadingThread = threading.Thread(
            target=self.prepare_video, args=(p1[0], p1[1], p2[0], p2[1])
        )
        self.videoLoadingThread.start()

    def post_prepare_video_join(self):
        """Should be called in main thread to post process
        self.current_video_forawrd and self.current_video_reverse
        to do whatever that was not doable in subthreads
        """
        self.current_video_forward[0].setRetraceRate(self.myWin)
        self.current_video_forward[1].setRetraceRate(self.myWin)
        self.current_video_reverse[0].setRetraceRate(self.myWin)
        self.current_video_reverse[1].setRetraceRate(self.myWin)

        self.current_video_forward[0]._updateFrameTexture()
        self.current_video_forward[1]._updateFrameTexture()
        # current_video_reverse._updateFrameTexture is called inside the
        # while loop of self.sessionloop.

    def make_sessions_videos(self):
        """
        Session and User profile factory

        Creates 6 sessions according to presets. expInfo is a dict
        that holds the logs of the experiment.

        Returns a list of session lambdas, len=6
        """
        l, r = self.player_ids

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
                "PNacc",
                acceptance_param_a,
                self.expInfo,
                ((l, "pos"), (r, "neg")),
            ],
            [
                total_passes,
                rejection_Spass_func(),
                "PPrej",
                rejection_param_a,
                self.expInfo,
                ((l, "pos"), (r, "pos")),
            ],
            [
                total_passes,
                acceptance_Spass_func(),
                "NNacc",
                acceptance_param_a,
                self.expInfo,
                ((l, "neg"), (r, "neg")),
            ],
            [
                total_passes,
                acceptance_Spass_func(),
                "PPacc",
                acceptance_param_a,
                self.expInfo,
                ((l, "pos"), (r, "pos")),
            ],
            [
                total_passes,
                rejection_Spass_func(),
                "NNrej",
                rejection_param_a,
                self.expInfo,
                ((l, "neg"), (r, "neg")),
            ],
            [
                total_passes,
                rejection_Spass_func(),
                "PNrej",
                rejection_param_a,
                self.expInfo,
                ((l, "pos"), (r, "neg")),
            ],
        ]

        sessions = [Session(*arg) for arg in session_args]
        for s in sessions:
            s.init_action_animation(self.action_animations)
        # Fix front and back. Shuffle middle ones
        mid_ordering = list(range(1, len(sessions) - 1, 1))
        random.shuffle(mid_ordering)
        ordering = [0] + mid_ordering + [len(sessions) - 1]

        sessions_reordered = [sessions[i] for i in ordering]

        return sessions_reordered

    def resetVideo(self, video0, video1):
        video0.loadMovie(video0.filename)
        video1.loadMovie(video1.filename)

    def sessionloop(self, session):
        self.videoLoadingThread.join()
        # Required by async movie loading (MovieStim4)
        self.post_prepare_video_join()

        self.current_video = self.current_video_forward
        self.current_video_direction = VideoDirection.FORWARD

        reverse_reload_thread = threading.Thread(
            target=self.resetVideo, args=(self.current_video_reverse)
        )

        self.run = True
        while self.run:
            session.poll()
            core.wait(1 / FPS)
            self.myWin.flip()
            self.current_video[0].draw()
            self.current_video[1].draw()
            if session.finished():
                self.run = False

            # When movie is finished, switch .current_video to the other playback
            # direction.
            if self.current_video[0].finished() or self.current_video[1].finished():
                if self.current_video_direction == VideoDirection.FORWARD:
                    # Switch to reverse direction, start reloading
                    # forward video async
                    self.current_video_direction = VideoDirection.REVERSE
                    if reverse_reload_thread.isAlive():  # Cannot join if not started
                        reverse_reload_thread.join()
                    self.current_video = self.current_video_reverse
                    forward_reload_thread = threading.Thread(
                        target=self.resetVideo, args=(self.current_video_forward)
                    )
                    forward_reload_thread.start()
                else:
                    # Switch to forward direction, start reloading
                    # reverse video async
                    self.current_video_direction = VideoDirection.FORWARD
                    forward_reload_thread.join()
                    self.current_video = self.current_video_forward
                    reverse_reload_thread = threading.Thread(
                        target=self.resetVideo, args=(self.current_video_reverse)
                    )
                    reverse_reload_thread.start()
                # self.current_video_reverse first time calling _updateFrameTexture()
                # is also here.
                self.current_video[0]._updateFrameTexture()
                self.current_video[1]._updateFrameTexture()

        self.myWin.flip()

    def make_practice_session(self):
        l, r = self.player_ids
        session = Session(
            15, 5, "Practice", 0.5, {"sessions": {}}, ((l, "neu"), (r, "neu"))
        )
        session.init_action_animation(self.action_animations)
        return session

    def practice(self):
        practice_session = self.make_practice_session()
        self.launch_prepare_video_asnyc(practice_session.user_profile)
        instruction1(self.myWin)
        instruction2(self.myWin)
        instruction3(self.myWin)
        connecting(self.myWin)
        self.sessionloop(practice_session)

    def main(self):
        # Practice
        self.practice()

        sessions = self.make_sessions_videos()
        self.launch_prepare_video_asnyc(sessions[0].user_profile)
        ready_for_test(self.myWin)
        for i, session in enumerate(sessions):
            if i < 5:
                self.sessionloop(session)
                self.launch_prepare_video_asnyc(sessions[i + 1].user_profile)
                between(self.myWin)
            else:
                self.sessionloop(session)
                end(self.myWin)

        dump_exp_info(self.expInfo)


mainobj = Main()

if __name__ == "__main__":
    LGFMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename="cyberball.log", level=logging.DEBUG, format=LGFMT)
    mainobj.setup()
    mainobj.main()
