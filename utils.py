import logging, random

from psychopy import gui, data, core
import pandas as pd


def get_player_id():
    all_players = [x for x in range(0, 5)]
    random.shuffle(all_players)
    playerids = all_players[0:2]
    logging.debug(f"Selected user ids: {playerids}")
    return playerids


def request_experiment_session_info():
    expInfo = {"Participant": "001"}
    expInfo["date"] = data.getDateStr()

    dlg = gui.DlgFromDict(expInfo, title="Experiment", fixed=["date"])
    if dlg.OK:
        return expInfo
    else:
        core.quit()


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
