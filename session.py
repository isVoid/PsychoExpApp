import random
from enum import Enum
import warnings
import logging

from typing import Tuple, Dict, Optional

from animation import Animation

from psychopy import core, event


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


class Position(Enum):
    """SELF, LEFT, RIGHT"""

    SELF = 0
    LEFT = 1
    RIGHT = 2


class SessionState(Enum):
    """Several states of the session:
    SELECT_TARGET:
        The previous action (ball pass) has finished, waiting to pick
        the next target.
    WAIT_USER:
        Waiting user input.
    IN_ACTION:
        Currently in the middle of the action.
    ACTION_FINISHED:
        The previous action sequence has finished.
    INVALID:
        Session is not running or something is wrong

    Transition condition and actions to take:
    SELECT_TARGET:
        if current pos is SELF: go to WAIT_USER state and wait for user input
        if current pos is not SELF: perform set_target() and go to IN_ACTION
    WAIT_USER:
        if user has valid input: perform set_target and go to IN_ACTION
        otherwise: do no-op and go to WAIT_USER
    IN_ACTION:
        if current action sequence has not finished:
            perform play_next_action_frame(), and go to IN_ACTION
        if current action sequence has finished:
            perform no-op and go to ACTION_FINISHED
    ACTION_FINISHED:
        if current passes < total_passes, go to SELECT_TARGET, perform no-op
        if current passes == total_passes, exit dfa
    """

    SELECT_TARGET = 0
    WAIT_USER_SETUP = 1
    WAIT_USER = 2
    IN_ACTION = 3
    ACTION_FINISHED = 4

    INVALID = -1


class Session:
    """Manages session variables and state transition

    A session should start with SELECT_TARGET state.

    Member Variables
    ----------------
    total_passes: int
        The total number of passes in the session
    num_Spass_totl: int
        The total number of passes to Position.SELF
    a: float
        The "magic parameter" for the probablistic model.
        See `prob_model` for detail.
    session_label: str
        The unique string to label the session.
    expInfo: dict
        A dictionary to record the process of the session

    cur_pos: Position
        The current starting position of the action.
    cur_target: Position
        The current ending position of the action.
    passes: int
        The number of passes in this session so far.
    num_Spass: int
        The number of passes to Position.SELF in this session
        so far.

    state: SessionState
        The current state of the session. See SessionState
        for detail
    """

    total_passes: int
    num_Spass_totl: int
    a: float
    session_label: str
    expInfo: Dict

    cur_pos: Position
    cur_target: Optional[Position]
    passes: int
    num_Spass: int

    state: SessionState
    cur_action: Animation

    reaction_time_t: float

    _pos_to_animation_map: Dict[Tuple[Position, Position], Animation]

    def __init__(self, total_passes, num_Spass_totl, session_label, a, expInfo):
        """Make sure you have called init_action_animation after init"""
        self.total_passes = total_passes
        self.num_Spass_totl = num_Spass_totl
        self.session_label = session_label
        self.a = a
        self.expInfo = expInfo

        self.cur_pos = random.choice(list(Position))
        # Only have cur_pos, no target at the start
        self.cur_target = None
        self.num_Spass = 0
        self.passes = 0

        self.state = SessionState.SELECT_TARGET
        self.expInfo["sessions"][self.session_label] = {
            "positions": [self.cur_pos],
            "reaction_times": [],
        }

    def init_action_animation(self, action_animations):
        self._pos_to_animation_map = {
            (Position.LEFT, Position.RIGHT): action_animations["LR"],
            (Position.LEFT, Position.SELF): action_animations["LS"],
            (Position.RIGHT, Position.LEFT): action_animations["RL"],
            (Position.RIGHT, Position.SELF): action_animations["RS"],
            (Position.SELF, Position.LEFT): action_animations["SL"],
            (Position.SELF, Position.RIGHT): action_animations["SR"],
        }
        self.cur_action = action_animations["SL"]

    def _update_action_and_record(self):
        """Based on `cur_pos` and `cur_target`, choose the proper
        `cur_action`
        """
        self.cur_action = self._pos_to_animation_map[(self.cur_pos, self.cur_target)]
        self.cur_action.reset()
        self.expInfo["sessions"][self.session_label]["positions"].append(
            self.cur_target
        )

    def _select_target_non_self(self):
        """Pick the next target to throw at when cur positions
        is not `SELF`.
        """
        self.cur_pos = self.cur_target if self.cur_target is not None else self.cur_pos
        should_pass_to_self = prob_model(
            self.total_passes - self.passes,
            self.num_Spass_totl - self.num_Spass,
            self.a,
        )
        if should_pass_to_self:
            self.cur_target = Position.SELF
            self.num_Spass += 1
        else:
            self.cur_target = (
                Position.LEFT if self.cur_pos == Position.RIGHT else Position.RIGHT
            )
        logging.debug([self.cur_pos, self.cur_target])
        self._update_action_and_record()

    def _set_temporary_self_action(self):
        # At this point, the next animation has not been determined,
        # however, we need to play the first frame of the animation
        # where the ball is at SELF position. We just temporarily set
        # the animation to be something starting with SELF
        if self.cur_pos == Position.LEFT:
            self.cur_action = self._pos_to_animation_map[(Position.SELF, Position.LEFT)]
        elif self.cur_pos == Position.RIGHT:
            self.cur_action = self._pos_to_animation_map[
                (Position.SELF, Position.RIGHT)
            ]
        self.cur_action.reset()

    def _wait_user_setup(self):
        event.clearEvents()
        self._reaction_time_t = core.getTime()

    def _check_user_select_target_async(self):
        """Check if the user has finished picking the target
        asynchronously and set the next target accordingly.

        If not updated, do nothing and return.
        Otherwise, update cur_pos and cur_target accordingly.

        Return
        ------
        True if the user has finished picking the target.
        False if the user did not perform any input.
        """
        getKeyRes = event.getKeys(["left", "right", "q"], timeStamped=True)
        if len(getKeyRes) > 0:
            self.cur_pos = (
                self.cur_target if self.cur_target is not None else self.cur_pos
            )
            key, reaction_timestamp = getKeyRes[0]
            logging.debug(f"key {key}")
            if "left" == key:
                self.cur_target = Position.LEFT
            elif "right" == key:
                self.cur_target = Position.RIGHT
            else:
                # Backdoor to early terminate experiment
                core.quit()
            self._update_action_and_record()
            self.expInfo["sessions"][self.session_label]["reaction_times"].append(
                reaction_timestamp - self._reaction_time_t
            )
            return True
        return False

    def _check_cur_action_animaion_has_finished(self):
        """Check if current animation in action has finished.

        Return
        ------
        True if the action animation is finished
        False otherwise
        """
        return self.cur_action.finished()

    def _draw_action_animation(self):
        """Advance to the next action animation"""
        self.cur_action.draw()

    def _draw_first_frame_animation(self):
        """Only draw the first frame of the action, do not increment frame index"""
        self.cur_action.draw_first_frame()

    def poll(self):
        if self.state == SessionState.SELECT_TARGET:
            if self.cur_target == Position.SELF or (
                self.cur_target is None and self.cur_pos == Position.SELF
            ):
                self.state = SessionState.WAIT_USER_SETUP
                self._set_temporary_self_action()
                self._draw_first_frame_animation()
            else:
                self._select_target_non_self()
                self.state = SessionState.IN_ACTION
                self._draw_action_animation()
        elif self.state == SessionState.WAIT_USER_SETUP:
            self._wait_user_setup()
            self.state = SessionState.WAIT_USER
            self._draw_first_frame_animation()
        elif self.state == SessionState.WAIT_USER:
            if self._check_user_select_target_async():
                self.state = SessionState.IN_ACTION
            self._draw_first_frame_animation()
        elif self.state == SessionState.IN_ACTION:
            if self._check_cur_action_animaion_has_finished():
                self.state = SessionState.ACTION_FINISHED
                self.passes += 1
            self._draw_action_animation()
        elif self.state == SessionState.ACTION_FINISHED:
            if self.passes == self.total_passes:
                self.state = SessionState.INVALID
            else:
                self.state = SessionState.SELECT_TARGET
            self._draw_action_animation()
        else:
            warnings.warn("Reached invalid session state.")
            import pdb

            pdb.set_trace()

    def finished(self):
        return self.state == SessionState.INVALID
