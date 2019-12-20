import requests
import json


def set_params(league_id, season, sport='NBA'):
    return {'sport': sport, 'league_id': league_id, 'season': season}

def get_team_info(params, name=""):
    req = requests.get("https://www.fleaflicker.com/api/FetchLeagueRosters", params)
    league = json.loads(req.text)
    team_list = {}
    for team in league["rosters"]:
        if name == "":
            team_list[team["team"]["name"]] = team["team"]["id"]
        else:
            if name == team["team"]["name"]:
                team_list[team["team"]["name"]] = team["team"]["id"]   
                return team_list
    return team_list

def parse_team_dict(params, team_list):
    for team in team_list:
        print("*****  ", team, "  *****")
        get_team_roster(params, team_list[team])

def get_team_roster(params, team_id):
    params['team_id'] = team_id
    req = requests.get("https://www.fleaflicker.com/api/FetchRoster", params)
    parse_group(json.loads(req.text))
    del params['team_id']

def parse_group(roster):
    player_groups = roster["groups"]
    for entry in player_groups:
        if 'group' in entry.keys():
            print(entry["group"], ":", sep="")
        else:
            print('BENCH:')
        slot = entry.get('slots')
        print_team(slot)

def print_team(player_list):
    # print(json.dumps(player_list, indent=2))
    for player in player_list:
        if 'leaguePlayer' in player.keys():
            print(player["leaguePlayer"]["proPlayer"]["nameFull"])
    print()

def main():
    params = set_params(23630, 2019)
    parse_team_dict(params, get_team_info(params, "Kyrie IRving"))

if __name__ == "__main__":
    main()
 