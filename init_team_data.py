import ncaa
import math 
import csv 
from bs4 import BeautifulSoup
import urllib
import re
import csv

def build_teams_and_odds(filename):
    url = "http://www.cbssports.com/college-basketball/news/march-madness-2017-point-spreads-lines-odds-released-for-ncaa-tournament-games/"
    r = urllib.urlopen(url).read()
    soup = BeautifulSoup(r)
    strong_tags = soup.select("strong") 
    matchups = []
    teams = []
    for t in strong_tags:
        s = str(t.contents)
        if ("day," in s):
            table = t.parent.next_sibling

            # build matchups
            matches = table.select("tbody tr > td:nth-of-type(2)")
            for m in matches:
                if (m.has_attr('data-sheets-value')):
                    matchup = m.string.encode("utf8")
                    matchup_str = re.search('(.*) \((\d+)-(\d+)\) vs. (.*)\s(?:\((\d+)-(\d+)\))?', matchup, re.DOTALL)
                    if matchup_str:
                        name = matchup_str.group(1)
                        wins = matchup_str.group(2)
                        losses = matchup_str.group(3)
                        t2_name = matchup_str.group(4)
                        # There are several entries on the page where the winners from the first
                        # four haven't been updated. Ignore these. 
                        if (not "winner" in t2_name):
                            t2_wins = matchup_str.group(5)
                            t2_losses = matchup_str.group(6) 
                        else:
                            t2_wins = ""
                            t2_losses = ""
                        team1 = ncaa.Team(name, None, wins, losses, "alive")
                        team2 = ncaa.Team(t2_name, None, t2_wins, t2_losses, "alive")
                        teams.append(team1)
                        teams.append(team2)
                        matchups.append(ncaa.Matchup(team1, team2))

                next_sibling = m.next_sibling
                if (next_sibling):
                    if (next_sibling.has_attr('data-sheets-value')):
                        odds = next_sibling['data-sheets-value']                    
                        team_and_odds = re.search('.*:.*:\"(.*) (-.*)\"', odds, re.DOTALL)
                        if team_and_odds:
                            team_name = team_and_odds.group(1).replace(".", "")
                            odds = float(team_and_odds.group(2))
                            if team_name == name: 
                                team1.odds = odds
                                team2.odds = math.fabs(odds)
                            elif team_name == t2_name:
                                team2.odds = odds
                                team1.odds = math.fabs(odds)
                            else:
                                print("team {0} not found".format(team_name))
    return matchups 
    
def write_teams_to_file(filename, matchups):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Team_Name', 'Team_Odds', 'Team_Wins', 'Team_Losses', 'Team_Status'])    
        for match in matchups:
            t1 = match.team1
            t2 = match.team2
            writer.writerow([t1.name, t1.odds, t1.wins, t1.losses, t1.status])    
            writer.writerow([t2.name, t2.odds, t2.wins, t2.losses, t2.status])    
    
    csvfile.closed
       
def main():
    filename = 'data/teams.csv'
    matchups = build_teams_and_odds(filename)
    write_teams_to_file(filename, matchups)

if __name__ == "__main__":
    main()