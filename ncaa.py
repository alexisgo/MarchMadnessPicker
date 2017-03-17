class Bracket(object):
    def __init__(self, starting_teams):
        self.starting_teams = starting_teams


class Team(object):
    def __init__(self, name, odds, wins, losses, status):
        self.name = name
        self.odds = odds
        self.wins = wins
        self.losses = losses
        # team status is either "alive" or "eliminated"
        self.status = status

class Matchup(object):

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        #todo: add date    
