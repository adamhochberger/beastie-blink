import requests
import json


def set_params(league_id, season=2019, sport='NBA'):
    '''Creates a dictionary of requests parameters

    Keyword arguments:
    league_id -- id of league (integer)
    season -- season where data originates (default is 2019)
    sport -- type of league (default is 'NBA')
    
    Function is to be run before calling request functions
    Will be further implemented to include optional parameters for use in
        different API calls
    Return is the dictionary structure with those given values
    '''
    return {'sport': sport, 'league_id': league_id, 'season': season}

def get_team_info(params, name=""):
    '''Retrieves team names and team ids

    Keyword arguments:
    params -- dictionary of request params (see set_params)
    name -- team name, if looking for one entry (default is "")
    
    Function is run to obtain the names and IDs of all teams in league
        (if one is not specified)

    Return:
    Dictionary structure with {team_name: team_id} pairings
    '''
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
    '''Simplifies team_list dictionary and obtains rosters

    Keyword arguments:
    params -- dictionary of request params (see set_params)
    team_list -- dictionary of {team_name: team_id} pairings
    
    Function is run to print name, and pass team id to get_team_roster
        for all teams in the team_list structure
    '''
    for team in team_list:
        print("*****  ", team, "  *****")
        get_team_roster(params, team_list[team])

def get_team_roster(params, team_id):
    '''Makes API request for team roster

    Keyword arguments:
    params -- dictionary of request params (see set_params)
    team_id -- Fleaflicker team id (integer)
    
    Function is run to obtain the players of the team denoted by team_id
    Passes the json-formatted request to parse_group
    Removes 'team_id' parameter to prevent errors with other functions
    '''
    params['team_id'] = team_id
    req = requests.get("https://www.fleaflicker.com/api/FetchRoster", params)
    parse_group(json.loads(req.text))
    del params['team_id']

def parse_group(roster):
    '''Separates raw input from request into player groups

    Keyword arguments:
    roster -- JSON-formatted data of all players on roster
    
    Function prints corresponding player group and passes structure to
        print_team for player names to be printed
    Due to lack of 'group' key for one of the entries in player_groups
        an if-check is used to denote bench players from others
    '''
    player_groups = roster["groups"]
    for entry in player_groups:
        if 'group' in entry.keys():
            print(entry["group"], ":", sep="")
        else:
            print('BENCH:')
        slot = entry.get('slots')
        print_team(slot)

def print_team(player_list):
    '''Prints out all players from player_list structure

    Keyword arguments:
    player_list -- JSON-formatted data of form 
        {
            leaguePlayer:{ 
                proPlayer:{ 
                    nameFull:string
                }...
            }...
        }
    
    Function prints the nameFull attribute from the above model
    Because slots can be blank, if-check determines if a leaguePlayer key
        is in the current slot from player_list    
    '''
    # print(json.dumps(player_list, indent=2))
    for slot in player_list:
        if 'leaguePlayer' in slot.keys():
            print(slot["leaguePlayer"]["proPlayer"]["nameFull"])
    print()

def main():
    '''Sets params and checks for a team in the league'''
    params = set_params(23630, 2019)
    parse_team_dict(params, get_team_info(params, "Kyrie IRving"))

if __name__ == "__main__":
    main()
 