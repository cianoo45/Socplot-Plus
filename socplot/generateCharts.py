import pandas as pd
import statsbombpy.sb as sb
from socplot.pitch import Pitch
import matplotlib.pyplot as plt

"""
wrapper function around socplot.pitch.plot_passes

Calls the statsbombpy api and filters results based on parameters

match_id = ID of the match
team = Name of the team the passmap is for
timemin,timemax = Constraints on time of event (I.E between 0th and 10th minute etc) 
overlay - Only used when generating an overlayed pass/heat map
"""


def generatePassChart(match_id, team, timemin=0, timemax=90,overlay=False):
    events = sb.events(match_id, fmt="dict")

    passList = []
    for key in events.keys():

        if events[key]['type']['name'] == "Pass" and events[key]['possession_team']['name'] == team \
                and timemax > int(events[key]['minute']) > timemin:
            location = events[key]['location']
            end_location = events[key]['pass']['end_location']
            pass_type = events[key]['pass']['height']['name']
            passList.append([location, end_location, pass_type])

    passes = pd.DataFrame(passList[0:1], columns=['location', 'end_location', 'pass_type'])


    pitch = Pitch()

    for _, row in passes.iterrows():
        pitch.plot_pass(row['location'], row['end_location'], pass_type=row['pass_type'],
                        match_id=match_id, team=team, timeMax=timemax, timeMin=timemin)
    if overlay:
        return pitch
    else:
        plt.show()


"""
wrapper function around socplot.pitch.heat_map

Calls the statsbombpy api and filters results based on parameters

match_id = ID of the match
team = Name of the team the passmap is for
timemin,timemax = Constraints on time of event (I.E between 0th and 10th minute etc) 
pitch = Only used when generating overlayed pass/heat map

TODO: Corner areas don't seem to be rendering properly on the heatmaps
"""
def generateHeatMap(match_id, team, timemin=0, timemax=90, pitch=None):
    events = sb.events(match_id)
    eventsFiltered = events[events.location.notnull()]

    xVals = []
    yVals = []
    for index, row in eventsFiltered.iterrows():
        if row['team'] == team and row['minute'] < timemax > timemin:
            xVals.append(row["location"][0])
            yVals.append(row["location"][1])

    if pitch == None:
        pitch = Pitch()
    pitch.heat_map(xVals, yVals)
    plt.show()



"""
Overlays a passmap ontop of a heat map

Calls the statsbombpy api and filters results based on parameters

match_id = ID of the match
team = Name of the team the passmap is for
timemin,timemax = Constraints on time of event (I.E between 0th and 10th minute etc) 
"""
def generateHeatPassMapOverlay(match_id,  team, timeMax=90, timeMin=0):
    passPitch = generatePassChart(match_id=match_id, team=team, timemax=timeMax, timemin=timeMin,overlay=True)
    generateHeatMap(match_id=match_id,team=team,timemin=timeMin,timemax=timeMax,pitch=passPitch)

