
from createPassMap import buildPassNetwork
from socplot.generateCharts import generatePassChart,generateHeatMap,generateHeatPassMapOverlay
from radarcharts.generateRadarChart import generateRadarChart
import sbpUtils



generateRadarChart(match_id=9592,player_names=["Lionel Messi","Luis Suárez"],competition_id=11,season_id=1)


#buildPassNetwork(match_id=9592,team="Barcelona")

#generatePassChart(9592,"Barcelona",timemax=2)
#generateHeatMap(9592,"Espanyol")


#generateHeatPassMapOverlay(9592,"Barcelona",timeMin=80)


