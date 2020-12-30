import matplotlib.pyplot as plt
from backend import ComplexRadar,get_player_stats,getAveragePerMatch
import sbpUtils



def generateRadarChart(match_id,player_names,competition_id=None,season_id=None):
    variables = ['Pass %', 'Shots', 'Pressures', 'Ball Recoveries', 'Touches in Box', 'Fouls Won','Avg Pass Length']
    ranges = [(0.5, 1), (0, 5), (0, 10), (0, 5), (0, 3), (0, 5),(5,30)]


    data=[]
    label =""
    for player_name in player_names:
        if competition_id is not None and season_id is not None:
            matchList = sbpUtils.getMatchList(competition_id,season_id)
            data.append(getAveragePerMatch(player_name,matchList,len(variables)))
            label = "Radar Chart for Competition {0}, Season {1} \n Average Values per Game".format(competition_id,season_id)
        else:
            data.append(list(get_player_stats(match_id=match_id,player_name=player_name).values()))
            label = "Radar Chart for Match {0}".format(match_id)

    for player in data:
        for index,stat in enumerate(player):

            if stat < ranges[index][0]:
                ranges[index] = (stat,ranges[index][1])
            elif stat > ranges[index][1]:
                ranges[index] = (ranges[index][0],stat)

        # plotting
    plt.rc('font', size=8)
    fig1 = plt.figure(figsize=(6, 6))

    radar = ComplexRadar(fig1, variables, ranges)

    for index,player in enumerate(data):
        radar.plot(player, label=player_names[index])
        radar.fill(player, alpha=0.2)

    radar.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.10),
                    fancybox=True, shadow=True, ncol=4, fontsize=8)

    # Only way i can get it to show properly
    plt.savefig('fig.png', bbox_inches='tight')
    plt.close()
    import matplotlib.image as mpimg
    img = mpimg.imread('fig.png')
    plt.imshow(img)
    plt.axis('off')
    plt.title(label)
    plt.show()
