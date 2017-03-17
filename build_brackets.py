import ncaa
import csv 
from bs4 import BeautifulSoup
import urllib
import re


def parse_teams(filename):
    starting_teams = []
    
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None) #skip header row
        for row in reader:
            if (row):
                name = row[0]
                odds = row[1]
                wins = row[2]
                losses = row[3]
                status = row[4]
                team = ncaa.Team(name, odds, wins, losses,status)
                starting_teams.append(team)
    f.closed

    return starting_teams

def build_matchups(teams):
    matchups = []
    i = 0
    while (i < len(teams)):
        matchups.append(ncaa.Matchup(teams[i], teams[i+1]))
        # increment by 2 since the csv file has all teams playing each other
        # listed sequentially
        i+=2
    return matchups
    
# just return the team with the greater # of wins for now
def pick_winner(matchup):
    team1 = matchup.team1
    team2 = matchup.team2
    
    if (team1.wins > team2.wins):
        return team1
    elif (team1.wins == team2.wins):
        # punt for now; if they're equal, just return team1
        return team1
    else: 
        return team2
     
def main():
    starting_teams = parse_teams('data/teams.csv')
    matchups = build_matchups(starting_teams)
    for m in matchups:
        print("Matchup: {0} vs {1}".format(m.team1.name,m.team2.name))
        winner = pick_winner(m)
        print("Predict {0} will win".format(winner.name))
    
if __name__ == "__main__":
    main()