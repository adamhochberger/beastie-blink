import requests
import json

def get_team_info(sport, league_id, season):
    params = {'sport': sport, 'league_id': league_id, 'season': season}
    req = requests.get("https://www.fleaflicker.com/api/FetchLeagueRosters", params)
    league = json.loads(req.text)
    team_id_list = {}
    for team in league["rosters"]:
        team_id_list[team["team"]["name"]] = team["team"]["id"]
    return team_id_list

def get_team_roster(sport, league_id, season, team_id):
    params = {'sport': sport, 'league_id': league_id, 'season': season, 'team_id': team_id}
    req = requests.get("https://www.fleaflicker.com/api/FetchRoster", params)
    parse_group(json.loads(req.text))

def parse_group(roster):
    player_groups = roster["groups"]
    for entry in player_groups:
        if 'group' in entry.keys():
            print(entry["group"], ":", sep="")
        else:
            print('BENCH:')
        slot = entry.get('slots')
        print_team(slot)
    print()

def print_team(player_list):
    # print(json.dumps(player_list, indent=2))
    for player in player_list:
        if 'leaguePlayer' in player.keys():
            print(player["leaguePlayer"]["proPlayer"]["nameFull"])
    print()

def main():
    teams = get_team_info('NBA', 23630, 2019)
    for team in teams:
        print(team)
        get_team_roster('NBA', 23630, 2019, teams[team])


if __name__ == "__main__":
    main()
 