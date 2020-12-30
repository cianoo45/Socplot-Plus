from statsbombpy import sb

def get_lineups(match_id):
    lineups = sb.lineups(match_id)
    name_dict = {}
    for team in lineups.keys():
        for index, player in lineups[team].iterrows():
            name_dict[player["player_name"]] = player["player_nickname"]
    return name_dict

def getMatchList(competition_id, season_id):
    matches = sb.matches(competition_id,season_id)
    return matches
