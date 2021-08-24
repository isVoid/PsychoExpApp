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

import glob, logging, random

import numpy as np


class Main:

    action_animations: Dict[str, Animation]

    def setup(self):
        self.myWin = make_window()
        set_min_style()
        self.myWin.flip(False)
        self.load_actionframes()

        self.expInfo = request_experiment_session_info()
        self.expInfo["sessions"] = {}

        nids = get_player_id()
        self.all_persons = ["f1", "f2", "f3", "m1", "m2", "m3"]
        self.all_emotions = ["pos", "neu", "neg"]

        self.player_ids = (self.all_persons[nids[0]], self.all_persons[nids[1]])

        self.load_videos()

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

    def load_videos(self):
        window_aspect_ratio = self.myWin.size[0] / self.myWin.size[1]
        face_vid_size_norm = (
            np.array([face_vid_aspect_ratio / window_aspect_ratio, 1.0]) * 0.6
        )
        # optimization: only load the videos from player ids that are used
        self.videos = {
            p: {
                e: makeVideo(
                    f"./stim/video/{p}{e}.mp4",
                    self.myWin,
                    pos=(0, 0),
                    size=face_vid_size_norm,
                )
                for e in self.all_emotions
            }
            for p in self.player_ids
        }

    def make_sessions_videos(self):
        """
        Session and User profile factory

        Creates 6 sessions according to presets. expInfo is a dict
        that holds the logs of the experiment.

        Returns a list of session lambdas, len=6
        """
        l, r = self.player_ids
        user_profiles = [
            (self.videos[l]["pos"], self.videos[r]["neg"]),
            (self.videos[l]["pos"], self.videos[r]["pos"]),
            (self.videos[l]["neg"], self.videos[r]["neg"]),
            (self.videos[l]["pos"], self.videos[r]["pos"]),
            (self.videos[l]["neg"], self.videos[r]["neg"]),
            (self.videos[l]["pos"], self.videos[r]["neg"]),
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
                "PNacc",
                acceptance_param_a,
                self.expInfo,
            ],
            [
                total_passes,
                rejection_Spass_func(),
                "PPrej",
                rejection_param_a,
                self.expInfo,
            ],
            [
                total_passes,
                acceptance_Spass_func(),
                "NNacc",
                acceptance_param_a,
                self.expInfo,
            ],
            [
                total_passes,
                acceptance_Spass_func(),
                "PPacc",
                acceptance_param_a,
                self.expInfo,
            ],
            [
                total_passes,
                rejection_Spass_func(),
                "NNrej",
                rejection_param_a,
                self.expInfo,
            ],
            [
                total_passes,
                rejection_Spass_func(),
                "PNrej",
                rejection_param_a,
                self.expInfo,
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
        user_profiles_reordered = [user_profiles[i] for i in ordering]

        return user_profiles_reordered, sessions_reordered

    def sessionloop(self, session, user_profile):
        self.run = True
        while self.run:
            session.poll()
            user_profile[0].draw()
            user_profile[1].draw()
            core.wait(1 / FPS)
            self.myWin.flip()

            if session.finished():
                self.run = False

    def make_practice_session(self):
        session = Session(15, 5, "Practice", 0.5, {"sessions": {}})
        session.init_action_animation(self.action_animations)
        l, r = self.player_ids
        user_profiles = self.videos[l]["neu"], self.videos[r]["neu"]
        user_profiles[0].pos = lface_pos
        user_profiles[1].pos = rface_pos

        return user_profiles, session

    def practice(self):
        user_profile, practice_session = self.make_practice_session()
        instruction1(self.myWin)
        instruction2(self.myWin)
        instruction3(self.myWin)
        connecting(self.myWin)
        self.sessionloop(practice_session, user_profile)

    def main(self):
        # Practice
        self.practice()
        ready_for_test(self.myWin)

        user_profiles_videos, sessions = self.make_sessions_videos()
        for i, p in enumerate(zip(user_profiles_videos, sessions)):
            user_profile, session = p
            user_profile[0].pos = lface_pos
            user_profile[1].pos = rface_pos

            if i < 5:
                self.sessionloop(session, user_profile)
                between(self.myWin)
            else:
                self.sessionloop(session, user_profile)
                end(self.myWin)

        dump_exp_info(self.expInfo)


mainobj = Main()

if __name__ == "__main__":
    LGFMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename="cyberball.log", level=logging.DEBUG, format=LGFMT)
    mainobj.setup()
    mainobj.main()
