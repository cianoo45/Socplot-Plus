import pandas as pd
from pandas import json_normalize
from statsbombpy import sb
import sbpUtils
import numpy as np

def _invert(x, limits):
    """inverts a value x on a scale from
    limits[0] to limits[1]"""
    return limits[1] - (x - limits[0])

def _scale_data(data, ranges):
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d = _invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1)
                     * (x2 - x1) + x1)
    return sdata

class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles = np.arange(0, 360, 360./len(variables))

        axes = [fig.add_axes([0.1,0.1,0.9,0.9],polar=True,
                label = "axes{}".format(i))
                for i in range(len(variables))]
        l, text = axes[0].set_thetagrids(angles,
                                         labels=variables)
        [txt.set_rotation(angle-90) for txt, angle
             in zip(text, angles)]
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for i, ax in enumerate(axes):
            grid = np.linspace(*ranges[i],
                               num=n_ordinate_levels)
            gridlabel = ["{}".format(round(x,2))
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid = grid[::-1] # hack to invert grid
                          # gridlabels aren't reversed
            gridlabel[0] = "" # clean up origin
            ax.set_rgrids(grid, labels=gridlabel,
                         angle=angles[i])
            #ax.spines["polar"].set_visible(False)
            ax.set_ylim(*ranges[i])
        # variables for plotting
        self.angle = np.deg2rad(np.r_[angles, angles[0]])
        self.ranges = ranges
        self.ax = axes[0]
    def plot(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.plot(self.angle, np.r_[sdata, sdata[0]], *args, **kw)
    def fill(self, data, *args, **kw):
        sdata = _scale_data(data, self.ranges)
        self.ax.fill(self.angle, np.r_[sdata, sdata[0]], *args, **kw)

def get_player_stats(match_id, player_name):


    events = sb.events(match_id=match_id,fmt="dict")
    newApiEvents = []
    for event in events.keys():
        newApiEvents.append(events[event])

    data = json_normalize(newApiEvents, sep='_')

    # Get events for this player
    player = data[(data['player_name'] == player_name)]

    if len(player)==0:
        lineup_dict = sbpUtils.get_lineups(match_id)
        dict_reversed = dict((v,k) for k,v in lineup_dict.items())
        try:
            player = data[(data['player_name'] == dict_reversed[player_name])]
        except:
            print("Player not found in match")
            return 0

    # Calculate pass percentage
    passes = player[(player['type_name'] == 'Pass')]['pass_outcome_name']
    passes_complete = passes.isna().sum()
    pass_percentage = passes_complete / len(passes)

    # Number of shots
    shots = player[(player['type_name'] == 'Shot')]['shot_outcome_name'].count()

    # Number of pressures
    pressures = player[(player['type_name'] == 'Pressure')]['type_name'].count()

    # Number of ball recoveries
    ball_recoveries = player[(player['type_name'] == 'Ball Recovery')]['type_name'].count()

    # Number of touches in the box
    touches = player[(player['type_name'] == 'Shot') | (player['type_name'] == 'Pass')]['location']
    touches_in_box = []
    for touch in touches.values:
        if touch[0] >= 114 and touch[1] >= 30 and touch[1] <= 50:
            touches_in_box.append(touch)
    touches_in_box_count = len(touches_in_box)

    # Number of fouls won
    fouls_won = player[(player['type_name'] == 'Foul Won')]['type_name'].count()

    passes = player[player.pass_length.notnull()]
    if len(passes)==0:
        avg_pass_length =0
    else:
        avg_pass_length = passes['pass_length'].sum() / len(passes)

    player_stats = {
        'pass_percentage': float(pass_percentage),
        'shots': int(shots),
        'pressures': int(pressures),
        'ball_recoveries': int(ball_recoveries),
        'touches_in_box': int(touches_in_box_count),
        'fouls_won': int(fouls_won),
        'avg_pass_length': float(avg_pass_length)
    }

    return player_stats


def getAveragePerMatch(player_name,matchList,variableCount):
    playerStats =  [0] * variableCount
    matchCount=0
    for index,match in matchList.iterrows():
         stats = get_player_stats(match['match_id'],player_name)
         if stats !=0:
             stats = list(stats.values())
             matchCount=matchCount+1
             for index,stat in enumerate(playerStats):
                 playerStats[index] = stats[index]+stat

    for index,stat in enumerate(playerStats):
        playerStats[index] = stat/matchCount

    return playerStats



