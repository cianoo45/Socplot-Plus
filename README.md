# Socplot-Plus

Socplot-Plus is a tool for Creating Visualizations from the StatsbombPy API, It incorporates code from other tools such as Socplot, passing-networks-in-python
as well as some custom additions__[WIP]__


## Why Socplot-Plus?
- Has the most features of any public repo for Statsbomb
- Pass Map, Heat map, Pass/Heat Map Overlay
- Passing Network
- Radar Charts with multiple players, Single match or Per game averages for a whole season

## Gallery

__Pressure heat map__

pressures position heat map for an example match
![](https://raw.githubusercontent.com/ArqamFC/socplot/master/docs/gallery/heatmap1.png)

![](https://raw.githubusercontent.com/ArqamFC/socplot/master/docs/gallery/heatmap2.png)

__Pass map__

pass map for selected time window in an example match
![](https://github.com/ArqamFC/socplot/blob/master/docs/gallery/pass_map1.png)

first 15 mins passes in an example match
![](https://github.com/ArqamFC/socplot/blob/master/docs/gallery/pass_map2.png)

__Pass Network__
Passing Network for a selected Game + Team
![](https://github.com/Friends-of-Tracking-Data-FoTD/passing-networks-in-python/blob/master/plots/statsbomb_match7576_Portugal_pass_value.png)

__Radar Chart__

Radar chart for two players , Average per game values over the course of a season
![](https://github.com/cianoo45/Socplot-Plus/blob/main/socplot/fig.png)
## Example 

```python
code snippet used to generate the last image
from radarcharts.generateRadarChart import generateRadarChart
generateRadarChart(match_id=None,player_names=["Lionel Messi","Luis Suárez"],competition_id=11,season_id=1)
```

__



## Dev Installation

```shell
# fork the repo
cd socplot
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

## LICENCE

ArqamFc/Socplot licensed under the __Apache License 2.0__.
