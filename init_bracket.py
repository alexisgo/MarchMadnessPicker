import csv 
from bs4 import BeautifulSoup
import urllib
import re

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
    
def build_odds():
    url = "http://www.cbssports.com/college-basketball/news/march-madness-2017-point-spreads-lines-odds-released-for-ncaa-tournament-games/"
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    strong_tags = soup.select("strong") 
    for t in strong_tags:
        s = str(t.contents)
        if ("day," in s):
            table = t.parent.next_sibling
            tds = table.select("tbody tr > td:nth-of-type(3)")
            for td in tds:
                if (td.has_attr('data-sheets-value')):
                    odds = td['data-sheets-value']                    
                    team_and_odds = re.search('.*:.*:\"(.*) (-.*)\"', odds, re.DOTALL)
                    if team_and_odds:
                        team = team_and_odds.group(1)
                        team = team.replace(".", "")
                        print("team: {0}".format(team))
                        odds = team_and_odds.group(2)
                        print("odds: {0}".format(odds))
                    # now grab the teams from the cvs, and add the odds to it
    
def vegas_line(team):
    # format:
    
    # http://www.vegasinsider.com/college-basketball/matchups/matchups.cfm/date/MM-DD-YY
    # to-do: parse out the odds
#    print(soup.prettify())
    return 1

def team_record_weight(team):
    return 10
    
def weight(team):
    return random.randint(1,101)
     #return (vegas_line(team) * 0.3) +  (record_team_weight(team) * 0.3) + (foo(team) * 0.4)
     
def main():
    starting_teams = parse_teams('data/first-four-teams.csv')
    matchups = build_matchups(starting_teams)
    for m in matchups:
        print("Matchup: {0} vs {1} - {2}".format(m.team1.name,m.team2.name,m.date))
        winner = pick_winner(m)
        print("Predict {0} will win".format(winner.name))
    build_odds()
    
    # to-do: loop through matches and call pick_winner on each    
    # to-do: loop through the initial data, and fill in with specific stats

if __name__ == "__main__":
    main()