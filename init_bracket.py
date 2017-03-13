from sets import Set
import csv 

class Bracket(object):
    def __init__(self, starting_teams):
        self.starting_teams = starting_teams


class Team(object):
    def __init__(self, name, id, game, status):
        self.id = id
        self.name = name
        self.game = game
        
        # team status is either "alive" or "eliminated"
        self.status = status

class Matchup(object):

    def __init__(self, team1, team2, date):
        self.team1 = team1
        self.team2 = team2
        self.date = date

def parse_teams(filename):
    starting_teams = []
    
    # read from a csv of teams to parse them into a dict with just their ids
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None) #skip header row
        for row in reader:
            if (row):
                team = Team(row[0], row[1], row[2], "alive")          
                starting_teams.append(team)
    f.closed

    return starting_teams

def grab_team_stats():
    # to-do: find wins, losses, ties
    return 

def build_matchups(teams):
    matchups = []
    i = 0
    while (i < len(teams)):
        matchups.append(Matchup(teams[i], teams[i+1], teams[i].game))
        i+=2
    return matchups
    
def fill_bracket(matchups):
    for match in matchups:
        pick_winner(match)    
        
def pick_winner(matchup):
    team1 = matchup.team1
    team2 = matchup.team2
    if (vegas_line(team1) == vegas_line(team2)):
        # todo: change this to a random selection between the two
        return team1
    elif (vegas_line(team1) > vegas_line(team2)): return team1
    else: return team2
    
def vegas_line(team):
    # to-do: beautiful soup to parse http://www.vegasinsider.com/college-basketball/odds/las-vegas/
    return 1
    
def main():
    starting_teams = parse_teams('data/first-four-teams.csv')
    matchups = build_matchups(starting_teams)
    for m in matchups:
        print("Matchup: {0} vs {1} - {2}".format(m.team1.name,m.team2.name,m.date))
    # to-do: loop through the initial data, and fill in with specific stats

if __name__ == "__main__":
    main()